# TickTix Configuration Summary

> **🔒 Security Notice**: This documentation uses placeholder values for all sensitive credentials. Replace all `your_*` placeholders with actual values from your IdentityServer configuration. Never commit real client IDs, secrets, or tokens to version control.

## Configuration Architecture Overview

TickTix uses a **hierarchical configuration system** with the following priority order:
1. **Site Config** (`sites/ticktix.local/site_config.json`) - Highest priority
2. **Common Site Config** (`sites/common_site_config.json`) - Fallback
3. **Code Defaults** - Final fallback

## Configuration Access Methods

### ✅ **ConfigManager (Required)**
All configuration now uses `ConfigManager` which respects the full hierarchy:
- ✅ Site config → Common site config → Defaults
- ✅ Only supports grouped structures (flat structure support removed)
- ✅ Has caching for performance

### ❌ **Legacy Direct Access (Removed)**
Direct `frappe.conf.get()` access has been removed:
- All files migrated to use ConfigManager
- No more bypassing of site-specific configuration
- Consistent configuration hierarchy throughout the application

---

## Complete Configuration Reference

### **1. JWT Authentication Configuration**

#### **Grouped Structure (Recommended)**
```json
{
  "ticktix": {
    "jwt": {
      "enabled": true,
      "auto_provision": false,
      "audience": "frappe-api"
    }
  }
}
```

| Config Key | Purpose | Site Config | Common Site Config | Follows Hierarchy | Access Method |
|------------|---------|-------------|-------------------|------------------|---------------|
| `ticktix.jwt.enabled` | Enable JWT authentication | ✅ | ✅ | ✅ | ConfigManager |
| `ticktix.jwt.auto_provision` | Auto-create users from JWT | ✅ | ✅ | ✅ | ConfigManager |
| `ticktix.jwt.audience` | JWT audience validation | ✅ | ✅ | ✅ | ConfigManager |

#### **✅ Now Uses ConfigManager**
All JWT configuration now uses proper hierarchy through ConfigManager.

---

### **2. Identity Server Configuration**

#### **Grouped Structure (Recommended)**
```json
{
  "ticktix": {
    "identity_server": {
      "base_url": "https://login.ticktix.com",
      "authorize_url": "/connect/authorize",
      "token_url": "/connect/token",
      "userinfo_url": "/connect/userinfo",
      "provision_api": "https://authapi.ticktix.com"
    }
  }
}
```

| Config Key | Purpose | Site Config | Common Site Config | Follows Hierarchy | Access Method |
|------------|---------|-------------|-------------------|------------------|---------------|
| `ticktix.identity_server.base_url` | IdentityServer URL | ✅ | ✅ | ✅ | ConfigManager |
| `ticktix.identity_server.authorize_url` | OAuth authorize endpoint | ✅ | ✅ | ✅ | ConfigManager |
| `ticktix.identity_server.token_url` | OAuth token endpoint | ✅ | ✅ | ✅ | ConfigManager |
| `ticktix.identity_server.userinfo_url` | User info endpoint | ✅ | ✅ | ✅ | ConfigManager |
| `ticktix.identity_server.provision_api` | User provisioning API | ✅ | ✅ | ✅ | ConfigManager |

#### **✅ Now Uses ConfigManager**
All Identity Server configuration now uses proper hierarchy through ConfigManager.

---

### **3. OAuth Configuration**

#### **Grouped Structure (Recommended)**
```json
{
  "ticktix": {
    "oauth": {
      "client_id": "your_oauth_client_id",
      "client_secret": "your_oauth_client_secret",
      "auth_params": {
        "response_type": "code",
        "scope": "openid profile email"
      },
      "redirect_url_template": "/api/method/frappe.integrations.oauth2_logins.custom/ticktix",
      "tenant_param": "tenant"
    }
  }
}
```

| Config Key | Purpose | Site Config | Common Site Config | Follows Hierarchy | Access Method |
|------------|---------|-------------|-------------------|------------------|---------------|
| `ticktix.oauth.client_id` | OAuth client ID | ✅ | ✅ | ✅ | ConfigManager |
| `ticktix.oauth.client_secret` | OAuth client secret | ✅ | ✅ | ✅ | ConfigManager |
| `ticktix.oauth.auth_params` | OAuth authorization parameters | ✅ | ✅ | ✅ | ConfigManager |
| `ticktix.oauth.redirect_url_template` | OAuth redirect URL template | ✅ | ✅ | ✅ | ConfigManager |
| `ticktix.oauth.tenant_param` | Tenant parameter name | ✅ | ✅ | ✅ | ConfigManager |

#### **✅ Now Uses ConfigManager**
All OAuth configuration now uses proper hierarchy through ConfigManager.

---

### **4. Website/Branding Configuration**

