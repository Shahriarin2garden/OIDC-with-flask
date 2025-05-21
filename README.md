# Flask OIDC Provider

## 🔍 How OpenID Connect Works

OpenID Connect (OIDC) is a simple identity layer on top of the OAuth 2.0 protocol that allows clients to verify the identity of users and obtain basic profile information in a secure and standardized manner. It provides a seamless way to handle single sign-on (SSO) and token-based authentication for web and mobile applications.

### 📊 OIDC Authentication Workflow

1. **Client Registration**: An application registers with the OIDC provider and receives a `client_id` and `client_secret`.

2. **Authorization Request**: The user is redirected to the `/authorize` endpoint with a request that includes the `client_id`, scopes, redirect URI, and a code challenge (PKCE).

3. **User Authentication**: The provider authenticates the user (e.g., via login form).

4. **User Consent**: If required, the user consents to sharing requested information.

5. **Authorization Code Issued**: The provider sends an authorization code to the client’s redirect URI.

6. **Token Request**: The client sends the code and code verifier to the `/token` endpoint.

7. **Token Response**: The provider returns an ID token (identity), access token (authorization), and optionally a refresh token.

8. **UserInfo Retrieval**: The client can use the access token to fetch profile data from the `/userinfo` endpoint.

9. **Token Introspection/Revocation**: Tokens can be validated or revoked using respective endpoints.

OIDC enhances OAuth 2.0 by returning a cryptographically signed ID token that includes identity claims about the user, enabling secure and interoperable SSO experiences. The ID token, typically a JWT, asserts the user's identity and is consumed by client applications to establish authenticated sessions.

![oidc Architecture](assets/oidc.svg)


This diagram illustrates a typical OIDC Authorization Code Flow with PKCE support, where identity assertions and access control are separated via the ID and access tokens respectively.

**Flask OIDC Provider** is a modular and standards-compliant implementation of an OpenID Connect (OIDC) identity provider using Flask. This project supports secure identity flows and token-based authentication for modern web and API clients. It offers:

* Authorization Code Flow with Proof Key for Code Exchange (PKCE)
* Refresh token issuance and lifecycle management
* Dynamic client registration capabilities
* Standards-aligned token revocation and introspection endpoints
* UserInfo and JWKS endpoints conforming to OIDC specifications

---

## 🗂️ Repository Structure

Understand the organization of code, assets, and configuration:

```text
flask-oidc-provider/
├── app.py               # Application entry point and routing logic
├── config.py            # Configuration management and key loading
├── models.py            # In-memory structures for client and token state
├── auth/                # Authentication and cryptographic modules
│   ├── token.py         # JWT handling and introspection
│   └── pkce.py          # PKCE challenge/response utilities
├── templates/           # HTML views for login and consent
│   ├── login.html
│   └── consent.html
├── static/              # CSS and static assets
├── jwks.json            # JSON Web Key Set (JWKS) document
├── public.pem           # Public RSA key for token verification
├── private.pem          # Private RSA key for signing
├── requirements.txt     # Dependency list
├── tests/               # Test suite (unit + integration)
│   ├── test_flow.py
│   └── test_jwks.py
├── Dockerfile           # Docker image specification
├── docker-compose.yml   # Docker Compose stack (app + Redis)
├── .github/workflows/   # CI configuration
│   └── ci.yml
└── README.md            # Project documentation
```

---

## 🚀 Core Capabilities

* 🔐 **OIDC Authorization Code Flow** with PKCE
* 🔄 **Refresh Token Support** for long-lived sessions
* 🔍 **Token Introspection & Revocation** for secure access control
* 📘 **OIDC Discovery Metadata** endpoint
* 👤 **UserInfo Endpoint** with customizable claims
* 🛡️ **JWT-based Token Architecture** (RS256 signed)
* 🧠 **Pluggable In-Memory Store**, Redis-ready backend

---

## ➕ Extended Features

1. **Dynamic Client Registration**

   * Client metadata validation and compliance checks
   * Enforces redirect URI and grant type rules

2. **Scopes and Claims Management**

   * Support for standard OIDC scopes: `profile`, `email`, `groups`
   * Configurable token claim augmentation

3. **Comprehensive Token Lifecycle**

   * Revocation endpoint for client-triggered invalidation
   * Introspection endpoint for downstream services

4. **Security Enhancements**

   * TLS and HSTS support
   * Rate limiting and brute-force protection
   * CSRF tokens on user-facing forms

5. **Monitoring and Metrics**

   * Prometheus-compatible metrics output
   * JSON-structured logs with trace IDs

6. **Developer Tooling**

   * Full OpenAPI 3.0 schema
   * Postman and Insomnia client configs
   * Dockerized development environment

7. **Testing and Automation**

   * Pytest-based suite with high coverage
   * CI/CD pipeline with linting, testing, Docker build

8. **Reference Clients**

   * Example Single Page Application (SPA) and CLI clients
   * Multilingual implementation samples (Python, Go, Node.js)

---

## 🛠️ Installation & Setup

