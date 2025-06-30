# 🔐 Flask OIDC Provider

**A Production-Ready OpenID Connect (OIDC) Provider Built with Flask**

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.1+-green.svg)](https://flask.palletsprojects.com/)
[![OpenID Connect](https://img.shields.io/badge/OpenID%20Connect-1.0-orange.svg)](https://openid.net/connect/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> 🚀 **Get your OIDC provider running in under 5 minutes!**

---

## 📖 Table of Contents

- [🎯 Overview](#-overview)
- [⚡ Quick Start](#-quick-start)
- [🛠️ Installation](#️-installation)
- [🔧 Configuration](#-configuration)
- [📡 API Reference](#-api-reference)
- [🧪 Testing](#-testing)
- [🚀 Deployment](#-deployment)
- [💡 Examples](#-examples)
- [🔒 Security](#-security)
- [🐞 Troubleshooting](#-troubleshooting)
- [🤝 Contributing](#-contributing)

---

## 🎯 Overview

### What is this project?

This repository provides a **complete, production-ready OpenID Connect (OIDC) Provider** built with Python and Flask. Think of it as your own "Login with..." service (like "Login with Google") that you can host and control yourself.

### 🔍 OAuth 2.0 vs OpenID Connect

| Aspect | OAuth 2.0 | OpenID Connect (OIDC) |
|--------|-----------|----------------------|
| **Purpose** | Authorization (What can you do?) | Authentication + Identity (Who are you?) |
| **Token Types** | Access Token | Access Token + ID Token |
| **User Info** | Not standardized | Standardized UserInfo endpoint |
| **Discovery** | Custom implementation | Standardized `.well-known` endpoints |
| **Token Format** | Opaque or JWT | JWT with standard claims |

### 🎨 Real-World Use Cases

<details>
<summary><strong>🏢 Enterprise Single Sign-On (SSO)</strong></summary>

**Scenario**: Company with multiple internal applications  
**Challenge**: Separate login systems for each app  
**Solution**: Single sign-on across all company applications  
**Benefit**: Users login once, access everything securely

</details>

<details>
<summary><strong>🌐 Multi-Platform Customer Experience</strong></summary>

**Scenario**: Platform with web app, mobile app, and APIs  
**Challenge**: Consistent authentication across platforms  
**Solution**: Unified identity provider for all touchpoints  
**Benefit**: Seamless user experience with centralized control

</details>

<details>
<summary><strong>🔌 Third-Party Integrations</strong></summary>

**Scenario**: Enable other developers to build integrations  
**Challenge**: Secure access without sharing credentials  
**Solution**: OAuth 2.0 flows with controlled permissions  
**Benefit**: Ecosystem growth with maintained security

</details>

### 🏗️ Architecture Overview

![OIDC Architecture](https://github.com/Shahriarin2garden/OIDC-with-flask/blob/d91dd896f3f679398d9e995dcbd1b5f9c1c57804/assets/Untitled%20Diagram.drawio%20(7).png)

**Authentication Flow:**
1. **User Request** → App redirects to OIDC Provider
2. **User Login** → Credentials validated securely  
3. **Authorization** → User grants permissions
4. **Token Issuance** → Secure JWT tokens generated
5. **Resource Access** → Tokens used for API calls

---

## ⚡ Quick Start

### Option 1: Automated Setup (Recommended)

#### Linux/WSL/macOS
```bash
git clone https://github.com/Shahriarin2garden/OIDC-with-flask
cd OIDC-with-flask

# Automated setup
chmod +x setup.sh
./setup.sh

# Start the provider
python app.py
```

#### Windows PowerShell
```powershell
git clone https://github.com/Shahriarin2garden/OIDC-with-flask
cd OIDC-with-flask

# Setup environment
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
python generate_keys.py

# Start the provider
python app.py
```

### Option 2: Docker (One Command)
```bash
# Start with Docker Compose
docker-compose up --build

# Or just the basics
docker build -t oidc-provider .
docker run -p 5000:5000 oidc-provider
```

### ✅ Verify Installation
```bash
# Test the provider is running
curl http://localhost:5000/.well-known/openid-configuration

# Check health status
curl http://localhost:5000/health
```

**Expected Output:**
```json
{
  "issuer": "http://localhost:5000",
  "authorization_endpoint": "http://localhost:5000/authorize",
  "token_endpoint": "http://localhost:5000/token",
  "userinfo_endpoint": "http://localhost:5000/userinfo",
  "jwks_uri": "http://localhost:5000/jwks.json"
}
```

---

## 🛠️ Installation

### Prerequisites

| Requirement | Version | Installation |
|-------------|---------|--------------|
| **Python** | 3.8+ | [Download Python](https://www.python.org/downloads/) |
| **Redis** (Optional) | 6.0+ | [Redis Installation](https://redis.io/download) |
| **Docker** (Optional) | 20.0+ | [Docker Installation](https://docs.docker.com/get-docker/) |

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Shahriarin2garden/OIDC-with-flask
   cd OIDC-with-flask
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Activate (Linux/macOS)
   source venv/bin/activate
   
   # Activate (Windows)
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Generate RSA keys**
   ```bash
   python generate_keys.py
   ```

5. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following configuration:

```bash
# Application Settings
FLASK_ENV=development
SECRET_KEY=your-super-secret-key-change-me
ISSUER_URL=http://localhost:5000

# Security Keys
PRIVATE_KEY_PATH=keys/private.pem
PUBLIC_KEY_PATH=keys/public.pem

# Storage Backend (Optional)
REDIS_URL=redis://localhost:6379/0

# Security Options
RATE_LIMITING_ENABLED=true
CORS_ENABLED=false
SSL_REQUIRED=false
```

### Key Generation

```bash
# Generate RSA key pair (2048-bit)
python generate_keys.py

# Or manually with OpenSSL
openssl genrsa -out keys/private.pem 2048
openssl rsa -in keys/private.pem -pubout -out keys/public.pem

# Generate JWKS
python generate_jwks.py
```

### Storage Options

#### In-Memory (Default)
- Fast startup, ideal for development
- No persistence across restarts
- No additional dependencies

#### Redis Backend
- Persistent storage for tokens and sessions
- Scalable for production workloads
- Requires Redis server

```bash
# Start Redis with Docker
docker run -p 6379:6379 redis:7-alpine

# Or install locally
# Ubuntu/Debian: sudo apt install redis-server
# macOS: brew install redis
# Windows: Download from https://redis.io/download
```

### Starting the Server

#### Development Mode
```bash
# With in-memory storage
python app.py

# With Redis backend
export REDIS_URL=redis://localhost:6379/0
python app.py

# With Flask dev server
flask run --host=0.0.0.0 --port=5000
```

#### Production Mode
```bash
# With Gunicorn
gunicorn --bind 0.0.0.0:8000 --workers 4 app:app

# With Docker Compose
docker-compose up -d
```

---

## 📡 API Reference

### Core Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| `GET` | `/.well-known/openid-configuration` | OIDC discovery metadata | None |
| `GET` | `/jwks.json` | JSON Web Key Set | None |
| `POST` | `/register` | Dynamic client registration | None |
| `GET` | `/authorize` | Authorization endpoint | None |
| `POST` | `/token` | Token endpoint | Client Auth |
| `GET` | `/userinfo` | User information | Bearer Token |
| `POST` | `/introspect` | Token introspection | Client Auth |
| `POST` | `/revoke` | Token revocation | Client Auth |

### Client Registration

Register a new client application:

```bash
curl -X POST http://localhost:5000/register \
  -H 'Content-Type: application/json' \
  -d '{
    "client_name": "My App",
    "redirect_uris": ["http://localhost:3000/callback"],
    "grant_types": ["authorization_code"],
    "response_types": ["code"],
    "scope": "openid profile email"
  }'
```

**Response:**
```json
{
  "client_id": "abc123",
  "client_secret": "secret456",
  "redirect_uris": ["http://localhost:3000/callback"],
  "grant_types": ["authorization_code"],
  "response_types": ["code"]
}
```

### Authorization Code Flow with PKCE

#### Step 1: Generate PKCE Values
```python
import base64, hashlib, secrets

# Generate code verifier
verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode().rstrip('=')

# Generate code challenge
challenge = base64.urlsafe_b64encode(
    hashlib.sha256(verifier.encode()).digest()
).decode().rstrip('=')

print(f"Code Verifier: {verifier}")
print(f"Code Challenge: {challenge}")
```

#### Step 2: Authorization Request
```bash
# Redirect user to this URL
http://localhost:5000/authorize?response_type=code&client_id=abc123&redirect_uri=http://localhost:3000/callback&scope=openid%20profile%20email&code_challenge=YOUR_CHALLENGE&code_challenge_method=S256&state=random123
```

#### Step 3: Exchange Code for Tokens
```bash
curl -X POST http://localhost:5000/token \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=authorization_code' \
  -d 'code=AUTHORIZATION_CODE' \
  -d 'redirect_uri=http://localhost:3000/callback' \
  -d 'client_id=abc123' \
  -d 'client_secret=secret456' \
  -d 'code_verifier=YOUR_VERIFIER'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "id_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "def456",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

#### Step 4: Access User Information
```bash
curl -H 'Authorization: Bearer YOUR_ACCESS_TOKEN' \
     http://localhost:5000/userinfo
```

**Response:**
```json
{
  "sub": "user-123",
  "email": "user@example.com",
  "name": "John Doe",
  "email_verified": true
}
```

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest -v

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test categories
pytest tests/test_flow.py -v           # OIDC flow tests
pytest tests/test_security.py -v       # Security tests  
pytest tests/test_endpoints.py -v      # API endpoint tests
```

### Interactive Test Client

```bash
# Use the built-in test client
python test_client.py

# Follow the prompts to test the complete OIDC flow
```

### Manual Testing with Postman

1. Import the collection: `postman/OIDC_Tests.json`
2. Set environment variables:
   - `base_url`: `http://localhost:5000`
   - `client_id`: Your registered client ID
   - `client_secret`: Your client secret
3. Run the test collection

### Health Check

```bash
# Basic health check
curl http://localhost:5000/health

# Detailed status
curl http://localhost:5000/metrics
```

---

## 🚀 Deployment

### Production Checklist

- [ ] **Security Keys**: Generate strong RSA keys (2048-bit minimum)
- [ ] **Environment Variables**: Set production values in `.env`
- [ ] **Redis**: Configure persistent Redis instance
- [ ] **SSL/TLS**: Enable HTTPS with valid certificates
- [ ] **Rate Limiting**: Enable request rate limiting
- [ ] **Monitoring**: Set up logging and monitoring
- [ ] **Backup**: Configure key and data backup

### Docker Deployment

#### Simple Docker Run
```bash
docker build -t oidc-provider .
docker run -p 5000:5000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-production-secret \
  -e REDIS_URL=redis://redis:6379/0 \
  oidc-provider
```

#### Docker Compose (Recommended)
```yaml
version: '3.8'
services:
  oidc-provider:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  redis_data:
```

```bash
# Start production deployment
docker-compose up -d

# View logs
docker-compose logs -f oidc-provider
```

### Kubernetes Deployment

<details>
<summary><strong>Kubernetes Manifests</strong></summary>

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: oidc-provider
spec:
  replicas: 3
  selector:
    matchLabels:
      app: oidc-provider
  template:
    metadata:
      labels:
        app: oidc-provider
    spec:
      containers:
      - name: oidc-provider
        image: oidc-provider:latest
        ports:
        - containerPort: 5000
        env:
        - name: FLASK_ENV
          value: "production"
        - name: SECRET_KEY
          valueFrom:
            secretKeyRef:
              name: oidc-secrets
              key: secret-key
        - name: REDIS_URL
          value: "redis://redis-service:6379/0"

---
apiVersion: v1
kind: Service
metadata:
  name: oidc-provider-service
spec:
  selector:
    app: oidc-provider
  ports:
  - port: 80
    targetPort: 5000
  type: LoadBalancer
```

```bash
kubectl apply -f deployment.yaml
```

</details>

### Load Balancer Configuration

#### Nginx Configuration
```nginx
server {
    listen 443 ssl http2;
    server_name oidc.example.com;
    
    ssl_certificate /etc/ssl/certs/oidc.crt;
    ssl_certificate_key /etc/ssl/private/oidc.key;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # WebSocket support (if needed)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

---

## 💡 Examples

### Python Client Example

```python
import requests
import base64
import hashlib
import secrets
import webbrowser
from urllib.parse import urlencode

class OIDCClient:
    def __init__(self, provider_url, client_id, client_secret, redirect_uri):
        self.provider_url = provider_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.code_verifier = None
        self.code_challenge = None
    
    def generate_pkce(self):
        """Generate PKCE code verifier and challenge"""
        self.code_verifier = base64.urlsafe_b64encode(
            secrets.token_bytes(32)
        ).decode().rstrip('=')
        
        self.code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(self.code_verifier.encode()).digest()
        ).decode().rstrip('=')
        
        return self.code_verifier, self.code_challenge
    
    def get_authorization_url(self, scope="openid profile email", state="random123"):
        """Generate authorization URL"""
        self.generate_pkce()
        
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': scope,
            'code_challenge': self.code_challenge,
            'code_challenge_method': 'S256',
            'state': state
        }
        
        return f"{self.provider_url}/authorize?{urlencode(params)}"
    
    def exchange_code_for_tokens(self, authorization_code):
        """Exchange authorization code for tokens"""
        data = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code_verifier': self.code_verifier
        }
        
        response = requests.post(f"{self.provider_url}/token", data=data)
        return response.json()
    
    def get_user_info(self, access_token):
        """Get user information using access token"""
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(f"{self.provider_url}/userinfo", headers=headers)
        return response.json()

# Usage example
client = OIDCClient(
    'http://localhost:5000',
    'your-client-id',
    'your-client-secret',
    'http://localhost:8080/callback'
)

# Get authorization URL and open in browser
auth_url = client.get_authorization_url()
print(f"Visit this URL: {auth_url}")
webbrowser.open(auth_url)

# After getting the code from callback, exchange for tokens
code = input("Enter the authorization code from callback: ")
tokens = client.exchange_code_for_tokens(code)
user_info = client.get_user_info(tokens['access_token'])

print("Tokens:", tokens)
print("User Info:", user_info)
```

### JavaScript/Node.js Example

```javascript
const crypto = require('crypto');
const querystring = require('querystring');

class OIDCClient {
    constructor(providerUrl, clientId, clientSecret, redirectUri) {
        this.providerUrl = providerUrl;
        this.clientId = clientId;
        this.clientSecret = clientSecret;
        this.redirectUri = redirectUri;
    }

    generatePKCE() {
        const codeVerifier = crypto.randomBytes(32).toString('base64url');
        const codeChallenge = crypto
            .createHash('sha256')
            .update(codeVerifier)
            .digest('base64url');
        
        return { codeVerifier, codeChallenge };
    }

    getAuthorizationUrl(scope = 'openid profile email', state = 'random123') {
        const { codeVerifier, codeChallenge } = this.generatePKCE();
        this.codeVerifier = codeVerifier;

        const params = querystring.stringify({
            response_type: 'code',
            client_id: this.clientId,
            redirect_uri: this.redirectUri,
            scope: scope,
            code_challenge: codeChallenge,
            code_challenge_method: 'S256',
            state: state
        });

        return `${this.providerUrl}/authorize?${params}`;
    }

    async exchangeCodeForTokens(authorizationCode) {
        const data = querystring.stringify({
            grant_type: 'authorization_code',
            code: authorizationCode,
            redirect_uri: this.redirectUri,
            client_id: this.clientId,
            client_secret: this.clientSecret,
            code_verifier: this.codeVerifier
        });

        const response = await fetch(`${this.providerUrl}/token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: data
        });

        return await response.json();
    }

    async getUserInfo(accessToken) {
        const response = await fetch(`${this.providerUrl}/userinfo`, {
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });

        return await response.json();
    }
}

// Usage
const client = new OIDCClient(
    'http://localhost:5000',
    'your-client-id',
    'your-client-secret',
    'http://localhost:8080/callback'
);

console.log('Authorization URL:', client.getAuthorizationUrl());
```

### React Integration Example

```jsx
import React, { useState, useEffect } from 'react';

const OIDCProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    const config = {
        authority: 'http://localhost:5000',
        client_id: 'your-client-id',
        redirect_uri: window.location.origin + '/callback',
        scope: 'openid profile email',
        response_type: 'code'
    };

    const login = () => {
        // Generate PKCE values
        const codeVerifier = generateCodeVerifier();
        const codeChallenge = generateCodeChallenge(codeVerifier);
        
        // Store verifier in sessionStorage
        sessionStorage.setItem('code_verifier', codeVerifier);
        
        // Build authorization URL
        const params = new URLSearchParams({
            response_type: config.response_type,
            client_id: config.client_id,
            redirect_uri: config.redirect_uri,
            scope: config.scope,
            code_challenge: codeChallenge,
            code_challenge_method: 'S256',
            state: 'random-state'
        });

        window.location.href = `${config.authority}/authorize?${params}`;
    };

    const logout = () => {
        setUser(null);
        sessionStorage.clear();
    };

    const generateCodeVerifier = () => {
        const array = new Uint8Array(32);
        crypto.getRandomValues(array);
        return btoa(String.fromCharCode(...array))
            .replace(/\+/g, '-')
            .replace(/\//g, '_')
            .replace(/=/g, '');
    };

    const generateCodeChallenge = (verifier) => {
        const encoder = new TextEncoder();
        const data = encoder.encode(verifier);
        return crypto.subtle.digest('SHA-256', data).then(hash => {
            return btoa(String.fromCharCode(...new Uint8Array(hash)))
                .replace(/\+/g, '-')
                .replace(/\//g, '_')
                .replace(/=/g, '');
        });
    };

    return (
        <div>
            {user ? (
                <div>
                    <h1>Welcome, {user.name}!</h1>
                    <button onClick={logout}>Logout</button>
                    {children}
                </div>
            ) : (
                <div>
                    <h1>Please log in</h1>
                    <button onClick={login}>Login</button>
                </div>
            )}
        </div>
    );
};

export default OIDCProvider;
```

---

## 🔒 Security

### Security Features

- ✅ **PKCE (RFC 7636)**: Prevents authorization code interception attacks
- ✅ **RS256 JWT Signing**: RSA-based token signing with public key verification
- ✅ **Rate Limiting**: Protection against brute force attacks
- ✅ **CORS Protection**: Configurable cross-origin resource sharing
- ✅ **CSRF Protection**: Cross-site request forgery prevention
- ✅ **Input Validation**: Comprehensive parameter validation
- ✅ **Secure Headers**: Security-focused HTTP headers

### Security Best Practices

#### Key Management
```bash
# Generate strong RSA keys (minimum 2048-bit)
openssl genrsa -out keys/private.pem 2048

# Set proper file permissions
chmod 600 keys/private.pem
chmod 644 keys/public.pem

# Never commit private keys to version control
echo "keys/private.pem" >> .gitignore
```

#### Environment Security
```bash
# Use strong, random secret keys
export SECRET_KEY=$(openssl rand -hex 32)

# Secure Redis connection in production
export REDIS_URL=rediss://username:password@redis-server:6380/0

# Enable SSL/TLS in production
export SSL_REQUIRED=true
```

#### Production Configuration
```bash
# .env.production
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=${VAULT_SECRET_KEY}
REDIS_URL=rediss://redis-cluster:6380/0
SSL_REQUIRED=true
RATE_LIMITING_ENABLED=true
CORS_ENABLED=false
```

### Token Security

#### JWT Token Structure
```json
{
  "header": {
    "alg": "RS256",
    "typ": "JWT",
    "kid": "2025-06-28-001"
  },
  "payload": {
    "iss": "http://localhost:5000",
    "sub": "user-123",
    "aud": "client-abc",
    "exp": 1719849600,
    "iat": 1719846000,
    "email": "user@example.com",
    "email_verified": true
  }
}
```

#### Token Validation
```python
import jwt
from cryptography.hazmat.primitives import serialization

# Load public key
with open('keys/public.pem', 'rb') as f:
    public_key = serialization.load_pem_public_key(f.read())

# Validate token
try:
    payload = jwt.decode(
        token,
        public_key,
        algorithms=['RS256'],
        audience='your-client-id',
        issuer='http://localhost:5000'
    )
    print("Token is valid:", payload)
except jwt.InvalidTokenError as e:
    print("Token is invalid:", e)
```

---

## 🐞 Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Error: Address already in use: Port 5000
# Solution: Kill existing process or use different port
lsof -ti:5000 | xargs kill -9
# Or
python app.py --port 5001
```

#### 2. Redis Connection Failed
```bash
# Error: Redis connection refused
# Solution: Start Redis server
docker run -p 6379:6379 redis:7-alpine
# Or
redis-server
```

#### 3. Invalid JWT Signature
```bash
# Error: JWT signature verification failed
# Solution: Regenerate keys or check key paths
python generate_keys.py
# Check .env file for correct key paths
```

#### 4. CORS Issues
```javascript
// Error: CORS policy blocks request
// Solution: Enable CORS in .env
CORS_ENABLED=true
// Or add specific origins
CORS_ORIGINS=http://localhost:3000,https://myapp.com
```

### Debug Mode

```bash
# Enable debug logging
export FLASK_DEBUG=1
export LOG_LEVEL=DEBUG

# Start with verbose output
python app.py --debug
```

### Health Checks

```bash
# Check service status
curl http://localhost:5000/health

# Verify all endpoints
endpoints=(
    "/.well-known/openid-configuration"
    "/jwks.json"
    "/health"
)

for endpoint in "${endpoints[@]}"; do
    echo "Testing $endpoint..."
    curl -s -o /dev/null -w "%{http_code}" "http://localhost:5000$endpoint"
    echo
done
```

### Log Analysis

```bash
# View application logs
tail -f app.log

# Filter for errors
grep "ERROR" app.log

# Monitor authentication events
grep "token_issued\|auth_request" app.log
```

---

## 🤝 Contributing

### Development Setup

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set up development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Make your changes**

5. **Run tests**
   ```bash
   pytest -v
   black .  # Code formatting
   flake8 .  # Linting
   ```

6. **Submit a pull request**

### Code Style

- **Python**: Follow PEP 8, use Black for formatting
- **Documentation**: Update README.md for new features
- **Tests**: Add tests for new functionality
- **Commits**: Use conventional commit messages

### Project Structure

```
OIDC-with-flask/
├── app.py                    # Main Flask application
├── config.py                 # Configuration management
├── models.py                 # Data models
├── requirements.txt          # Python dependencies
├── auth/                     # Authentication modules
│   ├── client_auth.py       # Client authentication
│   ├── pkce.py              # PKCE utilities
│   ├── registration.py      # Client registration
│   └── token.py             # Token management
├── templates/                # HTML templates
├── static/                   # Static assets
├── tests/                    # Test suite
├── keys/                     # RSA keys (not in git)
└── docs/                     # Documentation
```

### Reporting Issues

When reporting issues, please include:
- Python version
- Operating system
- Steps to reproduce
- Error messages/logs
- Expected vs actual behavior

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **OpenID Foundation** for the OpenID Connect specification
- **OAuth Working Group** for OAuth 2.0 standards
- **Flask Community** for the excellent web framework
- **Contributors** who helped improve this project

---

## 📞 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/Shahriarin2garden/OIDC-with-flask/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/Shahriarin2garden/OIDC-with-flask/discussions)
- 📖 **Documentation**: [Project Wiki](https://github.com/Shahriarin2garden/OIDC-with-flask/wiki)
- 📧 **Email**: For sensitive security issues

---

<div align="center">

**🌟 If this project helped you, please consider giving it a star! 🌟**

Made with ❤️ by the OIDC Flask community

</div>
