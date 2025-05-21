# flask-oidc-provider/models.py

"""
In-memory data stores for clients, users, authorization codes, and tokens.
For production, replace with persistent database/storage.
"""

# Registered OAuth clients (client_id as key)
clients = {
    "client123": {
        "client_id": "client123",
        "redirect_uris": ["http://localhost:8080/callback"],
        "scope": "openid profile email",
        "client_secret": "secret123"  # if applicable
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
