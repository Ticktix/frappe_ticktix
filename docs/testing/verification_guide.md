# TickTix OAuth Verification Guide

This guide explains the two verification methods available to test and validate your TickTix OAuth integration.

## Overview

The TickTix OAuth integration includes two comprehensive verification approaches:

1. **CLI Verification** - Standalone script for production and CI/CD environments
2. **API Verification** - Web-based endpoints for integration with Frappe applications

Both methods perform the same core validation checks but are designed for different use cases.

## Verification Methods

### 1. CLI Verification (`verify_cli.py`)

**Purpose**: Standalone command-line verification for production environments, CI/CD pipelines, and system administration.

**Location**: `apps/frappe_ticktix/frappe_ticktix/utils/verify_cli.py`

**Usage**:
```bash
cd /path/to/your/frappe/bench
python apps/frappe_ticktix/frappe_ticktix/utils/verify_cli.py
```

**Features**:
- Complete 6-point verification system
- Detailed console output with color-coded results
- OAuth URL generation for manual testing
- Standalone execution (initializes Frappe context)
- Perfect for automated testing and deployment verification

**Output Example**:
```
=== TickTix OAuth Integration Verification ===

✓ 1. OAuth-Only Authentication: PASS
✓ 2. TickTix Social Login Key: PASS
✓ 3. Administrator Setup: PASS
✓ 4. OAuth Handlers: PASS
✓ 5. JWT Decoder: PASS
✓ 6. Installation Hooks: PASS
✓ 7. User Provisioning System: PASS

=== VERIFICATION COMPLETE ===
Status: ALL CHECKS PASSED (7/7)
OAuth Integration: READY

Test OAuth URL: https://login.ticktix.com/connect/authorize?...
```

### 2. API Verification (`verify_setup.py`)

**Purpose**: Web-based verification endpoints for integration with Frappe applications and web interfaces.

**Location**: `apps/frappe_ticktix/frappe_ticktix/verify_setup.py`

**Available Endpoints**:

#### Quick Status Check
```http
GET /api/method/frappe_ticktix.utils.verify_setup.quick_status
```
Returns basic system status and OAuth readiness.

#### OAuth Test URL Generation
```http
GET /api/method/frappe_ticktix.utils.verify_setup.get_test_oauth_url
```
Generates a test OAuth URL for manual verification.

#### Complete Integration Verification
```http
GET /api/method/frappe_ticktix.utils.verify_setup.verify_complete_integration
```
Performs comprehensive 6-point verification with detailed results.

#### JWT Decoder Test
```http
GET /api/method/frappe_ticktix.utils.verify_setup.test_jwt_decoder
```
Tests the custom JWT decoder with sample TickTix tokens.

#### Auto-Provisioning Test
```http
GET /api/method/frappe_ticktix.utils.verify_setup.test_auto_provisioning
```
Tests the automatic user provisioning by creating a temporary user and verifying IDP creation and social login mapping.

#### Installation Provisioning Test
```http
GET /api/method/frappe_ticktix.utils.verify_setup.test_installation_provisioning
```
Tests and reports on the installation-time user provisioning system, showing how many users need provisioning and system readiness.

#### Manual Provisioning Commands
```http
GET /api/method/frappe_ticktix.install.manual_provision_existing_users
```
Manually triggers the installation-time user provisioning process to provision all existing users with email addresses to TickTix IDP.

#### Administrator Mapping Setup
```http
GET /api/method/frappe_ticktix.install.manual_setup_administrator_mapping
```
Manually sets up Administrator user mapping to TickTix IDP (useful for troubleshooting).

**Usage Examples**:

Using curl:
```bash
# Quick status
curl "http://your-site/api/method/frappe_ticktix.utils.verify_setup.quick_status"

# Complete verification
curl "http://your-site/api/method/frappe_ticktix.utils.verify_setup.verify_complete_integration"

# Test JWT decoder
curl "http://your-site/api/method/frappe_ticktix.utils.verify_setup.test_jwt_decoder"

# Test auto-provisioning
curl "http://your-site/api/method/frappe_ticktix.utils.verify_setup.test_auto_provisioning"

# Manually provision existing users (installation-time provisioning)
curl "http://your-site/api/method/frappe_ticktix.install.manual_provision_existing_users"

# Setup Administrator mapping
curl "http://your-site/api/method/frappe_ticktix.install.manual_setup_administrator_mapping"
```

Using JavaScript:
```javascript
// In a Frappe app
frappe.call({
    method: 'frappe_ticktix.verify_setup.verify_complete_integration',
    callback: function(r) {
        console.log('Verification Results:', r.message);
    }
});
```

