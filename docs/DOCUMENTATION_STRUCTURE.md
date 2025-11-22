# frappe_ticktix Documentation Structure

**Last Updated:** October 20, 2025  
**Status:** ✅ Current and Clean (Obsolete docs removed)

## Overview
All documentation has been reorganized into the `/docs` folder with logical subfolders for better organization and discoverability.

## 📁 Documentation Hierarchy

### � **Root Level**
- **[README.md](README.md)** - Main documentation index with navigation
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Technical overview and architecture
- **[DOCUMENTATION_STRUCTURE.md](DOCUMENTATION_STRUCTURE.md)** - This structure guide

### 🚀 **Setup & Configuration** ([setup/](setup/))
- **[setup_guide.md](setup/setup_guide.md)** - Complete installation and configuration guide
- **[requirements.md](setup/requirements.md)** - Login requirements and specifications (formerly loginRequirment.md)
- **[social_login_mapping_explanation.md](setup/social_login_mapping_explanation.md)** - User mapping between systems

### 🔐 **Authentication** ([authentication/](authentication/))
- **[authentication_flows_summary.md](authentication/authentication_flows_summary.md)** - Complete authentication architecture
- **[jwt_authentication_guide.md](authentication/jwt_authentication_guide.md)** - JWT middleware setup and configuration

### 📱 **Mobile Integration** ([mobile/](mobile/))
- **[mobile_authentication_flows.md](mobile/mobile_authentication_flows.md)** - Mobile app integration patterns
  - React Native examples with `react-native-app-auth`
  - Flutter examples with `flutter_appauth`
  - Native iOS/Android patterns
  - Security best practices

### 🧪 **Testing & Verification** ([testing/](testing/))
- **[verification_guide.md](testing/verification_guide.md)** - Testing OAuth integration
  - CLI verification tools
  - API testing endpoints
  - Troubleshooting guide

### 🎨 **User Interface** ([ui/](ui/))
- **[login_ui_improvements.md](ui/login_ui_improvements.md)** - Login page customization and branding

### 🔧 **Development** ([development/](development/))
- **[technical_details.md](development/technical_details.md)** - Low-level implementation details
- **[feature_migration_guide.md](development/feature_migration_guide.md)** - Migration from other systems
- **[one_fm_features_catalog.md](development/one_fm_features_catalog.md)** - Feature catalog and migration guide

## File Reorganization Summary

### ✅ **Moved to Subfolders**
| Original Location | New Location | Category |
|-------------------|--------------|-----------|
| `setup_guide.md` | `setup/setup_guide.md` | Setup & Config |
| `loginRequirment.md` | `setup/requirements.md` | Setup & Config |
| `social_login_mapping_explanation.md` | `setup/social_login_mapping_explanation.md` | Setup & Config |
| `jwt_authentication_guide.md` | `authentication/jwt_authentication_guide.md` | Authentication |
| `authentication_flows_summary.md` | `authentication/authentication_flows_summary.md` | Authentication |
| `mobile_authentication_flows.md` | `mobile/mobile_authentication_flows.md` | Mobile |
| `verification_guide.md` | `testing/verification_guide.md` | Testing |
| `login_ui_improvements.md` | `ui/login_ui_improvements.md` | UI/UX |
| `technical_details.md` | `development/technical_details.md` | Development |
| `feature_migration_guide.md` | `development/feature_migration_guide.md` | Development |
| `one_fm_features_catalog.md` | `development/one_fm_features_catalog.md` | Development |

### 📁 **New Subfolder Structure**
```
docs/
├── README.md                           # Main index
├── IMPLEMENTATION_SUMMARY.md            # Core technical overview  
├── DOCUMENTATION_STRUCTURE.md          # This guide
├── setup/                              # Setup & Configuration
│   ├── README.md
│   ├── setup_guide.md
│   ├── requirements.md
│   └── social_login_mapping_explanation.md
├── authentication/                     # Authentication & Security
│   ├── README.md
│   ├── authentication_flows_summary.md
│   └── jwt_authentication_guide.md
├── mobile/                            # Mobile Integration
│   ├── README.md
│   └── mobile_authentication_flows.md
├── testing/                           # Testing & Verification
│   ├── README.md
│   └── verification_guide.md
├── ui/                               # User Interface
│   ├── README.md
│   └── login_ui_improvements.md
└── development/                      # Development & Migration
    ├── README.md
    ├── technical_details.md
    ├── feature_migration_guide.md
    └── one_fm_features_catalog.md
```

### 🧹 **Clean Code Separation**
The `/frappe_ticktix/auth/` folder now contains only implementation code:
- `jwt_middleware.py` - Authentication middleware
- `jwt_validator.py` - JWT validation logic  
- `user_mapper.py` - User mapping functionality
- `__init__.py` - Module initialization

## Navigation Guide

### **For Setup & Installation**
1. Start with [README.md](README.md)
2. Follow [setup_guide.md](setup_guide.md)
3. Verify with [verification_guide.md](verification_guide.md)

### **For Mobile Development**
1. Read [authentication_flows_summary.md](authentication_flows_summary.md)
2. Implement using [mobile_authentication_flows.md](mobile_authentication_flows.md)
3. Test with [jwt_authentication_guide.md](jwt_authentication_guide.md)

### **For System Integration**
1. Review [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
2. Understand [social_login_mapping_explanation.md](social_login_mapping_explanation.md)
3. Check [technical_details.md](technical_details.md)

### **For Troubleshooting**
1. Use [verification_guide.md](verification_guide.md)
2. Check [technical_details.md](technical_details.md)
3. Review implementation files in `/frappe_ticktix/auth/`

## Benefits of This Structure

✅ **Centralized Documentation** - All docs in one location  
✅ **Clear Separation** - Code vs documentation  
✅ **Better Discoverability** - Logical organization  
✅ **Easier Maintenance** - Single source of truth  
✅ **Professional Structure** - Industry standard layout  

## Quick Reference

```bash
# View documentation
ls docs/

# Key files for different use cases:
docs/README.md                           # Start here
docs/setup_guide.md                      # Installation
docs/mobile_authentication_flows.md      # Mobile apps
docs/jwt_authentication_guide.md         # JWT setup
docs/verification_guide.md               # Testing

# Implementation code
frappe_ticktix/auth/jwt_middleware.py     # Core middleware
frappe_ticktix/auth/jwt_validator.py      # JWT validation
frappe_ticktix/auth/user_mapper.py        # User mapping
```