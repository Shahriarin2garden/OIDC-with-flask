# tests/test_flow.py
import pytest
from app import app
from models import clients, users

def test_authorization_flow(client):
    # Step 1: GET /authorize
    response = client.get(
        "/authorize",
        query_string={
            "client_id": "client123",
            "redirect_uri": clients["client123"]["redirect_uris"][0],
            "state": "abc",
            "scope": "openid",
            "code_challenge": "testchallenge",
            "code_challenge_method": "plain"
        }
    )
    assert response.status_code == 200
    assert b"Login" in response.data

    # Step 2: POST credentials
    response = client.post(
        "/authorize",
        data={"username": "alice", "password": users["alice"]["password"]}
    )
    assert response.status_code == 200
    assert b"Consent" in response.data

    # Step 3: Consent
    response = client.post(
        "/consent",
        data={"approve": "yes"},
        follow_redirects=False
    )
    assert response.status_code in (302, 303)
    location = response.headers["Location"]
    assert "code=" in location and "state=abc" in location

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
    