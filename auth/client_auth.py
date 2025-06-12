from typing import Optional, Dict

# Simple in-memory client storage
clients: Dict[str, Dict] = {
    "default_client": {
        "client_secret": "default_secret",
        "redirect_uris": ["http://localhost:8000/callback"],
        "grant_types": ["authorization_code"],
        "response_types": ["code"],
        "scope": "openid profile email"
    }
}

def authenticate_client(client_id: str, client_secret: str) -> bool:
    """
    Authenticate a client using client_id and client_secret.
    Returns True if authentication successful, False otherwise.
    """
    if client_id in clients:
        return clients[client_id]["client_secret"] == client_secret
    return False

def get_client_config(client_id: str) -> Optional[Dict]:
    """
    Get client configuration.
    Returns client config dict if found, None otherwise.
    """
    return clients.get(client_id)