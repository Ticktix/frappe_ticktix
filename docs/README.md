# Frappe TickTix Documentation

## 📚 **Documentation Overview**

Welcome to the Frappe TickTix app documentation. This comprehensive guide covers everything from installation to advanced plugin development.

## 📖 **Document Index**

### **🏗️ Architecture & Implementation**
- **[Implementation Summary](IMPLEMENTATION_SUMMARY.md)** - Technical overview and current status  
- **[Current Structure](architecture/CURRENT_STRUCTURE.md)** - Complete overview of implemented architecture
- **[Future Roadmap](architecture/FUTURE_ROADMAP.md)** - Planned HR modules and enhancements
- **[Documentation Structure](DOCUMENTATION_STRUCTURE.md)** - Guide to all documentation

### **⚙️ Setup & Installation**
- **[Installation Guide](setup/INSTALLATION.md)** - New comprehensive setup guide  
- **[Setup Guide](setup/setup_guide.md)** - Original setup documentation
- **[Requirements](setup/requirements.md)** - Login requirements and specifications
- **[Social Login Mapping](setup/social_login_mapping_explanation.md)** - User mapping between systems

### **� Authentication & Security**
- **[Authentication Flows](authentication/authentication_flows_summary.md)** - Complete authentication architecture
- **[JWT Authentication Guide](authentication/jwt_authentication_guide.md)** - JWT middleware setup and configuration

### **�🔌 Plugin Development**  
- **[Development Guide](plugins/DEVELOPMENT_GUIDE.md)** - Complete guide for creating new plugins

### **🌐 API Documentation**
- **[API Reference](api/API_REFERENCE.md)** - Complete API endpoint documentation

### **📱 Mobile Integration**
- **[Mobile Authentication Flows](mobile/mobile_authentication_flows.md)** - Mobile app integration patterns

### **🧪 Testing & Verification**
- **[Verification Guide](testing/verification_guide.md)** - Testing OAuth integration and troubleshooting

### **🎨 User Interface**  
- **[Login UI Improvements](ui/login_ui_improvements.md)** - Login page customization and branding

### **🔧 Development & Migration**
- **[Technical Details](development/technical_details.md)** - Low-level implementation details
- **[Feature Migration Guide](development/feature_migration_guide.md)** - Migration from other systems

## 🎯 **Quick Start**

### **For New Users (Setup & Installation):**
1. **Start Here**: [Installation Guide](setup/INSTALLATION.md) - New comprehensive setup
2. **Alternative**: [Setup Guide](setup/setup_guide.md) - Original setup documentation  
3. **Verify**: [Verification Guide](testing/verification_guide.md) - Test your installation

### **For Administrators:**
1. **Overview**: [Implementation Summary](IMPLEMENTATION_SUMMARY.md) - Current system status
2. **Architecture**: [Current Structure](architecture/CURRENT_STRUCTURE.md) - What's implemented
3. **APIs**: [API Reference](api/API_REFERENCE.md) - Available endpoints
4. **Authentication**: [Authentication Flows](authentication/authentication_flows_summary.md) - Security setup

### **For Developers:**
1. **Architecture**: [Current Structure](architecture/CURRENT_STRUCTURE.md) - System overview
2. **Plugin Development**: [Development Guide](plugins/DEVELOPMENT_GUIDE.md) - Create new plugins
3. **Future Plans**: [Future Roadmap](architecture/FUTURE_ROADMAP.md) - Upcoming features
4. **Technical Details**: [Technical Details](development/technical_details.md) - Implementation specifics

### **For Mobile App Development:**
1. **Authentication**: [Mobile Authentication Flows](mobile/mobile_authentication_flows.md) - Mobile integration
2. **JWT Setup**: [JWT Authentication Guide](authentication/jwt_authentication_guide.md) - Token handling
3. **API Usage**: [API Reference](api/API_REFERENCE.md) - Mobile endpoints

### **For HR Module Development:**
1. **Roadmap**: [Future Roadmap](architecture/FUTURE_ROADMAP.md) - Phase 2A & 2B specifications
2. **Plugin Patterns**: [Development Guide](plugins/DEVELOPMENT_GUIDE.md) - Development guidelines  
3. **Architecture**: Check existing `plugins/authentication/` and `plugins/branding/` implementations
4. **Configuration**: Review `core/config_manager.py` for HR config support

## 📊 **Implementation Status**

### ✅ **Currently Implemented (Production Ready)**
- **Core Framework**: Configuration management, plugin system
- **Branding Plugin**: Logo management, external image caching
- **Authentication Plugin**: JWT, OAuth, social login
- **API Layer**: Mobile support, PKCE flow, health checks
- **Backward Compatibility**: All legacy imports maintained