```bash
git clone https://github.com/your-org/flask-oidc-provider.git
cd flask-oidc-provider
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 🔐 Environment Variables

Define the following to configure runtime behavior:

```ini
FLASK_ENV=production                 # Runtime environment
SECRET_KEY=super-secret-key         # Flask session secret
PRIVATE_KEY_PATH=./private.pem      # Path to private signing key
PUBLIC_KEY_PATH=./public.pem        # Path to public verification key
ISSUER_URL=https://auth.example.com # OIDC issuer identifier
TOKEN_EXPIRY=3600                   # Access token expiration (in seconds)
REFRESH_TOKEN_EXPIRY=86400          # Refresh token expiration (in seconds)
```

---

## ▶️ Local Development

```bash
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000
```

Override defaults using a `.env`file or environment variables.

---

## 🔗 API Endpoint Overview

| Method | Path                                | Description                                         |
| ------ | ----------------------------------- | --------------------------------------------------- |
| POST   | `/register`                         | Register a new client dynamically                   |
| GET    | `/.well-known/openid-configuration` | Retrieve OIDC metadata                              |
| GET    | `/jwks`                             | JSON Web Key Set exposure                           |
| GET    | `/authorize`                        | Authorization request UI (PKCE flow)                |
| POST   | `/authorize`                        | Authenticate and prepare user consent               |
| POST   | `/consent`                          | Grant authorization code after consent              |
| POST   | `/token`                            | Exchange code or refresh token for access/ID tokens |
| POST   | `/revoke`                           | Revoke active tokens                                |
| POST   | `/introspect`                       | Validate and decode access/refresh tokens           |
| GET    | `/userinfo`                         | Return user claims (access token required)          |

---

## 📡 REST API Usage Examples

### 🔧 Client Registration

```bash
curl -X POST https://auth.example.com/register \
  -H 'Content-Type: application/json' \
  -d '{
    "client_name": "my-spa-app",
    "redirect_uris": ["https://app.example.com/callback"],
    "grant_types": ["authorization_code"],
    "response_types": ["code"],
    "scope": "openid profile email"
}'
```

### 🔑 Authorization Code Flow (with PKCE)

**Step 1: Generate verifier & challenge**

```bash
code_verifier=$(openssl rand -base64 32 | tr -d '=+/')
code_challenge=$(echo -n "$code_verifier" | openssl dgst -sha256 -binary | openssl base64 | tr -d '=+/')
```

**Step 2: Redirect to authorize endpoint**

```text
GET https://auth.example.com/authorize?
  response_type=code
 &client_id=CLIENT_ID
 &redirect_uri=https://app.example.com/callback
 &scope=openid profile email
 &code_challenge=$code_challenge
 &code_challenge_method=S256
 &state=XYZ
```

**Step 3: Exchange code for token**

```bash
curl -X POST https://auth.example.com/token \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=authorization_code&
client_id=CLIENT_ID&
code=$AUTH_CODE&
redirect_uri=https://app.example.com/callback&
code_verifier=$code_verifier'
```

### 🔄 Refresh Token Exchange

```bash
curl -X POST https://auth.example.com/token \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=refresh_token&
refresh_token=REFRESH_TOKEN&
client_id=CLIENT_ID'
```

### 🔍 Token Introspection

```bash
curl -X POST https://auth.example.com/introspect \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'token=ACCESS_TOKEN'
```

### 👤 User Info Retrieval

```bash
curl -H 'Authorization: Bearer ACCESS_TOKEN' \
  https://auth.example.com/userinfo
```

---

## 🐳 Docker Deployment

Launch the stack using Docker Compose:

```bash
docker-compose up --build
```

Configuration can be customized via `.env`or Docker environment overrides.

---

## 📦 Deployment

### 🐘 Gunicorn with Nginx (Production)

1. Install Gunicorn:

```bash
pip install gunicorn
```

2. Start the app:

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

3. Set up Nginx as a reverse proxy and enable HTTPS with Let's Encrypt.

### 🖥️ Systemd Unit (Linux Service)

Create`/etc/systemd/system/flask-oidc.service`:

```ini
[Unit]
Description=Flask OIDC Provider
After=network.target

[Service]
User=www-data
WorkingDirectory=/opt/flask-oidc-provider
ExecStart=/opt/flask-oidc-provider/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl enable flask-oidc
sudo systemctl start flask-oidc
```

---

## 🤝 Contributing

We welcome your contributions.

1. Fork this repository
2. Create a new branch:`git checkout -b feature/awesome-feature`
3. Implement changes with proper tests and documentation
4. Submit a pull request

See the [Contributor Guide](CONTRIBUTING.md) and [Code of Conduct](CODE_OF_CONDUCT.md) for collaboration guidelines. Visit our [GitHub Issues](https://github.com/your-org/flask-oidc-provider/issues) page to explore current opportunities.

---

## 📄 License

Licensed under the [MIT License](LICENSE).

---

*Thank you for your interest and support. Contributions are always appreciated.*