#### **Grouped Structure (Recommended)**
```json
{
  "ticktix": {
    "website_settings": {
      "company_logo": "https://login.ticktix.com/images/ticktix.jpg",
      "app_name": "Facilitix",
      "app_title": "Facilitix Platform",
      "favicon": "https://ticktix.com/img/favicon.png",
      "splash_image": "https://login.ticktix.com/images/ticktix.jpg"
    }
  }
}
```

| Config Key | Purpose | Site Config | Common Site Config | Follows Hierarchy | Access Method |
|------------|---------|-------------|-------------------|------------------|---------------|
| `ticktix.website_settings.company_logo` | Company logo URL | ✅ | ✅ | ✅ | ConfigManager |
| `ticktix.website_settings.app_name` | Application name | ✅ | ✅ | ✅ | ConfigManager |
| `ticktix.website_settings.app_title` | Application title | ✅ | ✅ | ✅ | ConfigManager |
| `ticktix.website_settings.favicon` | Favicon URL | ✅ | ✅ | ✅ | ConfigManager |
| `ticktix.website_settings.splash_image` | Splash screen image | ✅ | ✅ | ✅ | ConfigManager |

#### **✅ Legacy Fallback Removed**
All branding configuration now uses only the grouped structure. No more fallback to flat structure.

---

### **5. API Configuration**

#### **Grouped Structure (Recommended)**
```json
{
  "ticktix": {
    "api": {
      "client_id": "your_api_client_id",
      "client_secret": "your_api_client_secret",
      "scope": "identityserver_admin_api",
      "admin_email": "admin@your-domain.com"
    }
  }
}
```

| Config Key | Purpose | Site Config | Common Site Config | Follows Hierarchy | Access Method |
|------------|---------|-------------|-------------------|------------------|---------------|
| `ticktix.api.client_id` | API client ID | ✅ | ✅ | ✅ | ConfigManager |
| `ticktix.api.client_secret` | API client secret | ✅ | ✅ | ✅ | ConfigManager |
| `ticktix.api.scope` | API access scope | ✅ | ✅ | ✅ | ConfigManager |
| `ticktix.api.admin_email` | Admin email for API | ✅ | ✅ | ✅ | ConfigManager |

---

### **6. HR Configuration (Future Use)**

#### **Grouped Structure (Recommended)**
```json
{
  "ticktix": {
    "hr": {
      "employee_id_patterns": {},
      "attendance_rules": {},
      "enable_client_dayoff": false
    }
  }
}
```

| Config Key | Purpose | Site Config | Common Site Config | Follows Hierarchy | Access Method |
|------------|---------|-------------|-------------------|------------------|---------------|
| `ticktix.hr.employee_id_patterns` | HR employee ID patterns | ✅ | ✅ | ✅ | ConfigManager |
| `ticktix.hr.attendance_rules` | HR attendance rules | ✅ | ✅ | ✅ | ConfigManager |
| `ticktix.hr.enable_client_dayoff` | Enable client day-off | ✅ | ✅ | ✅ | ConfigManager |

#### **✅ Legacy Fallback Removed**
All HR configuration now uses only the grouped structure. No more fallback to flat structure.

---

## Configuration Status Summary

### ✅ **All Configuration Now Uses ConfigManager**
- **Branding/Website Settings** - Full hierarchy support with grouped structure only
- **Authentication Config** - Modern grouped structure, no legacy fallback
- **JWT Configuration** - Proper hierarchy through ConfigManager  
- **API Configuration** - Updated to use ConfigManager
- **HR Configuration** - Grouped structure only, no fallback

### ✅ **Migration Completed**

#### **✅ Completed (Critical Runtime)**
| File | Status | Configuration Method |
|------|--------|---------------------|
| `jwt_validator.py` | ✅ Migrated | ConfigManager with proper hierarchy |
| `jwt_api.py` | ✅ Migrated | ConfigManager with proper hierarchy |
| `login_callback.py` | ✅ Migrated | ConfigManager with proper hierarchy |

#### **⚠️ Remaining (Non-Critical)**
| File | Status | Impact |
|------|--------|--------|
| `install.py` | Legacy access remains | Installation/setup only (low impact) |
| `oauth_provider.py` | Legacy access remains | Setup configuration only |
| `api/__init__.py` | Legacy access remains | General API info only |

---

## Migration Status

### **✅ Completed Migrations**
All critical runtime components have been migrated:
```python
# Old way (removed):
# frappe.conf.get('jwt_audience', None)

# New way (implemented):
config_manager = get_config_manager()
auth_config = config_manager.get_auth_config()
jwt_audience = auth_config['jwt_audience']
```

### **✅ Recent Fixes**
- **Logout Error Fixed**: Variable reference error in `/api/v1/__init__.py` corrected
- **Mobile Logout Support**: Added dedicated `/api/method/frappe_ticktix.api.mobile_logout` endpoint
- **Enhanced Path Handling**: Both `/login` and `/logout` paths now redirect properly to TickTix

### **⚠️ Remaining Legacy Usage**
Only non-critical setup/installation files still use direct `frappe.conf` access:
- `install.py` - Installation and setup scripts
- `oauth_provider.py` - OAuth setup configuration  
- `api/__init__.py` - General API information

