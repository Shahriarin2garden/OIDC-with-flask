# 📸 Screenshot Capture Guide

This guide will help you capture all the screenshots needed for the README documentation.

## Prerequisites

1. Make sure the OIDC provider is running: `python app.py`
2. Have a web browser open
3. Install `jq` for JSON formatting: `choco install jq` (Windows) or `brew install jq` (macOS)
4. Have Postman installed with the collection imported

## 🔧 Setup Commands

Before capturing screenshots, run these commands to ensure everything is ready:

```bash
# Start the application
python app.py

# In another terminal, verify endpoints are working
curl http://localhost:5000/.well-known/openid-configuration
curl http://localhost:5000/jwks.json
```

## 📸 Screenshot Capture Instructions

### 1. Discovery Endpoint (`discovery-endpoint.png`)
```bash
# Run this command and capture the terminal output
curl -s http://localhost:5000/.well-known/openid-configuration | jq
```
**Capture**: Terminal window showing the formatted JSON response

### 2. JWKS Endpoint (`jwks-endpoint.png`)
```bash
# Run this command and capture the terminal output
curl -s http://localhost:5000/jwks.json | jq
```
**Capture**: Terminal window showing the JWKS JSON with public keys

### 3. Authorization Request (`authorization-request.png`)
**URL to visit**:
```
http://localhost:5000/authorize?response_type=code&client_id=client123&redirect_uri=http://localhost:8080/callback&scope=openid%20profile%20email&code_challenge=E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM&code_challenge_method=S256&state=test123
```
**Capture**: Browser address bar with the full authorization URL

### 4. Login Form (`login-form.png`)
**Action**: Visit the authorization URL above
**Capture**: The login form page with username/password fields
**Test Credentials**: 
- Username: `alice`
- Password: `password123`

### 5. Consent Form (`consent-form.png`)
**Action**: After logging in successfully
**Capture**: The consent page showing requested scopes and permissions

### 6. Authorization Callback (`auth-callback.png`)
**Action**: After clicking "Allow" on consent page
**Capture**: Browser showing the callback URL with the authorization code parameter

### 7. Token Response (`token-response.png`)
```bash
# Extract the code from the callback URL and run:
curl -X POST http://localhost:5000/token \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=authorization_code' \
  -d 'code=YOUR_AUTH_CODE_HERE' \
  -d 'redirect_uri=http://localhost:8080/callback' \
  -d 'client_id=client123' \
  -d 'client_secret=secret456' \
  -d 'code_verifier=dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk' | jq
```
**Capture**: Terminal showing the complete token response

### 8. UserInfo Response (`userinfo-response.png`)
```bash
# Use the access token from step 7:
curl -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
     http://localhost:5000/userinfo | jq
```
**Capture**: Terminal showing user claims and profile information

### 9. Test Client Interface (`test-client.png`)
```bash
# Run the test client
python test_client.py
```
**Capture**: Terminal showing the test client startup message and authorization URL

### 10. Browser Flow (`browser-flow.png`)
**Action**: When test client opens browser automatically
**Capture**: Browser with the authorization page loaded from test client

### 11. Authentication Success (`auth-success.png`)
**Action**: Complete the test client flow
**Capture**: Browser showing the success page with tokens and user info

### 12. Postman Collection (`postman-collection.png`)
**Action**: Open Postman and import `postman/OIDC_Tests.json`
**Capture**: Postman interface showing the imported OIDC test collection

### 13. cURL Examples (`curl-examples.png`)
```bash
# Show multiple curl commands in one terminal:
echo "=== Discovery Endpoint ==="
curl -s http://localhost:5000/.well-known/openid-configuration | jq .issuer

echo "=== JWKS Endpoint ==="
curl -s http://localhost:5000/jwks.json | jq .keys[0].kty

echo "=== Health Check ==="
curl -s http://localhost:5000/health 2>/dev/null || echo "Endpoint not available"
```
**Capture**: Terminal showing multiple curl commands and their outputs

### 14. Token Introspection (`token-introspection.png`)
```bash
# Use a valid access token:
curl -X POST http://localhost:5000/introspect \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -u 'client123:secret456' \
  -d 'token=YOUR_ACCESS_TOKEN' | jq
```
**Capture**: Terminal showing token introspection response

### 15. Client Registration (`client-registration.png`)
```bash
curl -X POST http://localhost:5000/register \
  -H 'Content-Type: application/json' \
  -d '{
    "client_name": "Test Client",
    "redirect_uris": ["http://localhost:3000/callback"],
    "grant_types": ["authorization_code"],
    "response_types": ["code"],
    "scope": "openid profile email"
  }' | jq
```
**Capture**: Terminal showing client registration request and response

