# Frappe TickTix API Documentation

## 🌐 **Overview**

This document describes the available API endpoints in the Frappe TickTix app.

## 🔐 **Authentication**

### **Supported Methods:**
- **JWT Token**: Bearer token in Authorization header
- **Session**: Frappe session cookies
- **API Key**: Frappe API key authentication

### **JWT Authentication:**
```bash
# Using JWT token
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     https://your-site.com/api/method/frappe_ticktix.api.jwt_api.test_jwt_auth
```

### **Session Authentication:**
```bash
# Using session (login first)
curl -c cookies.txt -X POST \
     -d "usr=user@example.com&pwd=password" \
     https://your-site.com/api/method/login

# Then use cookies
curl -b cookies.txt \
     https://your-site.com/api/method/frappe_ticktix.api.jwt_api.get_user_profile
```

## 🔑 **Authentication Endpoints**

### **Test JWT Authentication**
- **Endpoint**: `/api/method/frappe_ticktix.api.jwt_api.test_jwt_auth`
- **Method**: GET
- **Authentication**: JWT or Session
- **Description**: Test endpoint to verify authentication method

**Response:**
```json
{
  "status": "jwt_authenticated",
  "user": "user@example.com",
  "authentication_method": "jwt",
  "jwt_claims": {
    "sub": "user123",
    "email": "user@example.com",
    "name": "John Doe",
    "roles": ["Employee", "Desk User"]
  },
  "message": "Successfully authenticated via JWT token"
}
```

### **Get User Profile**
- **Endpoint**: `/api/method/frappe_ticktix.api.jwt_api.get_user_profile`  
- **Method**: GET
- **Authentication**: JWT or Session
- **Description**: Get current user profile information

**Response:**
```json
{
  "email": "user@example.com",
  "full_name": "John Doe",
  "first_name": "John",
  "last_name": "Doe",
  "user_type": "System User",
  "roles": ["Employee", "Desk User"],
  "authentication_method": "jwt",
  "jwt_info": {
    "sub": "user123",
    "iss": "https://login.ticktix.com",
    "aud": "api",
    "exp": 1696435200,
    "iat": 1696348800
  }
}
```

