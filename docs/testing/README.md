# Testing & Verification

This folder contains documentation for testing and verifying the TickTix OAuth integration.

## Files in this folder

### 🧪 **[verification_guide.md](verification_guide.md)**
Comprehensive testing guide covering:

#### **Verification Methods**
- **CLI Verification**: Standalone testing script
- **API Verification**: Web-based endpoints for integration testing
- **Manual Testing**: Step-by-step verification procedures

#### **Testing Scenarios**
- OAuth login flow verification
- User provisioning testing
- JWT token validation
- API endpoint functionality
- Error handling and edge cases

#### **Troubleshooting**
- Common issues and solutions
- Error code explanations
- Debugging techniques
- Log file analysis

## Testing Tools

### CLI Verification
```bash
# Run standalone verification
```bash
python apps/frappe_ticktix/frappe_ticktix/utils/verify_cli.py
```
```

### API Endpoints
| Endpoint | Purpose | Method |
|----------|---------|---------|
| `/api/method/frappe_ticktix.utils.verify_setup.quick_status` | System status | GET |
| `/api/method/frappe_ticktix.utils.verify_setup.verify_complete_integration` | Full verification | GET |
| `/api/method/frappe_ticktix.api.v1.jwt_api.health_check` | Health check | GET |

### JWT Testing
| Endpoint | Purpose | Auth Required |
|----------|---------|---------------|
| `/api/method/frappe_ticktix.api.v1.jwt_api.test_jwt_auth` | JWT validation | Yes |
| `/api/method/frappe_ticktix.api.v1.jwt_api.mobile_api_info` | Config info | No |

## Testing Checklist

### ✅ **Basic Integration**
- [ ] App installation successful
- [ ] OAuth configuration loaded
- [ ] Social login key configured
- [ ] IdentityServer connectivity

### ✅ **Authentication Flow**
- [ ] Browser login redirect works
- [ ] JWT token validation functional
- [ ] User mapping operational
- [ ] Session creation successful

### ✅ **API Functionality**
- [ ] JWT middleware active
- [ ] Bearer token authentication
- [ ] User profile retrieval
- [ ] Error handling proper

### ✅ **User Management**
- [ ] User provisioning works
- [ ] Role mapping functional
- [ ] Social login mapping
- [ ] Administrator access

## Common Test Scenarios

### 1. **First-time Setup**
```bash
# Test basic configuration
curl "http://your-site/api/method/frappe_ticktix.utils.verify_setup.quick_status"
```

### 2. **JWT Authentication**
```bash
# Test JWT endpoint (requires valid token)
curl -H "Authorization: Bearer **your_jwt_token_here**" \
     "http://your-site/api/method/frappe_ticktix.api.v1.jwt_api.test_jwt_auth"
```

### 3. **Mobile Discovery**
```bash
# Test mobile configuration discovery
curl "http://your-site/api/method/frappe_ticktix.api.v1.jwt_api.mobile_api_info"
```

## Debugging Tips

### Log Files
```bash
# Check Frappe logs for errors
tail -f sites/your-site/logs/frappe.log | grep -i "jwt\|oauth\|ticktix"

# Check bench logs
tail -f logs/bench.log
```

### Configuration Verification
```bash
# Check site configuration
cat sites/common_site_config.json | grep -i jwt
```

### Database Verification
```bash
# Check user mappings
bench --site your-site console
```

## Related Documentation

- **Setup**: [../setup/setup_guide.md](../setup/setup_guide.md) - Initial configuration
- **Authentication**: [../authentication/](../authentication/) - Understanding flows  
- **Mobile**: [../mobile/](../mobile/) - Mobile app testing
- **Development**: [../development/technical_details.md](../development/technical_details.md) - Technical debugging