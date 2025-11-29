# TickTix OAuth Integration - Technical Details

This document provides detailed technical information about how the frappe_ticktix app implements OAuth-only authentication and user access control.

## Architecture Overview

The frappe_ticktix app implements a **closed OAuth-only authentication system** with the following components:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Browser  │    │  Frappe Instance │    │ TickTix Identity│
│                 │    │  (ticktix.local) │    │    Server       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                       │
         │ 1. GET /login          │                       │
         │───────────────────────▶│                       │
         │                        │ 2. Redirect to        │
         │                        │    TickTix OAuth      │
         │                        │──────────────────────▶│
         │ 3. TickTix Login Page  │                       │
         │◀──────────────────────────────────────────────│
         │                        │                       │
         │ 4. OAuth Callback      │                       │
         │───────────────────────▶│ 5. Token Exchange     │
         │                        │──────────────────────▶│
         │                        │ 6. JWT Token          │
         │                        │◀──────────────────────│
         │ 7. Login Success/Deny  │                       │
         │◀───────────────────────│                       │
```

## Core Components

### 1. Installation Hooks (`install.py`)

The `after_install()` hook performs system lockdown:

```python
def after_install():
    setup_administrator_user()      # Configure admin email
    setup_ticktix_social_login()   # Create OAuth provider
    disable_other_login_methods()  # Lock down system
    setup_https_enforcement()      # Security settings
    setup_company_logo()          # Branding
    provision_existing_users()    # User provisioning
```

**Key Security Changes:**
- `disable_user_pass_login = 1` → Disables password login
- `login_with_email_link = 0` → Disables email login
- `sign_ups = 'Deny'` → Prevents OAuth signup
- Creates TickTix Social Login Key with proper configuration

### 2. OAuth Flow Handler (`login_callback.py`)

The custom OAuth handler implements strict access control:

```python
@frappe.whitelist(allow_guest=True)
def handle_ticktix_oauth():
    # Extract user info from JWT token
    user_info = get_ticktix_user_info_from_code(code)
    email = user_info.get('email', '').lower()
    ticktix_user_id = user_info.get('sub')
    
    # Access control logic
    admin_email = frappe.conf.get('ticktix_admin_email', 'admin@your-domain.com').lower()
    
    if email == admin_email:
        # Administrator access - always allowed
        return login_administrator_user(ticktix_user_id, email, state)
    else:
        # Check for existing user mapping
        existing_user = frappe.db.get_value("User Social Login", 
                                           {"provider": "ticktix", "userid": ticktix_user_id}, 
                                           "parent")
        if existing_user:
            # Pre-mapped user - allowed
            login_oauth_user(user_info, provider="ticktix", state=state)
        else:
            # No mapping - DENIED
            frappe.respond_as_web_page(
                "Signup is Disabled",
                "Your account is not authorized to access this system...",
                success=False, http_status_code=403
            )
```

### 3. User Provisioning System

Three-tier provisioning system ensures users exist in TickTix IDP:

#### Installation-Time Provisioning
```python
def provision_existing_users():
    # Get all enabled users with emails
    users = frappe.get_all('User', filters={
        'enabled': 1,
        'email': ['!=', ''],
        'name': ['not in', ['Administrator', 'Guest']]
    })
    
    # For each user:
    # 1. Check if exists in TickTix IDP
    # 2. Create if needed
    # 3. Create Social Login mapping
```

#### New User Auto-Provisioning
Document event hooks automatically provision new users:
```python
# In hooks.py
doc_events = {
    "User": {
        "after_insert": "frappe_ticktix.login_callback.auto_provision_user",
        "on_update": "frappe_ticktix.login_callback.handle_user_email_update"
    }
}
```

#### Email Update Handling
When existing users get email addresses, they're automatically provisioned.

### 4. JWT Token Processing

Custom JWT decoder handles TickTix ID tokens:

```python
def get_ticktix_user_info_from_code(authorization_code):
    # Exchange authorization code for tokens
    token_response = requests.post(token_url, data={
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': redirect_uri,
        'client_id': '**client_id**',
        'client_secret': '**client_secret**'
    })
    
    # Extract and decode JWT ID token
    id_token = token_response.json().get('id_token')
    jwt_parts = id_token.split('.')
    payload_b64 = jwt_parts[1]
    payload_b64 += '=' * (4 - len(payload_b64) % 4)  # Add padding
    user_info = json.loads(base64.b64decode(payload_b64).decode('utf-8'))
    
    return user_info
