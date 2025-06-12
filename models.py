# flask-oidc-provider/models.py

"""
In-memory data stores for clients, users, authorization codes, and tokens.
For production, replace with persistent database/storage.
"""

import time

# Registered OAuth clients (client_id as key)
clients = {
    "client123": {
        "client_id": "client123",
        "client_secret": "secret123",
        "redirect_uris": ["http://localhost:8080/callback"],
        "grant_types": ["authorization_code", "refresh_token"],
        "response_types": ["code"],
        "scope": "openid profile email"
    }
}

# User store keyed by username
users = {
    "alice": {
        "sub": "user-alice",
        "name": "Alice",
        "email": "alice@example.com",
        "password": "alicepassword"  # In production, store hashed passwords!
    },
    "bob": {
        "sub": "user-bob",
        "name": "Bob",
        "email": "bob@example.com",
        "password": "bobpassword"
    }
}

# Authorization codes store (code: {details})
authorization_codes = {}

# Access and refresh tokens store (token: {details})
tokens = {}

def add_token(token, data):
    data["issued_at"] = int(time.time())
    tokens[token] = data

def is_token_expired(token_data):
    issued_at = token_data.get("issued_at", 0)
    expires_in = token_data.get("expires_in", 0)
    return time.time() > (issued_at + expires_in)

def validate_token(token):
    token_data = tokens.get(token)
    if not token_data:
        return None
    if is_token_expired(token_data):
        del tokens[token]
        return None
    return token_data

def cleanup_expired_tokens():
    now = time.time()
    expired_tokens = [
        token for token, data in tokens.items()
        if now > data.get("issued_at", 0) + data.get("expires_in", 0)
    ]
    for token in expired_tokens:
        del tokens[token]
