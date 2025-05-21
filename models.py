# flask-oidc-provider/models.py

# In-memory client, user, token, and code stores
# In production, use persistent storage like a database

clients = {
    "client123": {
        "client_id": "client123",
        "redirect_uris": ["http://localhost:8080/callback"],
        "scope": "openid profile email"
    }
}

users = {
    "alice": {
        "sub": "user-alice",
        "name": "Alice",
        "email": "alice@example.com",
        "password": "alicepassword"
    },
    "bob": {
        "sub": "user-bob",
        "name": "Bob",
        "email": "bob@example.com",
        "password": "bobpassword"
    }
}

authorization_codes = {}
tokens = {}
