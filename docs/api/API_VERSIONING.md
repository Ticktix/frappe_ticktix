# API Versioning Strategy for TickTix Integration

## Overview
This document outlines the API versioning strategy for the TickTix Frappe integration. Since this is a new custom app without existing mobile integrations, we've simplified the structure to focus on clean, maintainable code.

## Current Structure

### API Organization
```
apps/frappe_ticktix/frappe_ticktix/api/
├── __init__.py          # Main API entry point with v1 imports
├── jwt_api.py           # JWT validation endpoints (imports from v1)
└── v1/
    ├── __init__.py      # Authentication endpoints (login, callback)
    └── jwt_api.py       # JWT validation implementation
```

### Version 1 (v1) - Current Implementation
- **Path**: `/api/v1/`
- **Purpose**: Initial API implementation supporting JWT authentication
- **Endpoints**:
  - `ticktix_login()` - OAuth login initiation
  - `login_callback()` - OAuth callback handler
  - `validate_jwt()` - JWT token validation
  - `get_jwt_public_keys()` - JWKS endpoint access

### Configuration Management
All API endpoints use the centralized ConfigManager for configuration access:
```python
from frappe_ticktix.config_manager import get_config_manager

config_manager = get_config_manager()
auth_config = config_manager.get_auth_config()
```

## Future Versioning Guidelines

### When to Create a New Version
Create a new API version when:
1. **Breaking Changes**: Modifying existing endpoint signatures or behavior
2. **Authentication Changes**: Altering JWT validation logic or OAuth flow
3. **Configuration Structure**: Changing how configuration is accessed or structured
4. **Mobile App Requirements**: Supporting new mobile app features that require different endpoints

### Version Creation Process

#### 1. Create New Version Directory
```bash
mkdir apps/frappe_ticktix/frappe_ticktix/api/v2
```

#### 2. Copy and Modify Endpoints
```bash
cp apps/frappe_ticktix/frappe_ticktix/api/v1/__init__.py apps/frappe_ticktix/frappe_ticktix/api/v2/__init__.py
cp apps/frappe_ticktix/frappe_ticktix/api/v1/jwt_api.py apps/frappe_ticktix/frappe_ticktix/api/v2/jwt_api.py
```

#### 3. Update Main API Entry Points
Update `/api/__init__.py` to include new version imports:
```python
# Current API (v1) - maintain for backward compatibility
from .v1 import ticktix_login, login_callback

# New API (v2) - new endpoints
from .v2 import ticktix_login_v2, login_callback_v2
```

#### 4. Update JWT API Entry Point
Update `/api/jwt_api.py` to route to appropriate version:
```python
# Import from latest stable version
from .v2.jwt_api import validate_jwt, get_jwt_public_keys
```

### Endpoint Naming Conventions

#### Version-Specific Endpoints
When creating breaking changes, append version suffix:
- `ticktix_login()` → `ticktix_login_v2()`
- `login_callback()` → `login_callback_v2()`
- `validate_jwt()` → `validate_jwt_v2()`

#### Backward Compatibility
Maintain previous version endpoints for at least one major release:
```python
# v1 endpoints (deprecated)
@frappe.whitelist(allow_guest=True)
def ticktix_login(redirect_to=None, tenant=None, mobile=None):
    frappe.msgprint("Warning: v1 API deprecated. Please upgrade to v2.")
    return ticktix_login_v2(redirect_to, tenant, mobile)
```

### Configuration Versioning

#### Current Configuration Structure
All versions should use ConfigManager for consistent configuration access:
```python
from frappe_ticktix.config_manager import get_config_manager

config_manager = get_config_manager()
auth_config = config_manager.get_auth_config()
api_config = config_manager.get_api_config()
```

#### Version-Specific Configuration
If different versions require different configuration structures:
```python
# In config_manager.py
def get_auth_config_v2(self):
    """Get auth configuration for API v2 with enhanced security."""
    base_config = self.get_auth_config()
    # Add v2-specific enhancements
    return base_config
```

