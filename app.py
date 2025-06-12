# flask-oidc-provider/app.py

from flask import Flask, redirect, request, render_template, session, jsonify
from datetime import datetime, timezone
from typing import Tuple, Dict, Any, Optional
import uuid
from auth.token import TokenService
from auth.pkce import verify_code_challenge
from auth.client_auth import authenticate_client, get_client_config
from models import clients, authorization_codes, tokens, users, cleanup_expired_tokens
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = app.config['SECRET_KEY']  # Required for session management

def create_error_response(error: str, description: str, status: int = 400) -> Tuple[Dict, int]:
    """Create standardized error response"""
    return jsonify({
        "error": error,
        "error_description": description
    }), status

def authenticate_client() -> Tuple[Dict[str, Any], Optional[Tuple[Dict, int]]]:
    """Authenticate client using Basic auth or request body"""
    auth = request.authorization
    if auth:
        client_id = auth.username
        client_secret = auth.password
    else:
        client_id = request.form.get("client_id")
        client_secret = request.form.get("client_secret")

    if not client_id or not client_secret:
        return None, create_error_response(
            "invalid_client",
            "Missing client credentials"
        )

    client = get_client_config(client_id)
    if not client or not authenticate_client(client_id, client_secret):
        return None, create_error_response(
            "invalid_client",
            "Invalid client credentials"
        )

    return client, None

@app.route("/")
def index():
    return "OIDC Provider is Running"

@app.route("/.well-known/openid-configuration")
def openid_configuration() -> Dict[str, Any]:
    """OpenID Connect discovery endpoint"""
    return jsonify({
        "issuer": "http://localhost:5000",
        "authorization_endpoint": f"{request.url_root}authorize",
        "token_endpoint": f"{request.url_root}token",
        "userinfo_endpoint": f"{request.url_root}userinfo",
        "jwks_uri": f"{request.url_root}.well-known/jwks.json",
        "scopes_supported": ["openid", "profile", "email"],
        "response_types_supported": ["code"],
        "token_endpoint_auth_methods_supported": ["client_secret_basic"],
        "grant_types_supported": ["authorization_code", "refresh_token"],
        "subject_types_supported": ["public"],
        "id_token_signing_alg_values_supported": ["RS256"]
    })

@app.route("/.well-known/jwks.json")
def jwks():
    """JSON Web Key Set endpoint"""
    return Config.load_jwks(), 200, {"Content-Type": "application/json"}

@app.route("/authorize", methods=["GET", "POST"])
def authorize():
    """Authorization endpoint"""
    if request.method == "GET":
        client_id = request.args.get("client_id")
        redirect_uri = request.args.get("redirect_uri")
        scope = request.args.get("scope", "openid")
        response_type = request.args.get("response_type")
        
        print(f"Request params: client_id={client_id}, redirect_uri={redirect_uri}, response_type={response_type}")
        
        # Basic validation
        if not client_id or not redirect_uri or not response_type:
            return create_error_response(
                "invalid_request",
                "Missing required parameters"
            )
            
        # Validate client and redirect URI
        client = get_client_config(client_id)
        print(f"Found client: {client}")
        
        if not client:
            return create_error_response(
                "invalid_client",
                "Unknown client"
            )
            
        if redirect_uri not in client.get("redirect_uris", []):
            return create_error_response(
                "invalid_request",
                "Invalid redirect URI"
            )

        # Validate response type
        if response_type != "code":
            return create_error_response(
                "unsupported_response_type",
                "Only 'code' response type is supported"
            )

        # Store request parameters in session
        session.update({
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'state': request.args.get("state"),
            'scope': scope,
            'code_challenge': request.args.get("code_challenge"),
            'code_challenge_method': request.args.get("code_challenge_method", "S256"),
            'nonce': request.args.get("nonce")
        })
        
        return render_template("login.html")

    # Handle POST (login)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        print(f"Login attempt for user: {username}")
        
        user = users.get(username)
        print(f"Found user: {user}")

        if not user or user['password'] != password:  # In production, use proper password hashing
            print("Invalid credentials")
            return create_error_response("invalid_credentials", "Invalid username or password", 401)

        session['user'] = username
        print(f"User {username} authenticated successfully")
          # Get the scope string and split it into a list
        scope_string = session.get('scope', 'openid')
        scopes = [s.strip() for s in scope_string.split() if s.strip()]
        print(f"Rendering consent page with scopes: {scopes}")
        return render_template(
            "consent.html", 
            client_id=session.get('client_id'),
            scopes=scopes
        )

