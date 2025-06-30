#!/usr/bin/env python3
"""
Direct test of the login functionality
"""

import requests

def test_login_direct():
    """Test the login endpoint directly"""
    print("Testing direct login functionality...")
    
    # First, get the authorization page to establish a session
    auth_url = "http://127.0.0.1:5000/authorize"
    params = {
        "response_type": "code",
        "client_id": "client123",
        "redirect_uri": "http://localhost:8080/callback",
        "scope": "openid profile email",
        "code_challenge": "test_challenge",
        "code_challenge_method": "S256"
    }
    
    session = requests.Session()
    
    # Get the login page
    print("1. Getting authorization page...")
    response = session.get(auth_url, params=params)
    print(f"   Status: {response.status_code}")
    print(f"   Response length: {len(response.text)}")
    
    # Now submit login credentials
    print("2. Submitting login credentials...")
    login_data = {
        "username": "alice",
        "password": "alicepassword"
    }
    
    response = session.post(auth_url, data=login_data, params=params)
    print(f"   Status: {response.status_code}")
    print(f"   Response length: {len(response.text)}")
    
    if response.status_code == 200:
        if "consent" in response.text.lower():
            print("   ✅ Login successful! Consent page returned.")
        elif "login" in response.text.lower():
            print("   ❌ Login failed. Still showing login page.")
        else:
            print(f"   Unknown response: {response.text[:200]}...")
    else:
        print(f"   ❌ Login failed with status {response.status_code}")
        try:
            error_data = response.json()
            print(f"   Error: {error_data}")
        except:
            print(f"   Response: {response.text[:200]}...")

if __name__ == "__main__":
    test_login_direct()
