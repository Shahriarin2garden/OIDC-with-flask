import requests
import base64
import hashlib
import os
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# OIDC Provider configuration
PROVIDER_URL = "http://localhost:5000"
CLIENT_ID = "client123"
CLIENT_SECRET = "secret123"
REDIRECT_URI = "http://localhost:8080/callback"
SCOPE = "openid profile email"

# Generate PKCE values
code_verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')
code_challenge = base64.urlsafe_b64encode(
    hashlib.sha256(code_verifier.encode()).digest()
).rstrip(b'=').decode('utf-8')

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        code = query.get('code', [None])[0]
        
        if code:
            # Exchange code for tokens
            token_response = requests.post(
                f"{PROVIDER_URL}/token",
                data={
                    'grant_type': 'authorization_code',
                    'code': code,
                    'redirect_uri': REDIRECT_URI,
                    'client_id': CLIENT_ID,
                    'client_secret': CLIENT_SECRET,
                    'code_verifier': code_verifier
                }
            ).json()
            
            # Get user info using access token
            userinfo_response = requests.get(
                f"{PROVIDER_URL}/userinfo",
                headers={'Authorization': f"Bearer {token_response['access_token']}"}
            ).json()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            response_html = f"""
            <h1>Authentication Successful!</h1>
            <h2>Tokens:</h2>
            <pre>{token_response}</pre>
            <h2>User Info:</h2>
            <pre>{userinfo_response}</pre>
            """
            self.wfile.write(response_html.encode())
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'No authorization code received')

def main():
    # Start callback server
    server = HTTPServer(('localhost', 8080), CallbackHandler)
    print("Starting callback server on http://localhost:8080")
    
    # Build authorization URL
    auth_url = (
        f"{PROVIDER_URL}/authorize"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope={SCOPE}"
        f"&code_challenge={code_challenge}"
        f"&code_challenge_method=S256"
    )
    
    print(f"Opening browser for authorization at:\n{auth_url}")
    webbrowser.open(auth_url)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print("\nServer stopped.")

if __name__ == '__main__':
    main()
