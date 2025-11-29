# Mobile Integration

This folder contains documentation for integrating mobile applications with the TickTix OAuth system.

## Files in this folder

### 📱 **[mobile_authentication_flows.md](mobile_authentication_flows.md)**
Complete mobile app integration guide covering:

#### **Integration Approaches**
- **Approach 1**: Direct IdentityServer integration (Recommended)
- **Approach 2**: Frappe-mediated flow (Alternative)

#### **Platform Examples**
- **React Native**: Using `react-native-app-auth` with PKCE
- **Flutter**: Using `flutter_appauth` for OAuth flows  
- **Python**: Backend integration patterns
- **Native iOS/Android**: Platform-specific implementations

#### **Security Best Practices**
- PKCE OAuth flow implementation
- Secure token storage (Keychain/Keystore)
- SSL certificate validation
- Token refresh handling

## Mobile Authentication Flow

### Recommended Flow (Direct IdentityServer)
```
1. User enters domain (your-site.com)
2. App discovers IdentityServer config
3. PKCE OAuth flow with IdentityServer
4. App receives JWT token
5. API calls with Bearer authentication
```

### Key Benefits
✅ **Standard OAuth**: Industry best practices  
✅ **Offline Support**: Works after token acquisition  
✅ **Performance**: Fewer network hops  
✅ **Security**: PKCE prevents code interception  

## Implementation Libraries

### React Native
- `react-native-app-auth` - OAuth PKCE flows
- `@react-native-async-storage/async-storage` - Secure storage

### Flutter  
- `flutter_appauth` - OAuth integration
- `flutter_secure_storage` - Secure token storage

### Native Development
- **iOS**: `ASWebAuthenticationSession` + Keychain
- **Android**: Custom Tabs + EncryptedSharedPreferences

## API Endpoints for Mobile

| Endpoint | Purpose | Auth Required |
|----------|---------|---------------|
| `/api/method/frappe_ticktix.api.jwt_api.mobile_api_info` | Discovery | No |
| `/api/method/frappe_ticktix.api.jwt_api.test_jwt_auth` | Test auth | Yes |
| `/api/method/frappe_ticktix.api.jwt_api.get_user_profile` | User info | Yes |

## Next Steps

1. **Choose approach**: Direct vs Frappe-mediated
2. **Select platform**: React Native, Flutter, or Native
3. **Implement PKCE**: Follow platform examples
4. **Test integration**: Use JWT testing endpoints
5. **Handle errors**: Implement proper error handling

## Related Documentation

- **Authentication flows**: [../authentication/authentication_flows_summary.md](../authentication/authentication_flows_summary.md)
- **JWT setup**: [../authentication/jwt_authentication_guide.md](../authentication/jwt_authentication_guide.md)
- **Testing**: [../testing/verification_guide.md](../testing/verification_guide.md)