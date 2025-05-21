# flask-oidc-provider/config.py

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-production")
    DEBUG = os.environ.get("FLASK_DEBUG", False)

    # Key locations
    PRIVATE_KEY_PATH = os.path.join(basedir, "private.pem")
    PUBLIC_KEY_PATH = os.path.join(basedir, "public.pem")
    JWKS_PATH = os.path.join(basedir, "jwks.json")

    @classmethod
    def load_private_key(cls):
        try:
            with open(cls.PRIVATE_KEY_PATH, "rb") as f:
                return f.read()
        except FileNotFoundError:
            raise RuntimeError("Private key not found at expected path.")

    @classmethod
    def load_public_key(cls):
        try:
            with open(cls.PUBLIC_KEY_PATH, "rb") as f:
                return f.read()
        except FileNotFoundError:
            raise RuntimeError("Public key not found at expected path.")

    @classmethod
    def load_jwks(cls):
        try:
            with open(cls.JWKS_PATH, "r") as f:
                return f.read()
        except FileNotFoundError:
            raise RuntimeError("JWKS file not found at expected path.")
