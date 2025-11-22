# JWT Authentication Middleware for Frappe TickTix

## Purpose and Benefits

### Why JWT Configuration is Needed

JWT (JSON Web Token) authentication solves a fundamental challenge: **mobile apps and API clients cannot use browser-based session authentication**. Here's why this configuration is essential:

#### **Technical Necessity**
- **Browser Authentication**: Uses cookies and redirects, works great for web browsers
- **Mobile Apps**: Cannot handle cookie-based sessions or redirect flows reliably
- **API Clients**: Need stateless authentication for server-to-server communication
- **Cross-Platform**: JWT tokens work identically across iOS, Android, web APIs, and desktop apps

#### **Business Benefits**
1. **Unified Authentication**: Same IdentityServer handles both web and mobile users
2. **Mobile User Experience**: Native app authentication without web browser redirects
3. **API Integration**: Third-party services can authenticate using standard JWT tokens
4. **Scalability**: Stateless tokens don't require server-side session storage
5. **Security**: Token-based auth with RSA signatures and JWKS validation

#### **Why These Configuration Options Matter**
- `jwt_auto_provision: false` - **Security**: Prevents unknown users from auto-creating accounts
- `jwt_allowed_domains` - **Control**: Restricts user creation to trusted email domains
- `ticktix_base_url` - **Integration**: Connects to your existing IdentityServer for JWKS validation
- `jwt_audience` - **Security**: Ensures tokens are intended for your specific API

#### **When You Need This**
- ✅ Building mobile apps (iOS/Android) that need API access
- ✅ Creating API integrations with external services
- ✅ Supporting both web and mobile users with unified authentication
- ✅ Implementing stateless authentication for better scalability
- ❌ **Not needed** if you only have browser-based web users

## Overview

> **🔒 Security Notice**: All example tokens and credentials in this guide use `**placeholder**` format. Replace with your actual values and never expose real credentials in documentation or version control.

This middleware extends Frappe's authentication system to support JWT Bearer tokens from IdentityServer for mobile and API clients, while maintaining full compatibility with existing browser-based social login functionality.

## Key Features

- **Dual Authentication Support**: Browser users continue using TickTix OAuth, mobile/API users use JWT tokens
- **Non-Intrusive**: Zero impact on existing browser authentication flows
- **Secure**: Supports both JWKS (recommended) and shared secret JWT validation
- **Auto-Provisioning**: Optionally create Frappe users from valid JWT tokens
- **Role Mapping**: Map JWT roles to Frappe roles automatically
- **Configurable**: Full configuration via TickTix Settings DocType

## Architecture

### Authentication Flow

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Browser User  │    │  Mobile/API User │    │  Frappe Server  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                        │
         │ GET /login            │ API Request            │
         │──────────────────────▶│ + Bearer JWT           │
         │                       │───────────────────────▶│
         │ Redirect to TickTix   │                        │
         │◀──────────────────────│ JWT Middleware         │
         │                       │ Validates Token        │
         │ OAuth Flow            │◀───────────────────────│
         │◀─────────────────────▶│                        │
         │                       │ API Response           │
         │ Session Cookie        │◀───────────────────────│
         │◀──────────────────────│                        │
