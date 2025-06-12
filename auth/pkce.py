import base64
import hashlib
import secrets
from typing import Literal

def create_code_verifier(length: int = 64) -> str:
    """
    Generate a code verifier for PKCE.
    Args:
        length: Length of the verifier (default: 64)
    Returns:
        A URL-safe base64-encoded string
    """
    return base64.urlsafe_b64encode(
        secrets.token_bytes(length)
    ).decode('utf-8').rstrip('=')

def create_code_challenge(
    code_verifier: str, 
    method: Literal['S256', 'plain'] = 'S256'
) -> str:
    """
    Create a code challenge from the code verifier.
    Args:
        code_verifier: The code verifier string
        method: The challenge method ('S256' or 'plain')
    Returns:
        The code challenge string
    """
    if method == 'S256':
        hash_digest = hashlib.sha256(code_verifier.encode()).digest()
        return base64.urlsafe_b64encode(hash_digest).decode('utf-8').rstrip('=')
    return code_verifier

def verify_code_challenge(
    code_verifier: str,
    code_challenge: str,
    method: Literal['S256', 'plain'] = 'S256'
) -> bool:
    """
    Verify the code challenge matches the code verifier.
    """
    return create_code_challenge(code_verifier, method) == code_challenge