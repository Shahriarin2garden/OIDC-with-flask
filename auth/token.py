# flask-oidc-provider/auth/token.py

import jwt
import time
from config import Config

private_key = Config.load_private_key()
issuer = Config.ISSUER_URL
expiry = Config.TOKEN_EXPIRY

def generate_id_token(user, client_id):
    now = int(time.time())
    payload = {
        "iss": issuer,
        "sub": user["sub"],
        "aud": client_id,
        "iat": now,
        "exp": now + expiry,
        "name": user["name"],
        "email": user["email"]
    }
    return jwt.encode(payload, private_key, algorithm="RS256")

def generate_access_token(user, client_id):
    now = int(time.time())
    payload = {
        "iss": issuer,
        "sub": user["sub"],
        "aud": client_id,
        "iat": now,
        "exp": now + expiry,
        "scope": "openid profile email"
    }
    return jwt.encode(payload, private_key, algorithm="RS256")

def introspect_token(token):
    try:
        payload = jwt.decode(token, Config.load_public_key(), algorithms=["RS256"], audience=None)
        return payload
    except jwt.ExpiredSignatureError:
        return {"active": False, "error": "expired"}
    except jwt.InvalidTokenError:
        return {"active": False, "error": "invalid"}
