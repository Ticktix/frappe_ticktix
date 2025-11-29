# Mobile Authentication Flows

> **🔒 Security Notice**: All client credentials in examples use `**placeholder**` format. Replace with your actual IdentityServer client configuration and store credentials securely.

## Overview
Mobile apps need a different approach than browser redirects. Here are two recommended patterns:

## Approach 1: Dir    // Build auth URL
    params = {
        'client_id': '**your_mobile_client_id**',
        'response_type': 'code',IdentityServer Integration (Recommended)

### Flow:
1. **User enters domain** → `your-site.com`
2. **App discovers IdentityServer** → Call discovery endpoint
3. **PKCE OAuth flow** → Direct to IdentityServer
4. **Get JWT token** → Use for API calls

### Implementation:

#### Step 1: Domain Discovery
```javascript
// React Native example
async function discoverIdentityServer(domain) {
  try {
    // Try to get IdentityServer config from Frappe site
    const response = await fetch(`https://${domain}/api/method/frappe_ticktix.api.jwt_api.mobile_api_info`);
    const data = await response.json();
    
    return {
      issuer: data.message.issuer, // https://login.ticktix.com
      audience: data.message.audience, // your-site.com
      authEndpoint: data.message.auth_endpoint,
      tokenEndpoint: data.message.token_endpoint
    };
  } catch (error) {
    // Fallback to standard TickTix IdentityServer
    return {
      issuer: 'https://login.ticktix.com',
      authEndpoint: 'https://login.ticktix.com/connect/authorize',
      tokenEndpoint: 'https://login.ticktix.com/connect/token'
    };
  }
}
```

#### Step 2: PKCE OAuth Flow
```javascript
import { authorize } from 'react-native-app-auth';

async function authenticateWithPKCE(domain) {
  const config = await discoverIdentityServer(domain);
  
  const authConfig = {
    issuer: config.issuer,
    clientId: '**your_mobile_client_id**', // Register this with IdentityServer
    redirectUrl: 'com.yourapp://oauth/callback',
    scopes: ['openid', 'profile', 'api'],
    additionalParameters: {
      audience: domain // Tell IdentityServer which site this is for
    }
  };

  try {
    const result = await authorize(authConfig);
    // result.accessToken is your JWT for API calls
    return {
      jwt: result.accessToken,
      refreshToken: result.refreshToken,
      domain: domain
    };
  } catch (error) {
    throw new Error('Authentication failed');
  }
}
```

#### Step 3: API Usage
```javascript
class TickTixMobileClient {
  constructor(domain, jwt) {
    this.baseUrl = `https://${domain}`;
    this.jwt = jwt;
  }

  async apiCall(endpoint, data = null) {
    const response = await fetch(`${this.baseUrl}/api/method/${endpoint}`, {
      method: data ? 'POST' : 'GET',
      headers: {
        'Authorization': `Bearer ${this.jwt}`,
        'Content-Type': 'application/json'
      },
      body: data ? JSON.stringify(data) : null
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }

    return response.json();
  }

  // Test the connection
  async testAuth() {
    return this.apiCall('frappe_ticktix.api.jwt_api.test_jwt_auth');
  }

  // Get user profile
  async getUserProfile() {
    return this.apiCall('frappe_ticktix.api.jwt_api.get_user_profile');
  }
}
```

## Approach 2: Frappe-Mediated Flow (Alternative)

If you want to route through your Frappe site first:

### Flow:
1. **User enters domain** → `your-site.com`
2. **App calls Frappe endpoint** → Get auth URL
3. **Open auth URL** → In-app browser or system browser
4. **Handle callback** → Extract token from redirect

### Implementation:

#### Step 1: Get Auth URL from Frappe
```javascript
async function getAuthUrl(domain) {
  const response = await fetch(`https://${domain}/api/method/frappe_ticktix.api.jwt_api.get_mobile_auth_url`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      redirect_uri: 'com.yourapp://oauth/callback',
      state: generateRandomState()
    })
  });
  
  const data = await response.json();
  return data.message.auth_url;
}
```

#### Step 2: Create Frappe Endpoint (Add this to jwt_api.py)
```python
@frappe.whitelist(allow_guest=True, methods=["POST"])
def get_mobile_auth_url():
    """Generate mobile auth URL for PKCE flow"""
    data = frappe.local.form_dict
    redirect_uri = data.get('redirect_uri')
    state = data.get('state')
    
    # Get JWT config
    config = get_jwt_config()
    
    # Generate PKCE parameters
    code_verifier = base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8').rstrip('=')
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode('utf-8')).digest()
    ).decode('utf-8').rstrip('=')
    
    # Store code_verifier temporarily (you'll need this for token exchange)
    frappe.cache().set(f"pkce_{state}", code_verifier, expires_in_sec=600)
    
    # Build auth URL
    params = {
        'client_id': 'mobile-app',
        'response_type': 'code',
        'scope': 'openid profile api',
        'redirect_uri': redirect_uri,
        'state': state,
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256',
        'audience': frappe.local.site
    }
    
    auth_url = f"{config.issuer}/connect/authorize?" + urlencode(params)
    
    return {'auth_url': auth_url}
```

## Recommended Libraries

### React Native
- `react-native-app-auth` - Best for PKCE OAuth flows
- `@react-native-async-storage/async-storage` - Secure token storage

### Flutter
- `flutter_appauth` - PKCE OAuth support
- `flutter_secure_storage` - Secure token storage

### Native iOS
- `ASWebAuthenticationSession` - System OAuth flow
- `Keychain Services` - Secure storage

### Native Android
- `Custom Tabs` - In-app browser for OAuth
- `EncryptedSharedPreferences` - Secure storage

## Security Considerations

1. **Never store JWT in plain text** - Use secure storage
2. **Implement token refresh** - Handle expiration gracefully  
3. **Validate SSL certificates** - Prevent man-in-the-middle attacks
4. **Use PKCE** - Prevents authorization code interception

## Complete Mobile Flow Example

```javascript
// Complete React Native implementation
export class TickTixMobile {
  async login(domain) {
    try {
      // Step 1: Discover IdentityServer
      const config = await this.discoverIdentityServer(domain);
      
      // Step 2: PKCE OAuth
      const auth = await this.authenticateWithPKCE(domain, config);
      
      // Step 3: Store securely
      await AsyncStorage.setItem('ticktix_jwt', auth.jwt);
      await AsyncStorage.setItem('ticktix_domain', domain);
      
      // Step 4: Test connection
      const client = new TickTixMobileClient(domain, auth.jwt);
      const profile = await client.getUserProfile();
      
      return { success: true, profile };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }
}
```

## Key Differences Summary

| Aspect | Browser Flow | Mobile Flow |
|--------|--------------|-------------|
| **Auth Method** | Redirect + Cookies | PKCE + JWT |
| **Entry Point** | Your Frappe site | IdentityServer directly |
| **Session Type** | Server-side session | Stateless JWT |
| **Storage** | Browser cookies | Secure mobile storage |
| **API Access** | Session-based | JWT Bearer token |

**Recommendation**: Use **Approach 1** (Direct IdentityServer) for better performance and standard OAuth mobile patterns.