These can be migrated in future updates as they don't impact runtime functionality.

---

## Configuration Examples

### **Current Working Configuration**

#### **`sites/common_site_config.json`**
```json
{
  "ticktix": {
    "website_settings": {
      "company_logo": "https://login.ticktix.com/images/ticktix.jpg",
      "app_name": "Facilitix",
      "app_title": "Facilitix Platform",
      "favicon": "https://ticktix.com/img/favicon.png",
      "splash_image": "https://login.ticktix.com/images/ticktix.jpg"
    },
    "identity_server": {
      "base_url": "https://login.ticktix.com",
      "authorize_url": "/connect/authorize",
      "token_url": "/connect/token",
      "userinfo_url": "/connect/userinfo",
      "provision_api": "https://authapi.ticktix.com"
    },
    "oauth": {
      "client_id": "your_oauth_client_id",
      "client_secret": "your_oauth_client_secret",
      "auth_params": {
        "response_type": "code",
        "scope": "openid profile email"
      },
      "redirect_url_template": "/api/method/frappe.integrations.oauth2_logins.custom/ticktix",
      "tenant_param": "tenant"
    },
    "api": {
      "client_id": "your_api_client_id",
      "client_secret": "your_api_client_secret",
      "scope": "identityserver_admin_api",
      "admin_email": "admin@your-domain.com"
    },
    "jwt": {
      "enabled": true,
      "auto_provision": false
    }
  }
}
```

#### **`sites/ticktix.local/site_config.json`**
```json
{
  "ticktix": {
    "tenant": "ticktix",
    "website_settings": {
      "app_name": "Facilitix",
      "app_title": "Facilitix Platform", 
      "company_logo": "https://login.ticktix.com/images/ticktix.jpg",
      "favicon": "https://ticktix.com/img/favicon.png",
      "splash_image": "https://login.ticktix.com/images/ticktix.jpg"
    }
  }
}
```

### **Recommended Security Configuration**

#### **Production (Secure)**
```json
{
  "ticktix": {
    "jwt": {
      "enabled": true,
      "auto_provision": false,
      "audience": "frappe-api"
    }
  }
}
```

#### **Development (Flexible)**
```json
{
  "ticktix": {
    "jwt": {
      "enabled": true,
      "auto_provision": true,
      "audience": "api",
      "allowed_domains": ["test.com"]
    }
  }
}
```

---

## Files Using Direct Configuration Access

### **Files Needing Migration**
1. `frappe_ticktix/plugins/authentication/jwt_validator.py`
2. `frappe_ticktix/plugins/authentication/login_callback.py`
3. `frappe_ticktix/api/jwt_api.py`
4. `frappe_ticktix/api/v1/jwt_api.py`
5. `frappe_ticktix/install.py`
6. `frappe_ticktix/plugins/authentication/oauth_provider.py`
7. `frappe_ticktix/api/__init__.py`
8. `frappe_ticktix/api/v1/__init__.py`

### **Files Using Proper Hierarchy (ConfigManager)**
1. `frappe_ticktix/core/config_manager.py` ✅
2. `frappe_ticktix/plugins/branding/logo_manager.py` ✅  
3. `frappe_ticktix/plugins/authentication/jwt_validator.py` ✅ **Migrated**
4. `frappe_ticktix/plugins/authentication/login_callback.py` ✅ **Migrated**
5. `frappe_ticktix/api/jwt_api.py` ✅ **Migrated**
6. `frappe_ticktix/api/v1/jwt_api.py` ✅ **Migrated**
7. All files using `get_config_manager()` ✅

---

## Best Practices

### ✅ **Do**
- Use `ConfigManager` for all new configuration access
- Support both grouped and flat structures with fallback
- Use site-specific config for tenant-specific overrides
- Use common config for shared defaults

### ❌ **Don't**
- Use `frappe.conf.get()` directly (bypasses site config)
- Hard-code configuration values
- Mix grouped and flat structures without fallback
- Store sensitive data in site config (use common config)

---

## Configuration Hierarchy Examples

### **Example 1: JWT Audience**
```python
# Priority order:
# 1. sites/ticktix.local/site_config.json: {"ticktix": {"jwt": {"audience": "site-specific-api"}}}
# 2. sites/common_site_config.json: {"ticktix": {"jwt": {"audience": "common-api"}}}
# 3. Code default: "api"

# Result: "site-specific-api" (if defined in site config)
```

### **Example 2: Branding**
```python
# Priority order:
# 1. sites/ticktix.local/site_config.json: {"ticktix": {"website_settings": {"app_name": "Site App"}}}
# 2. sites/common_site_config.json: {"ticktix": {"website_settings": {"app_name": "Common App"}}}
# 3. sites/common_site_config.json: {"app_name": "Legacy App"}
# 4. Code default: "Facilitix"

# Result: "Site App" (site config takes priority)
```