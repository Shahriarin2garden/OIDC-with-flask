import uuid
from datetime import datetime
from typing import Dict, Optional

# In-memory storage for registered clients
registered_clients: Dict[str, Dict] = {}

def register_client(metadata: Dict) -> Dict:
    """
    Register a new OAuth client.
    Args:
        metadata: Client metadata including redirect URIs
    Returns:
        Dict containing client credentials and metadata
    """
    client_id = str(uuid.uuid4())
    client_secret = str(uuid.uuid4())
    
    required_fields = ['redirect_uris', 'grant_types', 'response_types']
    for field in required_fields:
        if field not in metadata:
            raise ValueError(f"Missing required field: {field}")
    
    client_info = {
        "client_id": client_id,
        "client_secret": client_secret,
        "registration_time": datetime.utcnow().isoformat(),
        **metadata
    }
    
    registered_clients[client_id] = client_info
    return client_info

def get_client(client_id: str) -> Optional[Dict]:
    """
    Retrieve registered client information.
    Returns None if client_id not found.
    """
    return registered_clients.get(client_id)