### Mobile App Integration

#### Current Mobile Flow
1. App requests login: `GET /api/method/frappe_ticktix.api.ticktix_login`
2. User authenticates via IdentityServer
3. Callback processes: `GET /api/method/frappe_ticktix.api.login_callback`
4. JWT validation: `POST /api/method/frappe_ticktix.api.v1.jwt_api.validate_jwt`

#### Future Mobile Versions
When supporting new mobile app versions:
1. Create new API version (v2, v3, etc.)
2. Update mobile app to use versioned endpoints
3. Maintain backward compatibility for older app versions
4. Document migration path for mobile developers

### Documentation Updates

#### Version Documentation
Each version should include:
1. **CHANGELOG.md** - Version-specific changes
2. **API_REFERENCE.md** - Endpoint documentation
3. **MIGRATION_GUIDE.md** - Upgrade instructions

#### Example Version Documentation Structure
```
docs/
├── api/
│   ├── v1/
│   │   ├── endpoints.md
│   │   └── migration-from-legacy.md
│   ├── v2/
│   │   ├── endpoints.md
│   │   ├── migration-from-v1.md
│   │   └── breaking-changes.md
│   └── versioning-policy.md
```

### Testing Strategy

#### Version-Specific Tests
Maintain separate test suites for each API version:
```
tests/
├── api/
│   ├── test_v1_auth.py
│   ├── test_v1_jwt.py
│   ├── test_v2_auth.py
│   └── test_v2_jwt.py
```

#### Cross-Version Integration Tests
Ensure compatibility between versions:
```python
def test_v1_to_v2_migration():
    """Test that v1 endpoints properly redirect to v2."""
    # Test backward compatibility
    pass

def test_configuration_compatibility():
    """Test that all versions work with current config structure."""
    # Test config manager compatibility
    pass
```

### Deprecation Policy

#### Deprecation Timeline
1. **Release N**: New version introduced alongside existing version
2. **Release N+1**: Previous version marked as deprecated with warnings
3. **Release N+2**: Previous version removed (breaking change release)

#### Deprecation Warnings
```python
@frappe.whitelist(allow_guest=True)
def deprecated_endpoint():
    frappe.log_error(
        "Deprecated API endpoint used", 
        "API Deprecation Warning"
    )
    # Add response header for API consumers
    frappe.local.response["X-API-Deprecated"] = "true"
    frappe.local.response["X-API-Deprecated-Version"] = "v1"
    frappe.local.response["X-API-Migration-Guide"] = "/docs/api/v2/migration"
```

## Best Practices

### 1. Configuration Management
- Always use ConfigManager for configuration access
- Never use `frappe.conf.get()` directly in API endpoints
- Maintain configuration backward compatibility when possible

### 2. Error Handling
- Provide clear error messages with version information
- Include migration guidance in deprecation warnings
- Log API usage for monitoring adoption of new versions

### 3. Security Considerations
- Validate JWT tokens using version-appropriate logic
- Maintain security standards across all API versions
- Regularly audit and update authentication mechanisms

### 4. Performance
- Monitor API performance across versions
- Optimize based on usage patterns
- Consider caching strategies for frequently accessed endpoints

## Implementation Notes

### Current Status
- ✅ V1 API implemented with ConfigManager integration
- ✅ Backward compatibility layer removed (new custom app)
- ✅ Clean API structure established
- ✅ JWT authentication working with proper configuration hierarchy

### Next Steps for Future Versions
1. Monitor mobile app requirements and user feedback
2. Plan v2 based on identified limitations or enhancements needed
3. Implement versioning infrastructure when first breaking change is required
4. Establish automated testing for cross-version compatibility

This strategy ensures clean, maintainable code while providing a clear path for future API evolution as the TickTix integration grows and mobile app requirements evolve.