### 🏗️ **Ready for Implementation**
- **HR Extensions Structure**: Plugin framework prepared
- **Employee ID Generation**: Configuration support ready
- **Extended Attendance**: Calendar hierarchy planned

### 🚀 **Future Phases**
- **Advanced Plugin System**: Base classes, auto-discovery
- **Payroll Extensions**: Custom allowances and deductions  
- **Performance Management**: Appraisal workflows
- **Leave Management**: Complex policies and approvals

## 🔧 **Configuration Files**

### **Site-Specific Config** (`site_config.json`)
```json
{
  "ticktix_client_id": "your_client_id",
  "ticktix_client_secret": "your_secret",
  "company_logo": "https://your-logo-url.jpg"
}
```

### **Global Config** (`common_site_config.json`)
```json
{
  "jwt_enabled": true,
  "hr_employee_id_patterns": {
    "default": "EMP-{YYYY}-{####}"
  },
  "hr_attendance_rules": {
    "enable_client_dayoff": true
  }
}
```

## 🧪 **Testing**

### **Verification Commands:**
```bash
# Test core functionality
bench --site your-site.local execute frappe_ticktix.core.config_manager.get_branding_config

# Test authentication
bench --site your-site.local execute frappe_ticktix.api.v1.jwt_api.health_check

# Run full test suite
bench --site your-site.local run-tests --app frappe_ticktix
```

### **Build Process:**
```bash
# Build assets
bench build --app frappe_ticktix

# Expected result: ✅ ~250ms build time
```

## 📋 **Development Workflow**

### **1. Understanding the System**
- Read [Current Structure](architecture/CURRENT_STRUCTURE.md) to understand what's implemented
- Review plugin examples in `plugins/branding/` and `plugins/authentication/`
- Check configuration patterns in `core/config_manager.py`

### **2. Creating New Plugins**
- Follow [Development Guide](plugins/DEVELOPMENT_GUIDE.md) for plugin creation
- Use existing plugins as templates
- Integrate with `config_manager.py` for settings

### **3. HR Module Development**
- Reference [Future Roadmap](architecture/FUTURE_ROADMAP.md) for detailed specifications
- Create plugins in `plugins/hr_extensions/employee_id/` or `plugins/hr_extensions/attendance/`
- Follow configuration patterns for HR settings

### **4. Testing & Deployment**
- Create unit tests following existing patterns
- Use [Installation Guide](setup/INSTALLATION.md) for deployment
- Reference [API Documentation](api/API_REFERENCE.md) for endpoint testing

## 🔗 **Plugin Architecture**

The current plugin system provides:

### **✅ Implemented Features**
- **Modular Structure**: Isolated plugin directories
- **Configuration Integration**: Centralized config management  
- **Backward Compatibility**: Legacy import support
- **API Integration**: Plugin-specific endpoints
- **Testing Framework**: Comprehensive test patterns

### **🏗️ Framework Ready For**
- **HR Employee ID Generation**: Pattern-based ID creation
- **Extended Attendance Rules**: Client day-offs, custom weekly offs
- **Calendar Management**: Multi-level holiday calendars
- **Workflow Integration**: Approval processes and notifications

## 💡 **Key Concepts**

### **Configuration Hierarchy**
1. **Site Config** (`site_config.json`) - Site-specific settings
2. **Common Config** (`common_site_config.json`) - Global defaults
3. **Plugin Defaults** - Hardcoded fallbacks in code

### **Plugin Integration**
- **Import Path**: `frappe_ticktix.plugins.plugin_name.module`
- **Configuration**: Via `config_manager.get_config_value()`
- **Hooks**: Registered in main `hooks.py` file
- **APIs**: Exposed through standard Frappe whitelisting

### **Backward Compatibility**
- **Legacy Paths**: Old import paths redirected to new locations
- **API Stability**: All existing endpoints maintained
- **Hook System**: Frappe hooks use original paths (cannot be changed)

## 📞 **Support & Development**

### **For Questions:**
1. Check relevant documentation section first
2. Review existing plugin implementations
3. Test with provided examples and commands
4. Consult API documentation for endpoint details

### **For HR Module Development:**
- Use [Future Roadmap](architecture/FUTURE_ROADMAP.md) as specification
- Follow [Development Guide](plugins/DEVELOPMENT_GUIDE.md) patterns
- Leverage existing `core/config_manager.py` for configuration
- Reference `plugins/authentication/` for complex plugin examples

### **For Advanced Customization:**
- Study the complete [Current Structure](architecture/CURRENT_STRUCTURE.md)
- Understand backward compatibility requirements
- Follow established patterns for new feature development
- Maintain configuration-driven approach for flexibility

---

**Status**: Documentation reflects current implementation as of October 2025. All described features are tested and functional.