## Verification Checks

Both verification methods perform these 7 core checks:

### 1. OAuth-Only Authentication
- Verifies password login is disabled (`disable_user_pass_login = 1`)
- Confirms email link login is disabled (`login_with_email_link = 0`)
- Ensures OAuth is the only authentication method available
- **Security Impact**: Prevents users from creating accounts via traditional methods

### 2. TickTix Social Login Key
- Checks for existence of 'ticktix' Social Login Key
- Validates configuration parameters (client credentials, base_url, etc.)
- Verifies `sign_ups = 'Deny'` to prevent automatic user creation
- Confirms `user_id_property = 'sub'` for proper OAuth2 standard compliance

### 3. Administrator Setup
- Verifies Administrator email is set to your admin email
- Confirms Administrator is mapped to TickTix user ID
- Validates the user ID mapping for proper OAuth login
- **Security Impact**: Ensures admin access through OAuth

### 4. OAuth Handlers
- Tests custom OAuth callback handler availability
- Verifies TickTix-specific OAuth processing functions
- Confirms `handle_ticktix_oauth()` implements access control restrictions
- **Security Impact**: Only pre-mapped users can access the system

### 5. JWT Decoder
- Tests custom JWT token decoder (`get_ticktix_user_info_from_code`)
- Validates token parsing and user info extraction
- Ensures proper handling of TickTix ID tokens
- **Security Impact**: Secure token processing prevents token manipulation

### 6. Installation Hooks
- Verifies installation and setup functions are available
- Checks configuration management functions
- Validates `after_install` hook properly disabled other login methods
- **Security Impact**: Ensures system is properly locked down during setup

### 7. User Provisioning System
- Verifies auto-provisioning functions for new users
- Checks email update handling for existing users
- Validates installation-time provisioning capabilities
- Tests user mapping creation and TickTix IDP integration
- **Security Impact**: Ensures users are properly provisioned before they can access

### 8. Access Control Verification
The verification also confirms the complete user creation prevention matrix:

**System Settings Verification:**
- `disable_user_pass_login`: Must be `True`
- `login_with_email_link`: Must be `False`

**Social Login Key Verification:**
- `sign_ups`: Must be `'Deny'`
- `enable_social_login`: Must be `True`
- Custom OAuth handler must reject unmapped users with 403 Forbidden

**Expected Behavior:**
- Administrator (your admin user) → Can login via OAuth
- Pre-mapped users → Can login via OAuth  
- All other users → Receive "Signup is Disabled" message with 403 status

## When to Use Which Method

### Use CLI Verification When:
- Deploying to production environments
- Running automated tests in CI/CD pipelines
- Performing system administration tasks
- Need standalone verification without web interface
- Troubleshooting integration issues from command line

### Use API Verification When:
- Building web interfaces or dashboards
- Integrating verification into Frappe applications
- Creating monitoring or health check systems
- Need programmatic access to verification results
- Building custom administration interfaces

## Response Formats

### CLI Verification Output
- Human-readable console output
- Color-coded pass/fail indicators
- Summary statistics
- OAuth test URL generation

### API Verification Response
- JSON-formatted responses
- Structured data for programmatic consumption
- Detailed error information
- Consistent status codes

Example API response:
```json
{
  "message": {
    "overall_status": "success",
    "checks_passed": 6,
    "total_checks": 6,
    "checks": [
      {
        "name": "OAuth-Only Authentication",
        "success": true,
        "message": "Password login disabled, OAuth-only enabled"
      }
      // ... more checks
    ],
    "oauth_test_url": "https://login.ticktix.com/connect/authorize?...",
    "summary": {
      "status": "success",
      "message": "ALL CHECKS PASSED",
      "success_rate": "6/6",
      "oauth_ready": true
    }
  }
}
```

## Troubleshooting

### Common Issues

1. **Frappe Context Errors** (CLI only)
   - Ensure you're running from the correct bench directory
   - Verify Frappe environment is properly initialized

2. **Permission Errors** (API only)
   - Check user permissions for API access
   - Verify Social Login Key configuration

3. **JWT Decoder Failures**
   - Validate JWT signing keys
   - Check network connectivity to TickTix servers

4. **OAuth URL Generation Issues**
   - Verify Social Login Key client ID and secret
   - Check redirect URI configuration

### Getting Help

For issues with verification:
1. Check the Frappe error logs
2. Verify all configuration steps from the setup guide
3. Test OAuth flow manually using generated URLs
4. Compare CLI and API results for consistency

Both verification methods provide comprehensive testing to ensure your TickTix OAuth integration is properly configured and functional.
