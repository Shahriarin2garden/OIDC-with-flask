# Key Generation Instructions

This directory contains cryptographic keys for the OIDC server.

## Files that should be present (but NOT committed to git):
- `private.pem` - RSA private key for signing JWT tokens
- `public.pem` - RSA public key for verifying JWT tokens

## To generate new keys:
Run the following command from the project root:
```bash
python generate_keys.py
```

## Security Notes:
- Never commit private keys to version control
- Keys should be generated in production environments
- Rotate keys regularly for security
- Ensure proper file permissions (600 for private keys)
