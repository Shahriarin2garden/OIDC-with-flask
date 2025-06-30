"""
Complete OIDC Flow Test with Manual Browser Instructions
"""

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

print("="*60)
print("OIDC PROVIDER TEST CLIENT")
print("="*60)
print()
print("🔧 TROUBLESHOOTING STEPS FOR BROWSER LOGIN:")
print("1. Clear ALL browser data for localhost (cookies, cache, local storage)")
print("2. Use Incognito/Private browsing mode")
print("3. Disable browser extensions temporarily")
print("4. Try a different browser (Firefox, Edge, Safari)")
print()
print("📝 LOGIN CREDENTIALS:")
print("   Username: alice")
print("   Password: alicepassword")
print("   (Alternative: bob / bobpassword)")
print()
print("🚨 COMMON ISSUES & SOLUTIONS:")
print("   - If you see 'invalid_credentials': Clear browser data and try again")
print("   - If form doesn't submit: Check if JavaScript is enabled")
print("   - If page refreshes: Use fresh incognito window")
print("   - If multiple tabs open: Close all localhost tabs first")
print()

class CallbackHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return  # Suppress default logging
        
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        code = query.get('code', [None])[0]
        error = query.get('error', [None])[0]
        
        if error:
            print(f"❌ Authorization failed: {error}")
            error_description = query.get('error_description', ['Unknown error'])[0]
            print(f"   Description: {error_description}")
            
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            error_html = f"""
            <html><body>
            <h1>❌ Authorization Failed</h1>
            <p><strong>Error:</strong> {error}</p>
            <p><strong>Description:</strong> {error_description}</p>
            <p><a href="javascript:window.close()">Close Window</a></p>
            </body></html>
            """
            self.wfile.write(error_html.encode())
            return
        
        if code:
            print("✅ Authorization code received!")
            print("🔄 Exchanging code for tokens...")
            
            try:
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
                )
                
                if token_response.status_code == 200:
                    tokens = token_response.json()
                    print("✅ Tokens received successfully!")
                    
                    # Get user info using access token
                    print("🔄 Fetching user info...")
                    userinfo_response = requests.get(
                        f"{PROVIDER_URL}/userinfo",
                        headers={'Authorization': f"Bearer {tokens['access_token']}"}
                    )
                    
                    if userinfo_response.status_code == 200:
                        userinfo = userinfo_response.json()
                        print("✅ User info received successfully!")
                        print()
                        print("🎉 COMPLETE OIDC FLOW SUCCESSFUL!")
                        print("="*50)
                        print("📋 RESULTS:")
                        print(f"   User: {userinfo.get('name', 'N/A')}")
                        print(f"   Email: {userinfo.get('email', 'N/A')}")
                        print(f"   Subject: {userinfo.get('sub', 'N/A')}")
                        print()
                        print("🔑 TOKEN INFO:")
                        print(f"   Access Token: {tokens['access_token'][:20]}...")
                        print(f"   ID Token: {tokens['id_token'][:20]}...")
                        print(f"   Token Type: {tokens.get('token_type', 'N/A')}")
                        print(f"   Expires In: {tokens.get('expires_in', 'N/A')} seconds")
                        
                        self.send_response(200)
                        self.send_header('Content-type', 'text/html')
                        self.end_headers()
                        
                        success_html = f"""
                        <html><body style="font-family: Arial, sans-serif; margin: 40px;">
                        <h1 style="color: green;">🎉 Authentication Successful!</h1>
                        
                        <h2>👤 User Information:</h2>
                        <table border="1" style="border-collapse: collapse; width: 100%;">
                        <tr><td><strong>Name</strong></td><td>{userinfo.get('name', 'N/A')}</td></tr>
                        <tr><td><strong>Email</strong></td><td>{userinfo.get('email', 'N/A')}</td></tr>
                        <tr><td><strong>Subject</strong></td><td>{userinfo.get('sub', 'N/A')}</td></tr>
                        </table>
                        
                        <h2>🔑 Tokens:</h2>
                        <textarea style="width: 100%; height: 150px; font-family: monospace;">
Access Token: {tokens['access_token']}

ID Token: {tokens['id_token']}

Token Type: {tokens.get('token_type', 'N/A')}
Expires In: {tokens.get('expires_in', 'N/A')} seconds
                        </textarea>
                        
                        <p><button onclick="window.close()">Close Window</button></p>
                        </body></html>
                        """
                        self.wfile.write(success_html.encode())
                    else:
                        print(f"❌ Failed to get user info: {userinfo_response.status_code}")
                        print(f"   Response: {userinfo_response.text}")
                else:
                    print(f"❌ Token exchange failed: {token_response.status_code}")
                    print(f"   Response: {token_response.text}")
                    
            except Exception as e:
                print(f"❌ Error during token exchange: {e}")
        else:
            print("❌ No authorization code received")
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>No authorization code received</h1>')

def main():
    # Start callback server
    server = HTTPServer(('localhost', 8080), CallbackHandler)
    print("🚀 Starting callback server on http://localhost:8080")
    print()
    
    # Build authorization URL
    auth_url = (
        f"{PROVIDER_URL}/authorize"
        f"?response_type=code"
        f"&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope={SCOPE.replace(' ', '%20')}"
        f"&code_challenge={code_challenge}"
        f"&code_challenge_method=S256"
    )
    
    print("🔗 AUTHORIZATION URL:")
    print(auth_url)
    print()
    print("🌐 Opening browser for authorization...")
    print("   If browser doesn't open, copy the URL above and paste it into your browser")
    print()
    print("⏳ Waiting for authorization callback...")
    print("   Press Ctrl+C to stop the server")
    print()
    
    try:
        webbrowser.open(auth_url)
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print("\n🛑 Server stopped.")

if __name__ == '__main__':
    main()