```

### Middleware Processing

1. **Request Inspection**: Only processes `/api/*` requests with `Authorization: Bearer` headers
2. **JWT Validation**: Validates token using JWKS or shared secret
3. **User Mapping**: Maps JWT claims to existing Frappe users or auto-provisions new ones
4. **Session Setup**: Creates temporary API session context (stateless)

## Configuration

### Ultra-Clean Configuration

The JWT middleware leverages existing TickTix configuration to minimize setup and avoid duplication.

#### Common Site Config (`sites/common_site_config.json`)

```json
{
  "ticktix_base_url": "https://login.ticktix.com",  // EXISTING - Used for both OAuth and JWT
  "jwt_enabled": true,
  "jwt_audience": "api",
  "jwt_auto_provision": false,
  "jwt_allowed_domains": ["ticktix.com"]
}
```

#### Configuration Settings Explained

| Setting | Purpose | Security Impact | Recommended Value |
|---------|---------|-----------------|-------------------|
| `jwt_enabled` | Enable JWT authentication for mobile/API access | Low risk - just enables the feature | `true` |
| `jwt_audience` | Validates JWT `aud` claim - ensures tokens are for your API | **High security** - prevents token reuse | `"api"` or your app name |
| `jwt_auto_provision` | Create new Frappe users automatically from JWT claims | **High security risk** if `true` | `false` (recommended) |
| `jwt_allowed_domains` | Email domains allowed for auto-provisioning | Medium security - limits auto-creation | Your trusted domains only |
| `ticktix_base_url` | IdentityServer URL for JWKS validation | Critical - must match your auth server | Your IdentityServer URL |

#### Security Recommendations

**🔒 Production Security (Recommended):**
```json
{
  "jwt_auto_provision": false,     // Only existing users can authenticate
  "jwt_allowed_domains": [],       // No auto-provisioning from any domain
  "jwt_audience": "your-api-name"  // Specific audience validation
}
```

**⚠️ Development/Testing (Less Secure):**
```json
{
  "jwt_auto_provision": true,           // Auto-create users for testing
  "jwt_allowed_domains": ["test.com"],  // Limit to test domain
  "jwt_audience": "api"                 // Generic audience
}
```

**That's it!** Only 4 JWT-specific settings needed:
- `jwt_enabled`: Enable JWT authentication for all custom apps
- `jwt_audience`: JWT audience claim validation (security)
- `jwt_auto_provision`: Auto-create users from JWT tokens (security risk if enabled)
- `jwt_allowed_domains`: Email domains allowed for auto-provisioning (security control)

#### Automatic Configuration
- **JWT Issuer**: Uses existing `ticktix_base_url`
- **JWKS Endpoint**: Auto-constructed as `{ticktix_base_url}/.well-known/openid-configuration/jwks`
- **Validation Method**: Always JWKS (secure)
- **Algorithm**: Always RS256 (secure)
- **Cross-App Support**: Works for all custom apps (frappe_ticktix, helpdesk, hrms, etc.)

## How to Connect and Use

### Step 1: Mobile App Gets JWT Token

#### Option A: PKCE Flow (Recommended for Mobile Apps)
```javascript
// 1. Get authorization URL
const response = await fetch('/api/method/frappe_ticktix.api.mobile_login?tenant_domain=ticktix');
const { login_url } = await response.json();

// 2. Redirect user to IdentityServer
window.location = login_url;

// 3. Handle callback and extract JWT from URL fragments or code exchange
// (Standard PKCE implementation)
```

#### Option B: Direct IdentityServer Integration
```javascript
// Use existing TickTix IdentityServer endpoints
const tokenEndpoint = 'https://login.ticktix.com/connect/token';
const authEndpoint = 'https://login.ticktix.com/connect/authorize';

// Standard OAuth 2.0 PKCE flow to get JWT token
```

### Step 2: Use JWT Token for API Calls

#### Basic API Call
```javascript
const apiCall = async (endpoint, jwtToken) => {
  const response = await fetch(`/api/method/${endpoint}`, {
    headers: {
      'Authorization': `Bearer ${jwtToken}`,
      'Content-Type': 'application/json'
    }
  });
  return response.json();
};

// Example usage
const userProfile = await apiCall('frappe_ticktix.api.jwt_api.get_user_profile', myJwtToken);
```

#### Full Example: Mobile App Integration
```javascript
class FrappeJWTClient {
  constructor(baseUrl, jwtToken) {
    this.baseUrl = baseUrl;
    this.jwtToken = jwtToken;
  }

  async call(endpoint, method = 'GET', data = null) {
    const options = {
      method,
      headers: {
        'Authorization': `Bearer ${this.jwtToken}`,
        'Content-Type': 'application/json'
      }
    };

    if (data && method !== 'GET') {
      options.body = JSON.stringify(data);
    }

    const response = await fetch(`${this.baseUrl}/api/method/${endpoint}`, options);
    
    if (!response.ok) {
      throw new Error(`API call failed: ${response.status}`);
    }
    
    return response.json();
  }

  // Test authentication
  async testAuth() {
    return this.call('frappe_ticktix.api.jwt_api.test_jwt_auth');
  }

  // Get user profile
  async getUserProfile() {
    return this.call('frappe_ticktix.api.jwt_api.get_user_profile');
  }

  // Get API information
  async getApiInfo() {
    return this.call('frappe_ticktix.api.jwt_api.mobile_api_info');
  }
}

// Usage
const client = new FrappeJWTClient('https://your-site.com', yourJwtToken);
const profile = await client.getUserProfile();
```

### Step 3: API Testing & Validation

#### Test JWT Authentication
```bash
# Test authentication
curl -H "Authorization: Bearer **your_jwt_token_here**" \
     https://your-site.com/api/method/frappe_ticktix.api.jwt_api.test_jwt_auth

# Response:
{
  "message": {
    "status": "jwt_authenticated",
    "user": "user@ticktix.com",
    "authentication_method": "jwt",
    "jwt_claims": { "sub": "12345", "email": "user@ticktix.com" }
  }
}
```

#### Get User Profile
```bash
curl -H "Authorization: Bearer **your_jwt_token_here**" \
     https://your-site.com/api/method/frappe_ticktix.api.jwt_api.get_user_profile

# Response:
{
  "message": {
    "email": "user@ticktix.com",
    "full_name": "John Doe",
    "roles": ["Desk User"],
    "authentication_method": "jwt",
    "jwt_info": { "sub": "12345", "iss": "https://login.ticktix.com" }
  }
}
```

#### Test Server Configuration
```bash
# Check server configuration
curl https://your-site.com/api/method/frappe_ticktix.api.jwt_api.mobile_api_info

# Response:
{
  "message": {
    "api_version": "1.0",
    "authentication": {
      "jwt_enabled": true,
      "methods_supported": ["jwt", "session"]
    }
  }
}
```

### Step 4: Error Handling

#### Common HTTP Status Codes
- **200**: Success
- **401**: Invalid or expired JWT token
- **403**: User not authorized (no account or disabled)
- **404**: API endpoint not found
- **500**: Server error

#### Error Response Format
```json
{
  "exc_type": "AuthenticationError",
  "exception": "Invalid or expired JWT token"
}
```

#### Handling Errors in Code
```javascript
const handleApiCall = async (endpoint, jwtToken) => {
  try {
    const response = await fetch(`/api/method/${endpoint}`, {
      headers: { 'Authorization': `Bearer ${jwtToken}` }
    });

    if (response.status === 401) {
      // Token expired or invalid - refresh token
      throw new Error('Authentication required');
    }
    
    if (response.status === 403) {
      // User not authorized - contact admin
      throw new Error('Access denied');
    }

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    return response.json();
  } catch (error) {
    console.error('API call failed:', error);
    throw error;
  }
};
```

## JWT Token Requirements

### Required Claims
- `sub` or `email`: User identifier
- `exp`: Expiration time
- `iat`: Issued at time

### Optional Claims  
- `iss`: Issuer (validated if configured)
- `aud`: Audience (validated if configured)
- `name`: Full name
- `given_name`: First name
- `family_name`: Last name
- `preferred_username`: Username
- `role` or `roles`: User roles
- `scope` or `scp`: Token scopes

### Example JWT Payload
```json
{
  "sub": "12345",
  "email": "user@example.com", 
  "name": "John Doe",
  "given_name": "John",
  "family_name": "Doe",
  "preferred_username": "johndoe",
  "roles": ["user", "api_access"],
  "scope": "openid profile email api",
  "iss": "https://login.ticktix.com",
  "aud": "frappe-api",
  "exp": 1632744000,
  "iat": 1632657600
}
```

## Security Considerations

### JWT Validation
- Always use JWKS for production (RSA signatures)
- Validate issuer and audience claims
- Check token expiration
- Implement proper error handling

### User Provisioning
- Restrict auto-provisioning to trusted domains
- Map JWT roles to appropriate Frappe roles
- Use principle of least privilege for default roles

### API Access
- Rate limiting on API endpoints
- Audit logging for JWT authentication
- Regular token rotation

## Connection Examples by Platform

### React Native / Expo
```javascript
import AsyncStorage from '@react-native-async-storage/async-storage';

class TickTixAPI {
  constructor(baseUrl) {
    this.baseUrl = baseUrl;
    this.token = null;
  }

  async authenticate() {
    // Implement PKCE flow with TickTix IdentityServer
    // Store token securely
    this.token = await this.getPKCEToken();
    await AsyncStorage.setItem('jwt_token', this.token);
  }

  async apiCall(endpoint, options = {}) {
    if (!this.token) {
      this.token = await AsyncStorage.getItem('jwt_token');
    }

    return fetch(`${this.baseUrl}/api/method/${endpoint}`, {
      ...options,
      headers: {
        'Authorization': `Bearer ${this.token}`,
        'Content-Type': 'application/json',
        ...options.headers
      }
    });
  }
}
```

### Flutter/Dart
```dart
class FrappeJWTClient {
  final String baseUrl;
  String? jwtToken;

  FrappeJWTClient(this.baseUrl);

  Future<Map<String, dynamic>> call(String endpoint, {Map<String, dynamic>? data}) async {
    final response = await http.get(
      Uri.parse('$baseUrl/api/method/$endpoint'),
      headers: {
        'Authorization': 'Bearer $jwtToken',
        'Content-Type': 'application/json',
      },
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('API call failed: ${response.statusCode}');
    }
  }
}
```

### Python (for backend integrations)
```python
import requests

class FrappeJWTClient:
    def __init__(self, base_url, jwt_token):
        self.base_url = base_url
        self.jwt_token = jwt_token
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {jwt_token}',
            'Content-Type': 'application/json'
        })

    def call(self, endpoint, method='GET', data=None):
        url = f"{self.base_url}/api/method/{endpoint}"
        response = self.session.request(method, url, json=data)
        response.raise_for_status()
        return response.json()

    def test_auth(self):
        return self.call('frappe_ticktix.api.jwt_api.test_jwt_auth')

# Usage
client = FrappeJWTClient('https://your-site.com', '**your_jwt_token_here**')
result = client.test_auth()
```

## Troubleshooting

### Common Issues & Solutions

#### 1. JWT Token Invalid (401 Error)
```bash
# Check token expiration
echo "**your_jwt_token_here**" | cut -d'.' -f2 | base64 -d | jq '.exp'

# Verify issuer configuration
curl https://your-site.com/api/method/frappe_ticktix.api.jwt_api.mobile_api_info
```

#### 2. User Not Found (403 Error)
```json
// Enable auto-provisioning in common_site_config.json
{
  "jwt_auto_provision": true,
  "jwt_allowed_domains": ["yourdomain.com"]
}
```

#### 3. JWKS Connection Issues
```bash
# Test JWKS endpoint directly
curl https://login.ticktix.com/.well-known/openid-configuration/jwks

# Check server logs
tail -f sites/ticktix.local/logs/frappe.log | grep JWT
```

#### 4. Cross-Origin (CORS) Issues
```json
// Add to common_site_config.json for development
{
  "allow_cors": "*",
  "cors_headers": ["Authorization"]
}
```

### Debug Configuration
```json
// Add to common_site_config.json for debugging
{
  "developer_mode": 1,
  "log_level": "DEBUG"
}
```

### Testing Endpoints

| Endpoint | Purpose | Auth Required |
|----------|---------|---------------|
| `/api/method/frappe_ticktix.api.jwt_api.health_check` | Health check | No |
| `/api/method/frappe_ticktix.api.jwt_api.mobile_api_info` | API information | No |
| `/api/method/frappe_ticktix.api.jwt_api.test_jwt_auth` | Test JWT auth | Yes |
| `/api/method/frappe_ticktix.api.jwt_api.get_user_profile` | User profile | Yes |

## Compatibility

- **Frappe**: v14.x and above
- **Python**: 3.8+ 
- **Dependencies**: `PyJWT`, `requests`, `cryptography`
- **IdentityServer**: 4.x and above

## Migration Guide

### From Pure OAuth to JWT

1. Install JWT middleware (already included)
2. Configure TickTix Settings  
3. Update mobile apps to use JWT tokens
4. Browser users continue unchanged

### Existing User Migration

Users with existing social login mappings will automatically work with JWT tokens containing the same `sub` claim.

## API Reference

### Endpoints

- `GET /api/method/frappe_ticktix.api.jwt_api.test_jwt_auth` - Test authentication
- `GET /api/method/frappe_ticktix.api.jwt_api.get_user_profile` - Get user profile
- `POST /api/method/frappe_ticktix.auth.user_mapper.sync_jwt_user_data` - Sync user data
- `GET /api/method/frappe_ticktix.auth.user_mapper.get_jwt_user_info` - Get JWT claims

### Configuration Methods

- `test_jwt_connection()` - Test JWT configuration
- `clear_jwks_cache()` - Clear JWKS key cache

## Performance Considerations

- JWKS keys are cached for 1 hour
- JWT validation adds ~1-2ms per request
- Auto-provisioning involves database writes
- Consider token caching for high-frequency APIs