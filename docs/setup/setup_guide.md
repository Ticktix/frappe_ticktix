# Setup Guide

> **🔒 Security Notice**: Replace all `**placeholders**` with your actual credentials. Never commit real client IDs, secrets, or tokens to version control.

This guide provides step-by-step instructions for installing and configuring the TickTix OAuth integration with Frappe.

## Requirements Implemented

✅ **All Requirements Completed:**

1. **Disable Default Login** - Overrides `/login` to redirect to TickTix
2. **Social Login Integration** - Registers TickTix as OAuth2 provider
3. **OAuth-Only Authentication** - Password and email link login disabled
4. **Post-Login Redirect** - Handles OAuth callback with custom user mapping
5. **Auto User Creation Disabled** - Set to `sign_ups: "Deny"` as required
6. **Comprehensive User Provisioning** - Auto-provisions users to TickTix IDP in three scenarios:
   - **Installation**: All existing users with emails provisioned during app installation
   - **New Users**: Auto-provision when new users are created
   - **Email Updates**: Auto-provision when existing users get email addresses
7. **Security** - CSRF protection with state/nonce validation and custom JWT decoder
8. **Administrator Mapping** - Your admin user maps to Administrator account
9. **Verification Tools** - CLI and API-based verification for testing integration

## Configuration

### Common Site Configuration
Add the following to your `sites/common_site_config.json`:

```json
```json
{
  "ticktix_base_url": "https://login.ticktix.com",
  "ticktix_client_id": "**your_client_id_here**",
  "ticktix_client_secret": "**your_client_secret_here**",
  "ticktix_redirect_url_template": "/api/method/frappe.integrations.oauth2_logins.custom/ticktix"
}
```

## Installation

1. **Install the app:**
   ```bash
   bench get-app frappe_ticktix
   bench --site your-site install-app frappe_ticktix
   ```

2. **Configuration is automatic** - The `after_install` hook will:
   - Create TickTix Social Login Key with correct settings
   - Disable username/password login (OAuth-only authentication)
   - Disable login with email link
   - Map Administrator account to your admin email
   - Set `auto_create_user` to `false` (sign_ups = "Deny")

## Verification

After installation, verify your integration using the included verification tools:

### CLI Verification (Recommended)
```bash
# From your bench directory
./env/bin/python apps/frappe_ticktix/frappe_ticktix/verify_cli.py
```

### API Verification
```http
GET /api/method/frappe_ticktix.verify_setup.verify_complete_integration
```

Both methods perform comprehensive 6-point verification:
1. OAuth-Only Authentication enabled
2. TickTix Social Login Key configured
3. Administrator properly mapped
4. OAuth handlers available
5. JWT decoder working
6. Installation hooks ready

See the [verification guide](../docs/verification_guide.md) for complete details.

## Usage

### Web Login Flow
1. User visits `/login` 
2. Automatically redirected to `https://login.ticktix.com/connect/authorize`
3. After authentication, redirected back to Frappe with OAuth callback
4. Custom handler processes JWT token and maps to appropriate user
5. User logged in as Administrator (for admin user) or denied access

### OAuth Integration Features
- ✅ **OAuth-Only Authentication**: Password and email link login disabled
- ✅ **Custom JWT Decoder**: Handles TickTix ID tokens properly
- ✅ **Administrator Mapping**: Your admin user → Administrator account
- ✅ **Secure Callback Handling**: Custom OAuth callback with proper user mapping
- ✅ **Access Control**: Only pre-mapped users can access the system
- ✅ **Verification Tools**: CLI and API-based testing and monitoring

## Security Features

- ✅ OAuth-only authentication (password/email login disabled)
- ✅ CSRF protection with state/nonce validation  
- ✅ Custom JWT decoder for secure token processing
- ✅ Secure OAuth2 Authorization Code flow
- ✅ Access control via user mapping (signup disabled)
- ✅ Administrator account protection

## User Creation Control Mechanisms

After installation, frappe_ticktix implements **multiple layers of user creation prevention**:

### 1. System-Level Authentication Disabled
- **Password Login: DISABLED** → Users cannot create accounts via username/password
- **Email Link Login: DISABLED** → Users cannot get login links via email

### 2. Social Login Signup Prevention
- **Social Login Sign Ups: DENY** → OAuth login does NOT create new users automatically
- **Website Signup: DISABLED** → No signup forms available on website

