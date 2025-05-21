# flask-oidc-provider/config.py

import os

class Config:
    # WARNING: Change the secret key in production! Never use the default.
    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY environment variable is not set. This is required for production!")

    PRIVATE_KEY_PATH = os.environ.get("PRIVATE_KEY_PATH", "./private.pem")
    PUBLIC_KEY_PATH = os.environ.get("PUBLIC_KEY_PATH", "./public.pem")
    ISSUER_URL = os.environ.get("ISSUER_URL", "http://localhost:5000")

    # Token expiry times in seconds
    TOKEN_EXPIRY = int(os.environ.get("TOKEN_EXPIRY", 3600))
    REFRESH_TOKEN_EXPIRY = int(os.environ.get("REFRESH_TOKEN_EXPIRY", 86400))

    @classmethod
    def load_private_key(cls):
        try:
            with open(cls.PRIVATE_KEY_PATH, "r") as f:
                return f.read()
        except FileNotFoundError:
            raise RuntimeError(f"Private key file not found at {cls.PRIVATE_KEY_PATH}")
        except Exception as e:
            raise RuntimeError(f"Error loading private key: {e}")

    @classmethod
    def load_public_key(cls):
        try:
            with open(cls.PUBLIC_KEY_PATH, "r") as f:
                return f.read()
        except FileNotFoundError:
            raise RuntimeError(f"Public key file not found at {cls.PUBLIC_KEY_PATH}")
        except Exception as e:
            raise RuntimeError(f"Error loading public key: {e}")
#     if not verify_pkce(code_verifier, record["code_challenge"], record["code_challenge_method"]):