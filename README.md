# Flask OIDC Provider

A **minimal**, **production-ready** OpenID Connect (OIDC) provider built with Flask. Offers out-of-the-box support for:

- ✅ Authorization Code Flow
- ✅ Client Credentials & Resource Owner Password grants
- ✅ Dynamic JWKs publishing
- ✅ UserInfo endpoint

---

## 📂 Repository Structure

```text
flask-oidc-provider/
├── app.py             # Application entrypoint & routes
├── config.py          # Settings & RSA key loading
├── models.py          # In-memory store & helper functions
├── jwks.json          # Public JWKs
├── requirements.txt   # Python dependencies
├── Dockerfile         # Docker image build file
├── docker-compose.yml # Docker service orchestrator
├── templates/         # HTML views
│   ├── login.html
│   └── consent.html
└── README.md          # This document
```

---

## 📖 Table of Contents

1. [Features](#features)
2. [Getting Started](#getting-started)
3. [Configuration](#configuration)
4. [Running the Provider](#running-the-provider)
5. [Endpoints & Flows](#endpoints--flows)
6. [API Call Examples](#api-call-examples)
7. [Docker Support](#docker-support)
8. [Testing](#testing)
9. [Contributing](#contributing)
10. [License](#license)

---

## 🚀 Features

- **OIDC Discovery**: Auto-generated `.well-known/openid-configuration`
- **JWKS Rotation**: Serve public keys via `/jwks`
- **Authentication**: Login & consent screens
- **Token Generation**: Access & ID tokens (RS256)
- **Scopes**: `openid`, `email`, `profile`
- **Storage**: Simple in-memory storage (easily swappable)

---

## 🛠 Getting Started

```bash
# Clone
git clone https://github.com/your-org/flask-oidc-provider.git
cd flask-oidc-provider

# Create virtualenv & install
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 🔑 Generate RSA Key Pair

```bash
openssl genrsa -out private.pem 2048
openssl rsa -in private.pem -pubout -out public.pem
```

### 🔨 Build JWKS

```bash
python3 - << 'EOF'
import json, jwt
from jwt.utils import base64url_encode
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

key = serialization.load_pem_public_key(open('public.pem','rb').read(), default_backend())
nums = key.public_numbers()
n_b64 = base64url_encode(nums.n.to_bytes((nums.n.bit_length()+7)//8, 'big')).decode()
e_b64 = base64url_encode(nums.e.to_bytes((nums.e.bit_length()+7)//8, 'big')).decode()

jwks = {'keys': [{ 'kty':'RSA','use':'sig','kid':'1','alg':'RS256','n':n_b64,'e':e_b64 }]}
print(json.dumps(jwks, indent=2))
EOF > jwks.json
```

---

## ▶️ Running the Provider

```bash
export FLASK_ENV=production
python app.py
```

Access discovery at `http://localhost:5000/.well-known/openid-configuration`

---

## 🔗 Endpoints & Flows

### 1. Discovery
- `GET /.well-known/openid-configuration`

### 2. JWKS
- `GET /jwks`

### 3. Authorization Code
1. `GET /authorize?response_type=code&client_id={CLIENT_ID}&redirect_uri={URI}&scope=openid email profile&state=xyz`
2. Login → Consent → Redirect with `code`

### 4. Token Exchange
- `POST /token` with form data: `grant_type`, `client_id`, `client_secret`, `code`, `redirect_uri`

### 5. UserInfo
- `GET /userinfo` with `Authorization: Bearer {ACCESS_TOKEN}`

---

## 📡 API Call Examples

### 1. Authorization Request (Browser)
```http
GET /authorize?response_type=code&client_id=client123&redirect_uri=http://localhost:8000/callback&scope=openid%20email%20profile&state=abc123
```

### 2. Token Request (cURL)
```bash
curl -X POST http://localhost:5000/token \
  -d "grant_type=authorization_code" \
  -d "client_id=client123" \
  -d "client_secret=secret456" \
  -d "redirect_uri=http://localhost:8000/callback" \
  -d "code=AUTH_CODE_FROM_CALLBACK"
```

### 3. UserInfo Request (cURL)
```bash
curl -H "Authorization: Bearer ACCESS_TOKEN_HERE" http://localhost:5000/userinfo
```

---

## 🐳 Docker Support

### Build & Run Using Docker
```bash
docker build -t flask-oidc .
docker run -p 5000:5000 flask-oidc
```

### Or Use Docker Compose
```bash
docker-compose up --build
```

Server will be available at: `http://localhost:5000`

---

## 🧪 Testing

1. Start server
2. Run through auth code flow (browser + `curl`)
3. Validate token signature & payload

---

## 🤝 Contributing

- Fork & PR
- Create feature branches
- Write tests & update README

---

## 📄 License

[MIT](LICENSE)