### **Health Check**
- **Endpoint**: `/api/method/frappe_ticktix.api.jwt_api.health_check`
- **Method**: GET  
- **Authentication**: None (public)
- **Description**: System health check

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2025-10-04 16:17:57.847220",
  "version": "1.0"
}
```

## 📱 **Mobile API Endpoints**

### **Mobile API Information**
- **Endpoint**: `/api/method/frappe_ticktix.api.jwt_api.mobile_api_info`
- **Method**: GET
- **Authentication**: None (public)
- **Description**: Get API configuration for mobile applications

**Response:**
```json
{
  "api_version": "1.0",
  "site": "ticktix.local",
  "server_info": {
    "frappe_version": "15.x.x",
    "site_name": "ticktix.local"
  },
  "authentication": {
    "jwt_enabled": true,
    "methods_supported": ["jwt", "session"],
    "recommended_flow": "pkce",
    "mobile_client_id": "mobile-app"
  },
  "oauth_config": {
    "issuer": "https://login.ticktix.com",
    "audience": "ticktix.local",
    "auth_endpoint": "https://login.ticktix.com/connect/authorize",
    "token_endpoint": "https://login.ticktix.com/connect/token",
    "jwks_uri": "https://login.ticktix.com/.well-known/openid-configuration/jwks"
  },
  "api_endpoints": {
    "test_auth": "/api/method/frappe_ticktix.api.jwt_api.test_jwt_auth",
    "user_profile": "/api/method/frappe_ticktix.api.jwt_api.get_user_profile",
    "mobile_auth_url": "/api/method/frappe_ticktix.api.jwt_api.get_mobile_auth_url"
  },
  "mobile_integration": {
    "redirect_uri_scheme": "com.yourapp://oauth/callback",
    "scopes": ["openid", "profile", "api"],
    "pkce_required": true
  }
}
```

### **Generate Mobile Auth URL**
- **Endpoint**: `/api/method/frappe_ticktix.api.jwt_api.get_mobile_auth_url`
- **Method**: POST
- **Authentication**: None (public)
- **Description**: Generate PKCE authentication URL for mobile apps

**Request:**
```json
{
  "redirect_uri": "com.yourapp://oauth/callback",
  "state": "random_state_string_12345"
}
```

**Response:**
```json
{
  "auth_url": "https://login.ticktix.com/connect/authorize?client_id=mobile-app&response_type=code&scope=openid+profile+api&redirect_uri=com.yourapp://oauth/callback&state=random_state_string_12345&code_challenge=CODE_CHALLENGE&code_challenge_method=S256&audience=ticktix.local",
  "code_challenge": "CODE_CHALLENGE_VALUE",
  "state": "random_state_string_12345",
  "issuer": "https://login.ticktix.com"
}
```

## 🎨 **Branding Endpoints**

### **Get Branding Configuration**
- **Endpoint**: `/api/method/frappe_ticktix.core.config_manager.get_branding_config`
- **Method**: GET
- **Authentication**: Session (internal use)
- **Description**: Get branding configuration

**Response:**
```json
{
  "ticktix": {
    "website_settings": {
      "company_logo": "https://login.ticktix.com/images/ticktix.jpg",
      "app_name": "Facilitix", 
      "app_title": "Facilitix Platform"
    }
  }
  "favicon": "https://ticktix.com/img/favicon.png",
  "splash_image": "https://login.ticktix.com/images/ticktix.jpg"
}
```

### **Get Cached Branding**
- **Endpoint**: `/api/method/frappe_ticktix.plugins.branding.logo_manager.get_branding_config`
- **Method**: GET
- **Authentication**: Session (internal use)
- **Description**: Get branding configuration with cached image URLs

**Response:**
```json
{
  "company_logo": "/files/cached_images/companylogo.jpg",
  "app_name": "Facilitix",
  "app_title": "Facilitix Platform", 
  "favicon": "https://ticktix.com/img/favicon.png",
  "splash_image": "/files/cached_images/splashimage.jpg",
  "login_title": "Login to Facilitix"
}
```

## 🔐 **OAuth & Social Login**

### **Social Login Providers**
- **Endpoint**: `/api/method/frappe.integrations.oauth2_logins.get_social_login_providers`
- **Method**: GET
- **Authentication**: None (public)
- **Description**: Get available social login providers (overridden by TickTix)

**Response:**
```json
[
  {
    "name": "ticktix",
    "label": "TickTix",
    "client_id": "YOUR_CLIENT_ID",
    "authorize_url": "https://login.ticktix.com/connect/authorize",
    "token_url": "https://login.ticktix.com/connect/token",
    "tenant_param": "tenant",
    "auth_params": {
      "response_type": "code",
      "scope": "openid profile email"
    },
    "redirect_url": "/api/method/frappe.integrations.oauth2_logins.custom/ticktix"
  }
]
```

### **OAuth Callback Handler**
- **Endpoint**: `/api/method/frappe.integrations.oauth2_logins.custom/ticktix`
- **Method**: GET
- **Authentication**: None (OAuth callback)
- **Description**: Handle OAuth callback from TickTix identity server

**Parameters:**
- `code`: Authorization code from OAuth provider
- `state`: State parameter for CSRF protection

## 📊 **Configuration Endpoints**

### **Get Authentication Config**
- **Endpoint**: `/api/method/frappe_ticktix.core.config_manager.get_auth_config`
- **Method**: GET  
- **Authentication**: Session (internal use)
- **Description**: Get authentication configuration

**Response:**
```json
{
  "ticktix": {
    "oauth": {
      "client_id": "YOUR_CLIENT_ID",
      "client_secret": "YOUR_CLIENT_SECRET"
    },
    "identity_server": {
      "base_url": "https://login.ticktix.com",
      "authorize_url": "/connect/authorize", 
      "token_url": "/connect/token"
    },
    "jwt": {
      "enabled": true,
      "auto_provision": false
    }
  }
  "jwt_enabled": true,
  "jwt_audience": "api",
  "jwt_auto_provision": false
}
```

### **Get HR Configuration**
- **Endpoint**: `/api/method/frappe_ticktix.core.config_manager.get_hr_config`
- **Method**: GET
- **Authentication**: Session (internal use)  
- **Description**: Get HR-related configuration

**Response:**
```json
{
  "hr_employee_id_patterns": {},
  "hr_attendance_rules": {},
  "hr_enable_client_dayoff": false
}
```

## 📱 **Mobile Integration Example**

### **Complete Mobile Authentication Flow:**

**Step 1: Get Mobile API Info**
```bash
curl https://your-site.com/api/method/frappe_ticktix.api.jwt_api.mobile_api_info
```

**Step 2: Generate Auth URL**
```bash
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"redirect_uri": "com.yourapp://oauth/callback", "state": "random123"}' \
     https://your-site.com/api/method/frappe_ticktix.api.jwt_api.get_mobile_auth_url
```

**Step 3: Direct user to auth_url (from Step 2 response)**

**Step 4: Handle callback in your mobile app**

**Step 5: Use JWT token for API calls**
```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     https://your-site.com/api/method/frappe_ticktix.api.jwt_api.get_user_profile
```

## ❌ **Error Responses**

### **Authentication Error:**
```json
{
  "exc_type": "AuthenticationError",
  "exception": "Authentication failed",
  "_server_messages": "[\"Invalid token\"]"
}
```

### **Permission Error:**
```json
{
  "exc_type": "PermissionError", 
  "exception": "Not permitted",
  "_server_messages": "[\"You do not have permission to access this resource\"]"
}
```

### **Validation Error:**
```json
{
  "exc_type": "ValidationError",
  "exception": "Validation failed",
  "_server_messages": "[\"Required parameter missing: redirect_uri\"]"
}
```

## 🔧 **Rate Limiting**

- **Default Limit**: 100 requests per minute per IP
- **Authenticated Users**: 500 requests per minute
- **Headers**: 
  - `X-RateLimit-Limit`: Request limit
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Reset timestamp

## 📋 **API Versioning**

Current API version is **v1**. Future API endpoints will be versioned:
- **Current**: `/api/method/frappe_ticktix.api.jwt_api.*`
- **Future**: `/api/method/frappe_ticktix.api.v1.*` or `/api/method/frappe_ticktix.api.v2.*`

Backward compatibility is maintained for all current endpoints.