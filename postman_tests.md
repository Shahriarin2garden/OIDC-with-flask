# OIDC Provider Postman Test Guide

## Environment Setup

Create a new Postman environment with these variables:

```
BASE_URL: http://localhost:5000
CLIENT_ID: (will be obtained during registration)
CLIENT_SECRET: (will be obtained during registration)
AUTH_CODE: (will be populated during auth flow)
ACCESS_TOKEN: (will be populated after token exchange)
REFRESH_TOKEN: (will be populated after token exchange)
CODE_VERIFIER: (will be generated for PKCE)
CODE_CHALLENGE: (will be generated from CODE_VERIFIER)
REDIRECT_URI: http://localhost:3000/callback
```

## Test Sequence

### 1. Discovery Endpoint
```http
GET {{BASE_URL}}/.well-known/openid-configuration
```
**Test**: Verify that all required endpoints are present in the response.

### 2. JWKS Endpoint
```http
GET {{BASE_URL}}/.well-known/jwks.json
```
**Test**: Verify that RSA public key information is present.

### 3. Dynamic Client Registration
```http
POST {{BASE_URL}}/register
Content-Type: application/json

{
    "client_name": "postman-test-client",
    "redirect_uris": ["http://localhost:3000/callback"],
    "grant_types": ["authorization_code", "refresh_token"],
    "response_types": ["code"],
    "scope": "openid profile email"
}
```
**Tests**:
```javascript
var jsonData = pm.response.json();
pm.environment.set("CLIENT_ID", jsonData.client_id);
pm.environment.set("CLIENT_SECRET", jsonData.client_secret);
```

### 4. Generate PKCE Values
You'll need to generate these values using a tool. Here's a Python script to generate them:

```python
import base64
import hashlib
import secrets

code_verifier = secrets.token_urlsafe(32)
code_challenge = base64.urlsafe_b64encode(
    hashlib.sha256(code_verifier.encode()).digest()
).decode().rstrip('=')

print(f"Code Verifier: {code_verifier}")
print(f"Code Challenge: {code_challenge}")
```

Set these values in your Postman environment.

### 5. Authorization Request
```http
GET {{BASE_URL}}/authorize?
    response_type=code&
    client_id={{CLIENT_ID}}&
    redirect_uri={{REDIRECT_URI}}&
    scope=openid%20email%20profile&
    code_challenge={{CODE_CHALLENGE}}&
    code_challenge_method=S256
```
**Note**: This will redirect to the login page. After logging in and consenting, capture the authorization code from the redirect URL and set it to the AUTH_CODE environment variable.

### 6. Token Exchange
```http
POST {{BASE_URL}}/token
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code&
code={{AUTH_CODE}}&
redirect_uri={{REDIRECT_URI}}&
client_id={{CLIENT_ID}}&
code_verifier={{CODE_VERIFIER}}
```
**Tests**:
```javascript
var jsonData = pm.response.json();
pm.environment.set("ACCESS_TOKEN", jsonData.access_token);
pm.environment.set("REFRESH_TOKEN", jsonData.refresh_token);
```

### 7. UserInfo Endpoint
```http
GET {{BASE_URL}}/userinfo
Authorization: Bearer {{ACCESS_TOKEN}}
```

### 8. Token Introspection
```http
POST {{BASE_URL}}/introspect
Authorization: Basic {{base64(CLIENT_ID + ":" + CLIENT_SECRET)}}
Content-Type: application/x-www-form-urlencoded

token={{ACCESS_TOKEN}}
```

### 9. Refresh Token
```http
POST {{BASE_URL}}/token
Content-Type: application/x-www-form-urlencoded
Authorization: Basic {{base64(CLIENT_ID + ":" + CLIENT_SECRET)}}

grant_type=refresh_token&
refresh_token={{REFRESH_TOKEN}}
```

### 10. Token Revocation
```http
POST {{BASE_URL}}/revoke
Authorization: Basic {{base64(CLIENT_ID + ":" + CLIENT_SECRET)}}
Content-Type: application/x-www-form-urlencoded

token={{REFRESH_TOKEN}}
```

## Test Flow Automation

1. Create a new Postman Collection
2. Import all the above requests
3. Set up collection-level variables
4. Use the "Tests" tab in each request to:
   - Validate response status codes
   - Extract and set environment variables
   - Verify response payload structure
   - Check token validity and claims

## Example Test Scripts

### Response Status Validation
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});
```

### Token Response Validation
```javascript
pm.test("Token response structure is valid", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('access_token');
    pm.expect(jsonData).to.have.property('token_type', 'Bearer');
    pm.expect(jsonData).to.have.property('expires_in');
});
```

### UserInfo Response Validation
```javascript
pm.test("UserInfo contains required claims", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('sub');
    pm.expect(jsonData).to.have.property('email');
    pm.expect(jsonData).to.have.property('email_verified');
});
```

## Test Users

For testing, use these credentials:
```
Username: user1
Password: password1
```

## Error Cases to Test

1. Invalid client credentials
2. Invalid authorization code
3. Invalid PKCE verifier
4. Expired tokens
5. Invalid scopes
6. Invalid redirect URIs

## Security Testing

1. **PKCE Verification**
   - Try to exchange code without code_verifier
   - Try with incorrect code_verifier

2. **Token Security**
   - Verify token signature
   - Check token expiration
   - Validate token claims

3. **Client Authentication**
   - Test with invalid client credentials
   - Test with missing client authentication

## Troubleshooting

If you encounter issues:

1. Check environment variables are set correctly
2. Verify the server is running (`flask run --host=0.0.0.0 --port=5000`)
3. Ensure Redis is running if using Redis backend
4. Check server logs for detailed error messages

## Postman Collection Export

You can export this collection and environment after setting it up by:
1. Click on Collection menu (...)
2. Export
3. Save as JSON file

This will allow others to import and run the same tests.
