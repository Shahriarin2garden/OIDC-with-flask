#!/usr/bin/env python3
"""
Complete OIDC Flow Test Script
Tests the entire OIDC authorization code flow programmatically
"""

import requests
import base64
import hashlib
import os
from urllib.parse import urlparse, parse_qs

# Configuration
PROVIDER_URL = "http://127.0.0.1:5000"
CLIENT_ID = "client123"
CLIENT_SECRET = "secret123"
REDIRECT_URI = "http://localhost:8080/callback"
SCOPE = "openid profile email"
USERNAME = "alice"
PASSWORD = "alicepassword"

# Generate PKCE values
code_verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')
code_challenge = base64.urlsafe_b64encode(
    hashlib.sha256(code_verifier.encode()).digest()
).rstrip(b'=').decode('utf-8')

print("🚀 Starting OIDC Flow Test")
print(f"Provider: {PROVIDER_URL}")
print(f"Client ID: {CLIENT_ID}")
print(f"User: {USERNAME}")
print(f"Code Challenge: {code_challenge}")
print("=" * 50)

# Use a session to maintain cookies
session = requests.Session()

def test_discovery():
    """Test OIDC discovery endpoint"""
    print("\n📡 Testing Discovery Endpoint...")
    response = session.get(f"{PROVIDER_URL}/.well-known/openid-configuration")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        config = response.json()
        print(f"✅ Discovery successful")
        print(f"   - Issuer: {config.get('issuer')}")
        print(f"   - Authorization Endpoint: {config.get('authorization_endpoint')}")
        print(f"   - Token Endpoint: {config.get('token_endpoint')}")
        return True
    else:
        print(f"❌ Discovery failed: {response.text}")
        return False

def test_jwks():
    """Test JWKS endpoint"""
    print("\n🔑 Testing JWKS Endpoint...")
    response = session.get(f"{PROVIDER_URL}/.well-known/jwks.json")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        jwks = response.json()
        print(f"✅ JWKS successful")
        print(f"   - Keys count: {len(jwks.get('keys', []))}")
        if jwks.get('keys'):
            key = jwks['keys'][0]
            print(f"   - Key ID: {key.get('kid')}")
            print(f"   - Algorithm: {key.get('alg')}")
        return True
    else:
        print(f"❌ JWKS failed: {response.text}")
        return False

def test_authorization():
    """Test authorization endpoint"""
    print("\n🔐 Testing Authorization Flow...")
    
    # Step 1: GET /authorize (should return login form)
    print("Step 1: GET /authorize")
    auth_params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': SCOPE,
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256',
        'state': 'test-state-123'
    }
    
    response = session.get(f"{PROVIDER_URL}/authorize", params=auth_params)
    print(f"Status: {response.status_code}")
    
    if response.status_code != 200:
        print(f"❌ Authorization GET failed: {response.text}")
        return None
    
    if "login.html" not in response.text and "username" not in response.text.lower():
        print(f"❌ Expected login form, got: {response.text[:200]}...")
        return None
    
    print("✅ Login form received")
    
    # Step 2: POST credentials to /authorize
    print("Step 2: POST credentials to /authorize")
    login_data = {
        'username': USERNAME,
        'password': PASSWORD
    }
    
    response = session.post(f"{PROVIDER_URL}/authorize", data=login_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code != 200:
        print(f"❌ Login POST failed: {response.text}")
        return None
        
    if "consent.html" not in response.text and "approve" not in response.text.lower():
        print(f"❌ Expected consent form, got: {response.text[:200]}...")
        return None
    
    print("✅ Consent form received")
    
    # Step 3: POST consent approval to /consent
    print("Step 3: POST consent to /consent")
    consent_data = {
        'action': 'approve'
    }
    
    response = session.post(f"{PROVIDER_URL}/consent", data=consent_data, allow_redirects=False)
    print(f"Status: {response.status_code}")
    
    if response.status_code != 302:
        print(f"❌ Consent POST failed: {response.text}")
        return None
    
    # Extract authorization code from redirect
    location = response.headers.get('Location', '')
    print(f"Redirect location: {location}")
    
    if not location.startswith(REDIRECT_URI):
        print(f"❌ Invalid redirect URI: {location}")
        return None
    
    parsed_url = urlparse(location)
    query_params = parse_qs(parsed_url.query)
    code = query_params.get('code', [None])[0]
    
    if not code:
        print(f"❌ No authorization code in redirect: {location}")
        return None
    
    print(f"✅ Authorization code received: {code[:20]}...")
    return code

def test_token_exchange(auth_code):
    """Test token exchange"""
    print("\n🎫 Testing Token Exchange...")
    
    token_data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code_verifier': code_verifier
    }
    
    response = session.post(f"{PROVIDER_URL}/token", data=token_data)
    print(f"Status: {response.status_code}")
    
    if response.status_code != 200:
        print(f"❌ Token exchange failed: {response.text}")
        return None
    
    try:
        tokens = response.json()
        print("✅ Token exchange successful")
        print(f"   - Access Token: {tokens.get('access_token', '')[:20]}...")
        print(f"   - ID Token: {tokens.get('id_token', '')[:20]}...")
        print(f"   - Token Type: {tokens.get('token_type')}")
        print(f"   - Expires In: {tokens.get('expires_in')}")
        return tokens
    except Exception as e:
        print(f"❌ Token response parse error: {e}")
        print(f"Response text: {response.text}")
        return None

def test_userinfo(access_token):
    """Test UserInfo endpoint"""
    print("\n👤 Testing UserInfo Endpoint...")
    
    headers = {'Authorization': f'Bearer {access_token}'}
    response = session.get(f"{PROVIDER_URL}/userinfo", headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code != 200:
        print(f"❌ UserInfo failed: {response.text}")
        return False
    
    try:
        userinfo = response.json()
        print("✅ UserInfo successful")
        print(f"   - Subject: {userinfo.get('sub')}")
        print(f"   - Name: {userinfo.get('name')}")
        print(f"   - Email: {userinfo.get('email')}")
        return True
    except Exception as e:
        print(f"❌ UserInfo response parse error: {e}")
        return False

def main():
    """Run the complete test suite"""
    print("🧪 OIDC Provider End-to-End Test")
    print("=" * 50)
    
    # Test basic endpoints
    if not test_discovery():
        return False
    
    if not test_jwks():
        return False
    
    # Test authorization flow
    auth_code = test_authorization()
    if not auth_code:
        return False
    
    # Test token exchange
    tokens = test_token_exchange(auth_code)
    if not tokens:
        return False
    
    # Test UserInfo
    access_token = tokens.get('access_token')
    if not access_token:
        print("❌ No access token received")
        return False
    
    if not test_userinfo(access_token):
        return False
    
    print("\n" + "=" * 50)
    print("🎉 ALL TESTS PASSED! OIDC Provider is working correctly.")
    print("✅ Discovery endpoint working")
    print("✅ JWKS endpoint working")  
    print("✅ Authorization flow working")
    print("✅ Token exchange working")
    print("✅ UserInfo endpoint working")
    print("=" * 50)
    
    return True

if __name__ == '__main__':
    try:
        success = main()
        if not success:
            print("\n❌ Some tests failed. Check the logs above.")
            exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Test interrupted by user")
    except Exception as e:
        print(f"\n💥 Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
