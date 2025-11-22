# Frappe TickTix Setup and Installation Guide

## 📦 **Installation**

### **Prerequisites:**
- Frappe Bench installed and configured
- Frappe Framework v15.x or higher
- Python 3.8+
- Node.js 18+ and Yarn
- MySQL/MariaDB database

### **Installation Steps:**

#### **1. Get the App:**
```bash
# Clone from repository
bench get-app https://github.com/your-org/frappe_ticktix.git

# Or if you have local development
bench get-app /path/to/frappe_ticktix
```

#### **2. Install on Site:**
```bash
# Install the app
bench --site your-site.local install-app frappe_ticktix

# Migrate database
bench --site your-site.local migrate

# Build assets
bench build --app frappe_ticktix
```

#### **3. Restart Services:**
```bash
bench restart
```

## ⚙️ **Configuration**

### **Basic Configuration:**

Create or update `sites/your-site.local/site_config.json`:

```json
{
  "db_name": "your_site_db",
  "db_password": "your_db_password",
  
  "ticktix_client_id": "your_ticktix_client_id",
  "ticktix_client_secret": "your_ticktix_client_secret",
  "ticktix_base_url": "https://login.ticktix.com",
  
  "jwt_enabled": true,
  "jwt_audience": "api",
  "jwt_auto_provision": false,
  
  "company_logo": "https://login.ticktix.com/images/ticktix.jpg",
  "app_name": "Facilitix",
  "app_title": "Facilitix Platform",
  "favicon": "https://ticktix.com/img/favicon.png",
  "splash_image": "https://login.ticktix.com/images/ticktix.jpg"
}
```

### **Advanced Configuration:**

For multi-site setup, use `sites/common_site_config.json`:

```json
{
  "ticktix_client_id": "shared_client_id",
  "ticktix_client_secret": "shared_client_secret",
  "ticktix_base_url": "https://login.ticktix.com",
  "ticktix_authorize_url": "/connect/authorize",
  "ticktix_token_url": "/connect/token",
  
  "jwt_enabled": true,
  "jwt_audience": "api",
  "jwt_auto_provision": false,
  
  "company_logo": "https://login.ticktix.com/images/ticktix.jpg",
  "app_name": "Facilitix",
  "app_title": "Facilitix Platform",
  "favicon": "https://ticktix.com/img/favicon.png",
  "splash_image": "https://login.ticktix.com/images/ticktix.jpg",
  
  "hr_employee_id_patterns": {
    "default": "EMP-{YYYY}-{####}",
    "department_based": {
      "IT": "IT-{YY}-{####}",
      "HR": "HR-{YY}-{####}"
    }
  },
  
  "hr_attendance_rules": {
    "enable_client_dayoff": true,
    "enable_custom_weekly_off": true,
    "client_holiday_priority": true
  }
}
```

## 🔐 **OAuth Configuration**

### **TickTix Identity Server Setup:**

1. **Register Application** in TickTix Identity Server:
   - Application Type: Web Application
   - Redirect URIs: `https://your-site.com/api/method/frappe.integrations.oauth2_logins.custom/ticktix`
   - Allowed Scopes: `openid`, `profile`, `email`, `api`

2. **Configure Client Credentials:**
   - Note down `client_id` and `client_secret`
   - Add to your site configuration

3. **Test Configuration:**
   ```bash
   bench --site your-site.local execute frappe_ticktix.auth.jwt_validator.test_jwt_config
   ```

## 📱 **Mobile App Configuration**

### **Additional OAuth Setup for Mobile:**

```json
{
  "mobile_client_config": {
    "client_id": "mobile-app",
    "redirect_uri_scheme": "com.yourapp://oauth/callback",
    "scopes": ["openid", "profile", "api"],
    "pkce_enabled": true
  }
}
```

### **Test Mobile Integration:**
```bash
# Get mobile API info
curl https://your-site.com/api/method/frappe_ticktix.api.jwt_api.mobile_api_info

# Generate mobile auth URL
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"redirect_uri": "com.yourapp://oauth/callback", "state": "test123"}' \
     https://your-site.com/api/method/frappe_ticktix.api.jwt_api.get_mobile_auth_url
```

## 🧪 **Verification**

### **Test Installation:**

```bash
# Test core functionality
bench --site your-site.local execute frappe_ticktix.core.config_manager.get_branding_config

# Test authentication
bench --site your-site.local execute frappe_ticktix.api.jwt_api.health_check

# Test OAuth providers
bench --site your-site.local execute frappe_ticktix.plugins.authentication.oauth_provider.get_social_login_providers
```

