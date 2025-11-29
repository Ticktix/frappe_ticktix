# Social Login Mapping in Frappe Framework

## Overview
Frappe uses a **parent-child table relationship** to map external OAuth provider user IDs to internal Frappe users. This enables users to login with external providers (Google, GitHub, TickTix, etc.) while maintaining a single Frappe user identity.

## Database Structure

### 1. User Doctype (Parent)
- **Doctype**: `User`
- **File**: `/apps/frappe/frappe/core/doctype/user/user.json`
- **Child Table Field**: `social_logins` (Table field linking to User Social Login)

### 2. User Social Login Doctype (Child)
- **Doctype**: `User Social Login`
- **File**: `/apps/frappe/frappe/core/doctype/user_social_login/user_social_login.json`
- **Fields**:
  - `provider` (Data) - OAuth provider name (e.g., "ticktix", "google", "github")
  - `userid` (Data) - External provider's unique user ID
  - `username` (Data) - External provider's username (optional)

## Key Methods in User Class

### `get_social_login_userid(provider)`
```python
def get_social_login_userid(self, provider: str):
    try:
        for p in self.social_logins:
            if p.provider == provider:
                return p.userid
    except Exception:
        return None
```
- Returns the external User ID for a specific provider
- Returns `None` if no mapping exists

### `set_social_login_userid(provider, userid, username=None)`
```python
def set_social_login_userid(self, provider, userid, username=None):
    social_logins = {"provider": provider, "userid": userid}
    if username:
        social_logins["username"] = username
    self.append("social_logins", social_logins)
```
- Creates a new social login mapping
- Appends to the `social_logins` child table

## OAuth Login Flow in Frappe

### 1. Default Flow (`frappe.utils.oauth.login_via_oauth2`)
```python
def login_via_oauth2(provider: str, code: str, state: str, decoder: Callable | None = None):
    info = get_info_via_oauth(provider, code, decoder)
    login_oauth_user(info, provider=provider, state=state)
```

### 2. User Lookup and Creation (`update_oauth_user`)
```python
def update_oauth_user(user: str, data: dict, provider: str):
    user: "User" = get_user_record(user, data, provider)
    
    if not user.get_social_login_userid(provider):
        # Create social login mapping based on provider
        match provider:
            case "google":
                user.set_social_login_userid(provider, userid=data["id"])
            case "github":
                user.set_social_login_userid(provider, userid=data["id"], username=data.get("login"))
            case _:
                # For custom providers like TickTix
                user_id_property = frappe.db.get_value("Social Login Key", provider, "user_id_property") or "sub"
                user.set_social_login_userid(provider, userid=data[user_id_property])
```

### 3. User ID Property Configuration
- Defined in **Social Login Key** doctype
- For TickTix: `user_id_property = "sub"` (OAuth2 standard)
- Maps to the field in OAuth userinfo response that contains the unique user ID

## TickTix Integration Example

### 1. Social Login Key Configuration
```python
social_login_key = frappe.new_doc('Social Login Key')
social_login_key.provider_name = 'TickTix'
social_login_key.user_id_property = 'sub'  # OAuth2 standard user ID field
social_login_key.sign_ups = 'Deny'  # Disable auto-signup
```

### 2. Administrator Mapping Setup
```python
# Map Administrator to TickTix User ID
admin_user = frappe.get_doc("User", "Administrator")
admin_user.set_social_login_userid('ticktix', userid='6116a6b6-954d-4099-9822-e4aaaa9911bd')
admin_user.save(ignore_permissions=True)
```

### 3. OAuth Callback Logic
```python
def ticktix_oauth_callback():
    # Get TickTix User ID from OAuth response
    ticktix_user_id = user_info.get('sub')  # Using 'sub' field
    
    # Check if user already exists with this TickTix ID
    existing_user = frappe.db.get_value("User Social Login", 
                                       {"provider": "ticktix", "userid": ticktix_user_id}, 
                                       "parent")
    
    if existing_user:
        # Login existing user
        frappe.local.login_manager.user = existing_user
        frappe.local.login_manager.post_login()
    else:
        # Handle new user or create mapping
```

## Database Query Examples

### Find User by Provider User ID
```python
# Find Frappe user by TickTix User ID
user_name = frappe.db.get_value("User Social Login", 
    {"provider": "ticktix", "userid": "6116a6b6-954d-4099-9822-e4aaaa9911bd"}, 
    "parent")
```

### Get All Social Logins for a User
```python
# Get all social login mappings for Administrator
admin_user = frappe.get_doc("User", "Administrator")
for social_login in admin_user.social_logins:
    print(f"Provider: {social_login.provider}, User ID: {social_login.userid}")
```

### Direct Database Query
```sql
-- Find all users with TickTix mappings
SELECT 
    u.name as frappe_user,
    u.email,
    usl.userid as ticktix_user_id
FROM 
    tabUser u
    JOIN `tabUser Social Login` usl ON u.name = usl.parent
WHERE 
    usl.provider = 'ticktix';
```

## Best Practices

### 1. Provider Configuration
- Use `user_id_property = "sub"` for OAuth2 standard compliance
- Set `sign_ups = "Deny"` to prevent automatic user creation
- Pre-map critical users (like Administrator) before enabling OAuth

### 2. User ID Consistency
- External User IDs must be consistent across OAuth flows
- Use permanent IDs (not email addresses which can change)
- Validate User ID format and uniqueness

### 3. Error Handling
- Always check if social login mapping exists before creating new users
- Handle User ID mismatches gracefully
- Log OAuth flow details for debugging

### 4. Security Considerations
- Validate OAuth state parameter for CSRF protection
- Verify token signatures when using ID tokens
- Implement proper session management after login

## Common Issues and Solutions

### Issue: "Signup is Disabled" Error
- **Cause**: No existing User Social Login mapping found
- **Solution**: Pre-create mapping or enable signups temporarily

### Issue: Duplicate Users Created
- **Cause**: User ID property mismatch or inconsistent external User IDs
- **Solution**: Verify `user_id_property` matches OAuth response field

### Issue: Login Fails Despite Mapping
- **Cause**: External User ID changed or mapping corruption
- **Solution**: Update mapping with current User ID from provider

This system provides a robust foundation for multi-provider authentication while maintaining user identity consistency across login methods.
