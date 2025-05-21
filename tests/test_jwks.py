# tests/test_jwks.py
import json
import pytest
from app import app

# Pytest fixture to provide a test client for the Flask app
@pytest.fixture
def client():
    app.config["TESTING"] = True  # Enable testing mode
    with app.test_client() as client:
        print("Creating test client")
        yield client  # Provide the client to the test

# Test case for the JWKS (JSON Web Key Set) endpoint
def test_jwks_endpoint(client):
    print("Sending GET request to /.well-known/jwks.json")
    response = client.get("/.well-known/jwks.json")  # Send GET request to JWKS endpoint
    print(f"Received response with status code: {response.status_code}")
    assert response.status_code == 200  # Ensure response status is OK

    data = json.loads(response.data)  # Parse JSON response
    print(f"Parsed JSON data: {data}")
    assert "keys" in data and isinstance(data["keys"], list)  # Check 'keys' exists and is a list

    for key in data["keys"]:
        print(f"Checking key: {key}")
        assert key.get("kty") == "RSA"  # Key type must be RSA
        assert key.get("kid") is not None  # Key ID must be present
        assert key.get("alg") == "RS256"  # Algorithm must be RS256
        assert key.get("n") and key.get("e")  # Public modulus and exponent must be present
        assert isinstance(key["n"], str) and isinstance(key["e"], str)
        # Ensure 'n' and 'e' are strings