### **Test Web Interface:**

1. **Visit Login Page**: `https://your-site.com/login`
   - Should show TickTix login button
   - Custom branding should be applied

2. **Test OAuth Flow**:
   - Click "Login with TickTix"
   - Should redirect to TickTix Identity Server
   - After login, should redirect back and create/login user

3. **Test API Endpoints**:
   ```bash
   # Health check
   curl https://your-site.com/api/method/frappe_ticktix.api.jwt_api.health_check
   
   # Mobile info
   curl https://your-site.com/api/method/frappe_ticktix.api.jwt_api.mobile_api_info
   ```

## 🔧 **Development Setup**

### **Local Development:**

```bash
# Setup development environment
cd /path/to/frappe-bench
bench get-app frappe_ticktix /path/to/local/frappe_ticktix

# Install in development mode
bench --site development.local install-app frappe_ticktix

# Enable developer mode
bench --site development.local set-config developer_mode 1

# Watch for changes
bench --site development.local build --app frappe_ticktix --verbose
```

### **Testing Setup:**

```bash
# Run unit tests
bench --site development.local run-tests --app frappe_ticktix

# Run specific test module
bench --site development.local run-tests --app frappe_ticktix --module frappe_ticktix.tests.branding

# Run with coverage
bench --site development.local run-tests --app frappe_ticktix --coverage
```

## 📋 **Configuration Reference**

### **Required Settings:**
- `ticktix_client_id`: OAuth client ID from TickTix Identity Server
- `ticktix_client_secret`: OAuth client secret
- `ticktix_base_url`: Base URL of TickTix Identity Server

### **Optional Branding Settings:**
- `company_logo`: URL for company logo
- `app_name`: Application name
- `app_title`: Application title
- `favicon`: Favicon URL
- `splash_image`: Splash screen image URL

### **Optional Authentication Settings:**
- `jwt_enabled`: Enable JWT authentication (default: true)
- `jwt_audience`: JWT audience claim (default: "api")
- `jwt_auto_provision`: Auto-provision users from JWT (default: false)
- `ticktix_authorize_url`: OAuth authorization endpoint (default: "/connect/authorize")
- `ticktix_token_url`: OAuth token endpoint (default: "/connect/token")

### **HR Configuration Settings:**
- `hr_employee_id_patterns`: Employee ID generation patterns
- `hr_attendance_rules`: Attendance validation rules
- `hr_enable_client_dayoff`: Enable client-specific day-offs

## 🚨 **Troubleshooting**

### **Common Issues:**

#### **OAuth Login Not Working:**
1. Check client credentials in site config
2. Verify redirect URLs in TickTix Identity Server
3. Check SSL certificates for HTTPS endpoints

#### **JWT Authentication Failing:**
1. Verify JWKS endpoint is accessible
2. Check JWT token format and claims
3. Ensure system clocks are synchronized

#### **Branding Not Applied:**
1. Clear bench cache: `bench clear-cache`
2. Rebuild assets: `bench build --app frappe_ticktix`
3. Check image URLs are accessible

#### **Mobile API Issues:**
1. Test PKCE flow with curl commands
2. Verify CORS settings for mobile app domains
3. Check mobile client configuration

### **Debug Commands:**

```bash
# Check configuration
bench --site your-site.local execute frappe_ticktix.core.config_manager.get_auth_config

# Test JWT validation
bench --site your-site.local execute frappe_ticktix.plugins.authentication.jwt_validator.test_jwt_config

# Clear cache
bench --site your-site.local clear-cache

# Rebuild with verbose output
bench --site your-site.local build --app frappe_ticktix --verbose

# Check logs
tail -f sites/your-site.local/logs/frappe.log
```

### **Getting Help:**

1. Check the logs: `sites/your-site.local/logs/`
2. Enable developer mode for detailed error messages
3. Review configuration settings
4. Consult the API documentation
5. Check GitHub issues for known problems

## 🔄 **Updates and Migration**

### **Updating the App:**

```bash
# Pull latest changes
bench get-app frappe_ticktix

# Update the app
bench --site your-site.local migrate

# Rebuild assets
bench build --app frappe_ticktix

# Restart services
bench restart
```

### **Database Migrations:**

The app includes automatic database migrations. After updating, always run:

```bash
bench --site your-site.local migrate
```

This ensures your database schema is up to date with the latest app version.