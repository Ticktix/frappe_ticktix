# Authentication Flows Summary

## Flow Separation

Your JWT middleware implementation maintains **complete separation** between browser and mobile authentication flows:

### 🌐 **Browser Flow** (Existing - Unchanged)
```
Desktop User → your-site.com → Your TickTix Custom App → Social Login Redirect → IdentityServer OAuth → Session Cookies → Normal Frappe API
```

- **Entry Point**: Your Frappe site (`your-site.com`)
- **Authentication**: Your existing social login enforcement
- **Technology**: OAuth redirect + server-side sessions
- **API Access**: Session cookies (existing Frappe way)
- **Impact**: **Zero changes** to existing functionality

### 📱 **Mobile Flow** (New - JWT API)
```
Mobile User → Domain Input → IdentityServer Discovery → PKCE OAuth → JWT Token → Bearer API Calls
```

- **Entry Point**: IdentityServer directly or via discovery
- **Authentication**: PKCE OAuth flow
- **Technology**: JWT Bearer tokens
- **API Access**: `Authorization: Bearer <jwt>` headers
- **Storage**: Secure mobile storage (Keychain/Keystore)

## Two Mobile Approaches

### **Approach 1: Direct IdentityServer** (Recommended)

**Mobile App Flow:**
1. User enters domain: `your-site.com`
2. App calls discovery: `GET /api/method/frappe_ticktix.api.v1.jwt_api.mobile_api_info`
3. App gets IdentityServer config: `https://login.ticktix.com`
4. App initiates PKCE OAuth directly with IdentityServer
5. User authenticates on IdentityServer
6. App receives JWT token
7. App makes API calls: `Authorization: Bearer <jwt>`

**Pros:**
- ✅ Standard OAuth mobile pattern
- ✅ Better performance (fewer hops)
- ✅ Works offline after token acquisition
- ✅ Industry best practice

### **Approach 2: Frappe-Mediated** (Alternative)

**Mobile App Flow:**
1. User enters domain: `your-site.com`
2. App calls: `POST /api/method/frappe_ticktix.api.v1.jwt_api.get_mobile_auth_url`
3. Frappe returns PKCE auth URL
4. App opens auth URL in browser/webview
5. User authenticates on IdentityServer
6. App handles OAuth callback
7. App exchanges code for JWT (via IdentityServer)
8. App makes API calls: `Authorization: Bearer <jwt>`

**Pros:**
- ✅ More control over auth URL generation
- ✅ Can add custom parameters/validation
- ✅ Centralized configuration

## Key Differences

| Aspect | Browser Users | Mobile Users |
|--------|---------------|---------------|
| **Authentication** | Your social login redirect | PKCE OAuth |
| **Session Management** | Server-side cookies | Client-side JWT |
| **API Access** | Session-based | JWT Bearer |
| **Entry Point** | Frappe site | IdentityServer |
| **User Experience** | Redirect flow | In-app auth |
| **Storage** | Browser cookies | Secure mobile storage |

## Implementation Status

### ✅ **Completed Components**

1. **JWT Middleware** (`/auth/jwt_middleware.py`)
   - Intercepts `/api/*` requests with `Authorization: Bearer` headers
   - Validates JWT tokens via JWKS
   - Creates API sessions for authenticated users

2. **Discovery Endpoint** (`/api/jwt_api.mobile_api_info`)
   - Returns IdentityServer configuration
   - Provides recommended OAuth parameters
   - No authentication required

3. **Optional Auth URL Generator** (`/api/jwt_api.get_mobile_auth_url`)
   - Generates PKCE-compliant auth URLs
   - Handles code challenge generation
   - Alternative to direct IdentityServer integration

### 🔧 **Required IdentityServer Configuration**

You'll need to register the mobile app client in IdentityServer:

```csharp
// IdentityServer configuration
new Client
{
    ClientId = "**your_mobile_client_id**",
    ClientName = "TickTix Mobile App",
    
    AllowedGrantTypes = GrantTypes.Code,
    RequirePkce = true,
    RequireClientSecret = false, // Public client
    
    RedirectUris = { "com.yourapp://oauth/callback" },
    
    AllowedScopes = { "openid", "profile", "api" },
    
    // Allow all your tenant domains as audiences
    AllowedCorsOrigins = { "*" }, // Configure appropriately
    
    // Token lifetimes
    AccessTokenLifetime = 3600, // 1 hour
    RefreshTokenExpiration = TokenExpiration.Sliding,
    SlidingRefreshTokenLifetime = 2592000 // 30 days
}
```

## Mobile App Implementation Examples

The [`mobile_authentication_flows.md`](../mobile/mobile_authentication_flows.md) document contains complete implementation examples for:

- **React Native** with `react-native-app-auth`
- **Flutter** with `flutter_appauth`  
- **Python** for backend integrations
- **Native iOS/Android** patterns

## Security Notes

1. **JWT tokens are stateless** - No server session tracking
2. **Tokens should be stored securely** - Use Keychain (iOS) or Keystore (Android)
3. **Implement token refresh** - Handle expiration gracefully
4. **PKCE is required** - Prevents code interception attacks
5. **Validate SSL certificates** - Prevent MITM attacks

## Testing

Use these endpoints to test mobile integration:

```bash
# Test discovery
curl https://your-site.com/api/method/frappe_ticktix.api.v1.jwt_api.mobile_api_info

# Test JWT authentication (requires valid token)
curl -H "Authorization: Bearer **your_jwt_token_here**" \
     https://your-site.com/api/method/frappe_ticktix.api.v1.jwt_api.test_jwt_auth

# Health check
curl https://your-site.com/api/method/frappe_ticktix.api.v1.jwt_api.health_check
```

## Summary

✅ **Browser users continue using your existing social login enforcement**  
✅ **Mobile users get modern OAuth PKCE flow with JWT tokens**  
✅ **Both flows coexist without any conflicts**  
✅ **Zero impact on existing Frappe functionality**  
✅ **Complete mobile integration examples provided**