### 16. Health Check (`health-check.png`)
```bash
# If health endpoint exists, otherwise show application status
curl -s http://localhost:5000/health 2>/dev/null || \
curl -s http://localhost:5000/.well-known/openid-configuration | jq '{status: "healthy", issuer: .issuer}'
```
**Capture**: Terminal showing health check response

### 17. Application Logs (`application-logs.png`)
**Action**: While the Flask app is running
**Capture**: Terminal where `python app.py` is running, showing request logs

### 18. Docker Compose (`docker-compose.png`)
```bash
# If using Docker:
docker-compose ps
docker-compose logs --tail=10
```
**Capture**: Terminal showing Docker container status

### 19. Container Status (`container-status.png`)
```bash
# Show system processes:
ps aux | grep python | grep app.py
netstat -tulpn | grep :5000
```
**Capture**: Terminal showing running processes and port status

### 20. Production Deployment (`production-deployment.png`)
```bash
# Show production-ready command:
echo "Production deployment would use:"
echo "gunicorn --bind 0.0.0.0:8000 --workers 4 app:app"
echo "Current development server running on port 5000"
```
**Capture**: Terminal showing deployment information

### 21. Performance Metrics (`performance-metrics.png`)
```bash
# Simple performance test:
time curl -s http://localhost:5000/.well-known/openid-configuration > /dev/null
echo "Response time measurement complete"
```
**Capture**: Terminal showing timing information

### 22. Load Testing (`load-testing.png`)
```bash
# If you have Apache Bench installed:
ab -n 10 -c 2 http://localhost:5000/.well-known/openid-configuration
# Or use curl in a loop:
for i in {1..5}; do
  echo "Request $i:"
  time curl -s http://localhost:5000/.well-known/openid-configuration > /dev/null
done
```
**Capture**: Terminal showing load test results

### 23. Security Logs (`security-logs.png`)
**Action**: While Flask app is running, make several requests
**Capture**: Terminal showing Flask request logs with IP addresses and timestamps

### 24. Error Responses (`error-responses.png`)
```bash
# Generate error responses:
echo "=== Invalid Client ID ==="
curl -s http://localhost:5000/authorize?client_id=invalid | head -5

echo "=== Missing Parameters ==="
curl -s -X POST http://localhost:5000/token | head -5
```
**Capture**: Terminal showing error responses

### 25. Validation Errors (`validation-errors.png`)
```bash
# Test validation:
curl -X POST http://localhost:5000/register \
  -H 'Content-Type: application/json' \
  -d '{"invalid": "data"}' 2>/dev/null || echo "Validation failed as expected"
```
**Capture**: Terminal showing validation error messages

### 26. Rate Limiting (`rate-limiting.png`)
```bash
# Make rapid requests to test rate limiting:
for i in {1..10}; do
  echo "Request $i: $(date)"
  curl -s -o /dev/null -w "%{http_code}\n" http://localhost:5000/.well-known/openid-configuration
  sleep 0.1
done
```
**Capture**: Terminal showing multiple rapid requests

## 📝 Screenshot Best Practices

### Terminal Screenshots
1. Use a dark theme for better contrast
2. Increase font size for readability
3. Clear the terminal before running commands
4. Include the command prompt for context

### Browser Screenshots
1. Use Chrome or Firefox for consistency
2. Open developer tools if showing network requests
3. Zoom to 100% for standard sizing
4. Clear browser cache if needed

### File Naming Convention
Save screenshots with these exact names in `assets/screenshots/`:
- Use lowercase with hyphens
- Match the names in the README exactly
- Use PNG format for best quality

## 🚀 Quick Capture Script

You can create a batch script to capture multiple terminal outputs:

```bash
# save as capture_outputs.sh
#!/bin/bash
mkdir -p outputs

echo "Capturing Discovery Endpoint..."
curl -s http://localhost:5000/.well-known/openid-configuration | jq > outputs/discovery.json

echo "Capturing JWKS..."
curl -s http://localhost:5000/jwks.json | jq > outputs/jwks.json

echo "Testing Client Registration..."
curl -X POST http://localhost:5000/register \
  -H 'Content-Type: application/json' \
  -d '{
    "client_name": "Screenshot Test Client",
    "redirect_uris": ["http://localhost:3000/callback"]
  }' | jq > outputs/registration.json

echo "All outputs saved to outputs/ directory"
echo "Now take screenshots of these files and the terminal outputs"
```

## 📱 Mobile/Responsive Screenshots

If you want to show mobile compatibility:
1. Open browser developer tools
2. Switch to mobile device simulation
3. Refresh the login and consent pages
4. Capture mobile-responsive views

Remember to blur or hide any sensitive information like actual tokens or secrets in your screenshots!
