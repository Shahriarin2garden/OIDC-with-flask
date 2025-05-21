import hashlib
import base64

def verify_pkce(code_challenge, code_verifier):
    if not code_challenge or not code_verifier:
        return False

    digest = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    calculated_challenge = base64.urlsafe_b64encode(digest).decode('utf-8').rstrip('=')
    return calculated_challenge == code_challenge