### 3. Custom OAuth Handler Restrictions
The custom OAuth handler (`handle_ticktix_oauth()`) implements strict access control:

**Allowed Access:**
1. **Administrator Login**: Your admin user → Maps to Administrator account
2. **Pre-mapped Users**: Users with existing TickTix Social Login mappings → Allowed to login

**Denied Access:**
- **All Other Users**: Receive **403 Forbidden** with message: *"Your account is not authorized to access this system. Please contact your administrator."*

### 4. Complete Access Control Matrix

| **Login Method** | **Status** | **Effect** |
|------------------|------------|------------|
| Username/Password Login | ❌ DISABLED | Cannot create accounts via login form |
| Email Link Login | ❌ DISABLED | Cannot get login links sent to email |
| Website Signup Forms | ❌ DISABLED | No signup forms available |
| OAuth Social Signup | ❌ DENIED | OAuth login cannot create new users |
| Direct API User Creation | ⚠️ ADMIN ONLY | Requires administrator permissions |
| Custom OAuth Handler | 🔒 RESTRICTED | Only allows pre-mapped users or Administrator |

### 5. User Provisioning System
The app includes automatic user provisioning to TickTix IDP:
- **Installation Time**: Provisions all existing users with emails
- **New User Creation**: Auto-provisions when administrators create users
- **Email Updates**: Auto-provisions when existing users get email addresses

**Result**: A **completely closed system** where only pre-authorized users or the Administrator can access the Frappe instance.

## File Structure

```
frappe_ticktix/
├── login_callback.py   # OAuth callback & JWT processing
├── install.py          # Auto-setup hooks
├── hooks.py           # Frappe hooks configuration
├── verify_cli.py      # CLI verification tool
├── verify_setup.py    # API verification endpoints
└── oauth_provider.py  # Social login provider registration
```

## Troubleshooting

### Common Issues

1. **Login not redirecting to TickTix:**
   - Check that `frappe_ticktix` is in `sites/apps.txt`
   - Verify the app was installed correctly: Run verification CLI tool
   - Ensure `/login` hook is active

2. **OAuth 400 Bad Request errors:**
   - Verify client credentials in `common_site_config.json`
   - Check redirect URI configuration matches TickTix OAuth app
   - Ensure `ticktix_redirect_url_template` is properly set

3. **"Authentication failed: Failed to get user information":**
   - Check client credentials are correct and accessible
   - Verify TickTix base URLs are correct
   - Test token endpoint connectivity

4. **"Signup is Disabled" message for valid users:**
   - User needs to be pre-mapped with TickTix Social Login mapping
   - Run user provisioning: `/api/method/frappe_ticktix.install.manual_provision_existing_users`
   - For Administrator: Ensure email matches your admin user email

5. **Users can still login with password:**
   - Check `System Settings` → `disable_user_pass_login` should be enabled
   - Verify installation completed successfully
   - Re-run installation hooks if needed

6. **Website signup forms still visible:**
   - Check `Website Settings` → signup should be disabled
   - Clear browser cache
   - Verify `sign_ups = 'Deny'` in TickTix Social Login Key

### User Access Scenarios

**✅ Allowed Access:**
- Your admin user → Automatically maps to Administrator
- Users with existing TickTix Social Login mappings → Can login via OAuth

**❌ Denied Access:**
- New users without pre-mapping → "Signup is Disabled" message
- Users trying password login → Login form unavailable
- Users trying email link → Email link login disabled

### Verification Commands

```bash
# Run complete verification
python apps/frappe_ticktix/frappe_ticktix/verify_cli.py

# Check current settings
python -c "
import frappe
frappe.init(site='your-site')
frappe.connect()
print('Password login disabled:', frappe.db.get_single_value('System Settings', 'disable_user_pass_login'))
print('Email link disabled:', not frappe.db.get_single_value('System Settings', 'login_with_email_link'))
social = frappe.get_doc('Social Login Key', 'ticktix')
print('Social signup:', social.sign_ups)
"

# Manual user provisioning
curl "http://your-site/api/method/frappe_ticktix.install.manual_provision_existing_users"
```

## Support

This app provides complete TickTix OAuth-only integration with comprehensive verification tools. Use the verification guide for testing and the implementation summary for technical details.