```

### 5. Redirect URI Configuration

Simplified redirect URI handling using site-specific configuration:

```python
# Both api.py and login_callback.py use same logic
site_config = frappe.get_site_config() if hasattr(frappe, 'get_site_config') else {}
tenant_base_url = site_config.get('tenant_base_url')
redirect_uri_template = common_config.get('ticktix_redirect_url_template')

if not tenant_base_url:
    frappe.throw("tenant_base_url is required in site_config.json")
if not redirect_uri_template:
    frappe.throw("ticktix_redirect_url_template is required in common_site_config.json")

redirect_uri = f"{tenant_base_url.rstrip('/')}{redirect_uri_template}"
```

**Site Configuration Example:**
```json
// site_config.json
{
  "tenant_base_url": "https://your-site.com",  // or "http://ticktix.local:8000" for local
  // ... other site-specific config
}
```

## Security Implementation

### Access Control Matrix

| User Type | Email | TickTix Mapping | Access Result |
|-----------|-------|-----------------|---------------|
| Administrator | `admin@your-domain.com` | Auto-created | ✅ **ALLOWED** → Admin login |
| Existing User | Any email | Pre-mapped | ✅ **ALLOWED** → User login |
| New User | Any email | None | ❌ **DENIED** → 403 Forbidden |
| Any User | No email | N/A | ❌ **DENIED** → No OAuth mapping possible |

### Multi-Layer Security

1. **System Level**: Password/email login disabled
2. **OAuth Level**: Social signup denied
3. **Handler Level**: Custom access control logic
4. **Mapping Level**: Pre-mapping required
5. **Provisioning Level**: Controlled user creation

### Configuration Security

```json
// common_site_config.json - Secure configuration
{
  "ticktix_client_id": "**your_client_id**",
  "ticktix_client_secret": "**your_client_secret**",
  "ticktix_base_url": "https://login.ticktix.com",
  "ticktix_admin_email": "admin@your-domain.com",
  "ticktix_redirect_url_template": "/api/method/frappe.integrations.oauth2_logins.custom/ticktix"
}
```

### Error Handling

Graceful error responses prevent information leakage:
- Invalid tokens → Generic "Authentication failed" message
- Unmapped users → "Signup is Disabled" with contact admin message
- System errors → Logged server-side, generic error to user

## Database Schema Changes

### Social Login Key Document
```
Social Login Key: ticktix
├── provider_name: "TickTix"
├── enable_social_login: 1
├── client_id: "**your_client_id**"
├── client_secret: "**your_client_secret**"
├── base_url: "https://login.ticktix.com"
├── redirect_url: "/api/method/frappe.integrations.oauth2_logins.custom/ticktix"
├── user_id_property: "sub"
└── sign_ups: "Deny"
```

### System Settings Changes
```
System Settings:
├── disable_user_pass_login: 1
├── login_with_email_link: 0
└── app_name: "TickTix"
```

### User Social Login Mappings
```
User Social Login:
├── parent: "Administrator"
├── provider: "ticktix"
├── userid: "6116a6b6-954d-4099-9822-e4aaaa9911bd"
└── username: "admin@your-domain.com"
```

## API Endpoints

### Verification Endpoints
- `GET /api/method/frappe_ticktix.utils.verify_setup.quick_status`
- `GET /api/method/frappe_ticktix.utils.verify_setup.verify_complete_integration`
- `GET /api/method/frappe_ticktix.utils.verify_setup.test_jwt_decoder`

### Management Endpoints
- `GET /api/method/frappe_ticktix.install.manual_provision_existing_users`
- `GET /api/method/frappe_ticktix.install.manual_setup_administrator_mapping`

### OAuth Endpoints
- `GET /api/method/frappe.integrations.oauth2_logins.custom/ticktix` (OAuth callback)
- `GET /api/method/frappe_ticktix.login_callback.handle_ticktix_oauth`

## Monitoring and Verification

The system includes comprehensive verification tools:

### CLI Verification
```bash
python apps/frappe_ticktix/frappe_ticktix/utils/verify_cli.py
```

### Verification Checks
1. OAuth-only authentication status
2. TickTix Social Login Key configuration
3. Administrator mapping validation
4. OAuth handler availability
5. JWT decoder functionality
6. Installation hook status
7. User provisioning system readiness

## Maintenance

### Regular Checks
- Verify OAuth endpoints are accessible
- Check client credentials are valid
- Monitor failed login attempts
- Review user provisioning logs

### Updates
- Client secret rotation requires config update
- TickTix base URL changes need configuration update
- New users require manual provisioning or admin creation

This technical implementation ensures a secure, OAuth-only authentication system with comprehensive user access control and monitoring capabilities.
