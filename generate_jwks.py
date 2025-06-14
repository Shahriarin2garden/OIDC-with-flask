import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime
import base64

def int_to_base64(value):
    value_hex = format(value, 'x')
    # Ensure even length
    if len(value_hex) % 2 == 1:
        value_hex = '0' + value_hex
    value_bytes = bytes.fromhex(value_hex)
    return base64.urlsafe_b64encode(value_bytes).rstrip(b'=').decode('ascii')

# Load the public key
with open('keys/public.pem', 'rb') as f:
    public_key = serialization.load_pem_public_key(f.read())

# Create JWKS
if isinstance(public_key, rsa.RSAPublicKey):
    numbers = public_key.public_numbers()
    jwk = {
        'kty': 'RSA',
        'use': 'sig',
        'kid': datetime.now().strftime('%Y-%m-%d-001'),
        'n': int_to_base64(numbers.n),
        'e': int_to_base64(numbers.e),
        'alg': 'RS256'
    }
    
    jwks = {'keys': [jwk]}
    
    with open('jwks.json', 'w') as f:
        json.dump(jwks, f, indent=2)
        
    print("JWKS file generated successfully")
