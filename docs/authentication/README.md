# Authentication

This folder contains documentation about authentication flows, JWT middleware, and security implementation.

## Files in this folder

### 🔄 **[authentication_flows_summary.md](authentication_flows_summary.md)**
Complete authentication architecture overview:
- **Browser Flow**: Traditional social login for desktop users
- **Mobile Flow**: JWT token-based API authentication
- **Flow separation**: How both coexist without conflicts
- **Implementation status**: What's completed and configured

### 🔐 **[jwt_authentication_guide.md](jwt_authentication_guide.md)**
JWT middleware setup and configuration:
- **Middleware architecture**: How JWT validation works
- **Configuration**: Setting up JWKS validation
- **User mapping**: JWT claims to Frappe users
- **API usage**: Bearer token authentication
- **Troubleshooting**: Common issues and solutions

## Authentication Flows

### Browser Users (Existing)
```
Desktop → Frappe Site → Social Login → IdentityServer → Session Cookies
```

### Mobile Users (New)
```
Mobile App → JWT Discovery → PKCE OAuth → JWT Token → API Calls
```

## Key Features

✅ **Dual Authentication**: Browser sessions + JWT tokens  
✅ **Zero Impact**: Existing functionality unchanged  
✅ **Security**: JWKS validation with RSA256 signatures  
✅ **Auto-provisioning**: Create users from JWT claims  
✅ **Role mapping**: JWT roles → Frappe roles  

## Implementation Components

- **JWT Middleware** (`/frappe_ticktix/auth/jwt_middleware.py`)
- **JWT Validator** (`/frappe_ticktix/auth/jwt_validator.py`)
- **User Mapper** (`/frappe_ticktix/auth/user_mapper.py`)

## Related Documentation

- **Mobile implementation**: [../mobile/](../mobile/)
- **Testing JWT**: [../testing/verification_guide.md](../testing/verification_guide.md)
- **Setup configuration**: [../setup/setup_guide.md](../setup/setup_guide.md)