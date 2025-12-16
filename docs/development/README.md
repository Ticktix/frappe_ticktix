# Development

This folder contains technical documentation for developers working on the TickTix integration, migration guides, and advanced implementation details.

## Files in this folder

### 🔧 **[technical_details.md](technical_details.md)**
Low-level implementation details including:
- **Architecture overview**: System components and interactions
- **OAuth flow implementation**: Detailed technical flow
- **Database schema**: User mapping table structure
- **API endpoints**: Technical specifications
- **Configuration management**: Site config and settings
- **Error handling**: Exception management patterns

### 📦 **[feature_migration_guide.md](feature_migration_guide.md)**
Guide for migrating features from other systems:
- **Migration patterns**: Common migration scenarios
- **Code transformation**: Updating existing patterns
- **Best practices**: Avoiding common pitfalls
- **Testing strategies**: Validating migrated features
- **Integration considerations**: Working with existing systems

### 📋 **[one_fm_features_catalog.md](one_fm_features_catalog.md)**
Comprehensive catalog of One FM features and migration paths:
- **Feature inventory**: Complete list of One FM capabilities
- **Migration roadmap**: Priority and complexity assessment
- **Technical mapping**: How features map to Frappe TickTix
- **Custom field requirements**: Field mappings and customizations
- **Testing framework**: Validation approaches for each feature

## Development Topics

### 🏗️ **Architecture**
- **JWT Middleware**: Authentication layer implementation
- **User Mapping**: Social login integration patterns
- **Configuration Management**: Centralized settings approach
- **API Design**: RESTful endpoint patterns

### 🔄 **Integration Patterns**
- **OAuth 2.0**: IdentityServer integration
- **JWT Validation**: JWKS-based token verification
- **User Provisioning**: Automatic user creation
- **Role Mapping**: JWT claims to Frappe roles

### 🛠️ **Development Tools**
- **Verification Scripts**: Automated testing tools
- **CLI Utilities**: Command-line debugging
- **API Testing**: Endpoint validation
- **Configuration Validation**: Setup verification

## Code Organization

### Core Implementation
```
/frappe_ticktix/auth/
├── jwt_middleware.py      # Authentication middleware
├── jwt_validator.py       # JWT token validation
└── user_mapper.py         # User mapping logic

/frappe_ticktix/api/
├── jwt_api.py            # JWT testing endpoints
└── force_ticktix_login.py # Login enforcement
```

### Configuration
```
/sites/common_site_config.json  # JWT configuration
/frappe_ticktix/hooks.py        # Frappe hooks
```

## Development Workflow

### 1. **Setup Development Environment**
```bash
# Install in development mode
bench get-app frappe_ticktix
bench --site your-site install-app frappe_ticktix
```

### 2. **Enable Developer Mode**
```json
// In site_config.json
{
  "developer_mode": 1,
  "log_level": "DEBUG"
}
```

### 3. **Testing Changes**
```bash
# Run verification
```bash
python apps/frappe_ticktix/frappe_ticktix/utils/verify_cli.py
```

# Check logs
tail -f sites/your-site/logs/frappe.log
```

## Advanced Topics

### **Custom JWT Claims**
- Extending JWT validation
- Custom role mapping logic
- Additional claim processing

### **Multi-tenant Considerations**
- Site-specific configuration
- Tenant isolation patterns
- Shared IdentityServer usage

### **Performance Optimization**
- JWKS caching strategies
- Database query optimization
- Session management efficiency

### **Security Considerations**
- Token validation best practices
- User provisioning security
- API endpoint protection

## Migration Strategies

### **From Other OAuth Systems**
- Configuration mapping
- User data migration
- Role and permission mapping

### **From One FM**
- Feature inventory and assessment
- Gradual migration approach
- Data transformation patterns

### **Custom Implementations**
- Extending JWT middleware
- Custom user provisioning logic
- Advanced role mapping

## Related Documentation

- **Authentication**: [../authentication/](../authentication/) - Auth implementation details
- **Testing**: [../testing/verification_guide.md](../testing/verification_guide.md) - Development testing
- **Setup**: [../setup/setup_guide.md](../setup/setup_guide.md) - Development environment setup
- **Mobile**: [../mobile/](../mobile/) - API development for mobile