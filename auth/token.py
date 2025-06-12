# flask-oidc-provider/auth/token.py

import jwt
from datetime import datetime, timezone, timedelta
from typing import Dict, Optional
from flask import current_app
from cryptography.hazmat.primitives import serialization
from config import Config

def create_jwt(
    payload: Dict,
    private_key: str,
    algorithm: str = 'RS256',
    expiry_hours: int = 1
) -> str:
    """
    Create a signed JWT token.
    Args:
        payload: Dict containing claims
        private_key: RSA private key for signing
        algorithm: Signing algorithm (default: RS256)
        expiry_hours: Token expiry in hours (default: 1)
    """
    now = datetime.now(timezone.utc)
    payload.update({
        'iat': now,
        'exp': now + timedelta(hours=expiry_hours),
        'iss': 'http://localhost:5000'  # Match your ISSUER_URL
    })
    return jwt.encode(payload, private_key, algorithm=algorithm)

def validate_token(
    token: str,
    public_key: str,
    algorithm: str = 'RS256'
) -> Optional[Dict]:
    """
    Validate and decode a JWT token.
    Returns decoded payload if valid, None if invalid.
    """
    try:
        return jwt.decode(
            token,
            public_key,
            algorithms=[algorithm],
            issuer='http://localhost:5000'  # Match your ISSUER_URL
        )
    except jwt.InvalidTokenError:
        return None

class TokenService:
    @staticmethod
    def generate_id_token(sub, aud, nonce=None):
        now = datetime.now(timezone.utc)
        payload = {
            "iss": "http://localhost:5000",
            "sub": sub,
            "aud": aud,
            "iat": now,
            "exp": now + timedelta(minutes=10),
            "auth_time": now,
        }
        if nonce:
            payload["nonce"] = nonce

        private_key = Config.load_private_key()
        key = serialization.load_pem_private_key(private_key, password=None)
        return jwt.encode(payload, key, algorithm="RS256")

    @staticmethod
    def generate_access_token(sub, scope):
        now = datetime.datetime.utcnow()
        payload = {
            "iss": "http://localhost:5000",
            "sub": sub,
            "scope": scope,
            "iat": now,
            "exp": now + datetime.timedelta(minutes=30)
        }

        private_key = Config.load_private_key()
        key = serialization.load_pem_private_key(private_key, password=None)
        return jwt.encode(payload, key, algorithm="RS256")

    @staticmethod
    def generate_refresh_token(sub):
        now = datetime.datetime.utcnow()
        payload = {
            "iss": "http://localhost:5000",
            "sub": sub,
            "iat": now,
            "exp": now + datetime.timedelta(days=30),
            "type": "refresh"
        }

        private_key = Config.load_private_key()
        key = serialization.load_pem_private_key(private_key, password=None)
        return jwt.encode(payload, key, algorithm="RS256")

    @staticmethod
    def decode_token(token):
        public_key = Config.load_public_key()
        key = serialization.load_pem_public_key(public_key)
        return jwt.decode(token, key=key, algorithms=["RS256"], options={"verify_aud": False})
