# flask-oidc-provider/app.py

from flask import Flask, redirect, request, render_template, session, jsonify
from auth.token import TokenService
from auth.pkce import verify_code_challenge
from auth.client_auth import authenticate_client, get_client_config
from models import clients, authorization_codes, tokens, users, cleanup_expired_tokens
from config import Config
import uuid
from datetime import datetime
from typing import Tuple, Dict, Any, Optional

app = Flask(__name__)
app.config.from_object(Config)

def create_error_response(error: str, description: str, status: int = 400) -> Tuple[Dict, int]:
    """Create standardized error response"""
    return jsonify({
        "error": error,
        "error_description": description
    }), status

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
        
        # Validate client and redirect URI
        client = get_client_config(client_id)
        if not client or redirect_uri not in client.get("redirect_uris", []):
            return create_error_response("invalid_client", "Invalid client or redirect URI")

        # Store authorization request parameters
        session.update({
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'state': request.args.get("state"),
            'scope': request.args.get("scope", "openid"),
            'code_challenge': request.args.get("code_challenge"),
            'code_challenge_method': request.args.get("code_challenge_method", "S256")
        })
        return render_template("login.html")

    # Handle POST (login)
    username = request.form.get("username")
    password = request.form.get("password")
    user = users.get(username)

    if not user or user['password'] != password:  # In production, use proper password hashing
        return create_error_response("invalid_credentials", "Invalid username or password", 401)

    session['user'] = username
    return render_template(
        "consent.html", 
        client_id=session['client_id'], 
        scope=session['scope']
    )

@app.route("/consent", methods=["POST"])
def consent():
    """Handle user consent"""
    if "user" not in session:
        return create_error_response("unauthorized", "No active session", 401)

    # Generate authorization code
    code = str(uuid.uuid4())
    authorization_codes[code] = {
        "client_id": session['client_id'],
        "user": session['user'],
        "code_challenge": session['code_challenge'],
        "code_challenge_method": session['code_challenge_method'],
        "scope": session['scope'],
        "created_at": datetime.utcnow()
    }

    # Redirect back to client
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