@app.route("/consent", methods=["POST"])
def consent():
    """Handle user consent"""
    if "user" not in session:
        print("No active session found")
        return create_error_response("unauthorized", "No active session", 401)

    # Check if user denied access
    if request.form.get("action") == "deny":
        redirect_uri = (
            f"{session['redirect_uri']}?"
            f"error=access_denied&"
            f"error_description=User denied access&"
            f"state={session.get('state', '')}"
        )
        return redirect(redirect_uri)

    # Generate authorization code
    code = str(uuid.uuid4())
    
    # Ensure scope is properly formatted
    scope_string = session.get('scope', 'openid')
    scopes = ' '.join(s.strip() for s in scope_string.split() if s.strip())
    
    authorization_codes[code] = {
        "client_id": session['client_id'],
        "user": session['user'],
        "code_challenge": session.get('code_challenge'),
        "code_challenge_method": session.get('code_challenge_method', 'S256'),
        "scope": scopes,
        "created_at": datetime.now(timezone.utc)
    }

    print(f"Generated authorization code for user {session['user']} with scopes: {scopes}")

    # Redirect back to client with the code
    redirect_uri = (
        f"{session['redirect_uri']}?"
        f"code={code}&"
        f"state={session.get('state', '')}"
    )
    return redirect(redirect_uri)

@app.route("/token", methods=["POST"])
def token():
    """Token endpoint"""
    client, error = authenticate_client()
    if error:
        return error

    grant_type = request.form.get("grant_type", "authorization_code")
    
    if grant_type == "authorization_code":
        return handle_authorization_code_grant()
    elif grant_type == "refresh_token":
        return handle_refresh_token_grant()
    else:
        return create_error_response(
            "unsupported_grant_type", 
            f"Grant type '{grant_type}' not supported"
        )

def handle_authorization_code_grant() -> Tuple[Dict[str, Any], int]:
    """Handle authorization code grant type"""
    code = request.form.get("code")
    client_id = request.form.get("client_id")
    code_verifier = request.form.get("code_verifier")

    # Validate authorization code
    auth_code = authorization_codes.pop(code, None)
    if not auth_code or auth_code["client_id"] != client_id:
        return create_error_response("invalid_grant", "Invalid authorization code")

    # Verify PKCE
    if not verify_code_challenge(
        code_verifier,
        auth_code['code_challenge'],
        auth_code['code_challenge_method']
    ):
        return create_error_response("invalid_grant", "Invalid code verifier")

    # Generate tokens
    user = users[auth_code['user']]
    tokens_response = generate_token_response(user, client_id, auth_code['scope'])
    return jsonify(tokens_response)

def handle_refresh_token_grant() -> Tuple[Dict[str, Any], int]:
    """Handle refresh token grant type"""
    refresh_token = request.form.get("refresh_token")
    try:
        decoded = TokenService.decode_token(refresh_token)
        if decoded.get("type") != "refresh":
            return create_error_response("invalid_grant", "Invalid token type")
        
        new_access_token = TokenService.generate_access_token(
            decoded["sub"], 
            decoded.get("scope", "")
        )
        return jsonify({
            "access_token": new_access_token,
            "token_type": "Bearer",
            "expires_in": 1800
        })
    except Exception as e:
        return create_error_response("invalid_grant", str(e))

def generate_token_response(user: Dict, client_id: str, scope: str) -> Dict[str, Any]:
    """Generate complete token response"""
    id_token = TokenService.generate_id_token(user["sub"], client_id)
    access_token = TokenService.generate_access_token(user["sub"], scope)
    refresh_token = TokenService.generate_refresh_token(user["sub"])

    # Store token information
    tokens[access_token] = {"user": user, "client_id": client_id}
    tokens[refresh_token] = {"user": user, "client_id": client_id}

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "id_token": id_token,
        "token_type": "Bearer",
        "expires_in": 3600
    }

@app.route("/userinfo")
def userinfo():
    """UserInfo endpoint"""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return create_error_response("invalid_token", "Missing or invalid token", 401)

    token = auth_header.replace("Bearer ", "")
    token_data = tokens.get(token)
    if not token_data:
        return create_error_response("invalid_token", "Token not found", 401)

    user = token_data["user"]
    return jsonify({
        "sub": user["sub"],
        "name": user["name"],
        "email": user["email"],
        "email_verified": True
    })

@app.before_request
def cleanup():
    """Cleanup expired tokens before each request"""
    cleanup_expired_tokens()

if __name__ == '__main__':
    app.run(debug=Config.DEBUG)
