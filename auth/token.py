# flask-oidc-provider/auth/token.py

import jwt
import datetime
from flask import current_app
from cryptography.hazmat.primitives import serialization
from config import Config

class TokenService:
    @staticmethod
    def generate_id_token(sub, aud, nonce=None):
        now = datetime.datetime.utcnow()
        payload = {
            "iss": "http://localhost:5000",
            "sub": sub,
            "aud": aud,
            "iat": now,
            "exp": now + datetime.timedelta(minutes=10),
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
