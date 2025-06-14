"""
PKCE (Proof Key for Code Exchange) Generator for OIDC Testing
"""
import base64
import hashlib
import secrets

def generate_pkce_pair():
    """Generate a PKCE code verifier and challenge pair."""
    code_verifier = secrets.token_urlsafe(32)
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).decode().rstrip('=')
    
    return {
        "code_verifier": code_verifier,
        "code_challenge": code_challenge
    }

if __name__ == "__main__":
    pkce = generate_pkce_pair()
    print("\nPKCE Values for Postman Testing:")
    print("-" * 40)
    print(f"Code Verifier: {pkce['code_verifier']}")
    print(f"Code Challenge: {pkce['code_challenge']}")
    print("-" * 40)
    print("\nInstructions:")
    print("1. Copy these values to your Postman environment")
    print("2. Set 'CODE_VERIFIER' to the Code Verifier value")
    print("3. Set 'CODE_CHALLENGE' to the Code Challenge value")
    print("\nNote: Generate new values for each test session")
