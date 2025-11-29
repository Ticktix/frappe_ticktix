# Frappe Custom App Requirements – Plan 2 (Ticktix Login Integration)

## Objective

Replace Frappe’s default login with a **forced redirect** to TickTix IdentityServer, passing along tenant information for dynamic branding and authentication.

---

## Functional Requirements

1. **Disable Default Login**

   * Override Frappe’s login flow so that:

     * Direct access to `/login` redirects automatically to TickTix login.
     * Disable password-based login (no local user DB login).

2. **Social Login Integration**

   * Register TickTix as a social login provider (OAuth2).
   * All authentication requests must go through IdentityServer.

3. **Tenant Parameter Passing**

   * On redirect to IdentityServer:

     * Append a `tenant` parameter derived from the current site domain.

       * Example: `tenant=acme` if the user is on `acme.myfrappe.com`.
     * Redirect URL format:

       ```
       https://{tenant}.ticktix.com/api/method/frappe.integrations.oauth2_logins.custom/ticktix
       ```

4. **Post-Login Redirect**

   * After successful login:

     * IdentityServer redirects back to `https://{tenant}.myfrappe.com/login/callback`.
     * Frappe exchanges authorization code for tokens.
     * User is logged in or auto-created (`auto_create_user = false`).
     * When a new user is created in Frappe, the app must also provision the same user in TickTix Identity Server via the server-side API (`https://authapi.ticktix.com/`).

---

## Non-Functional Requirements

* **Security**

  * Ensure HTTPS enforced for all redirects.
  * Validate `state` and `nonce` for CSRF protection.

* **Maintainability**

  * All overrides packaged into a custom app.
  * Configurable via  `common_site_config.json`:

    ```json
    {
      "ticktix_client_id": "**your_client_id**",
      "ticktix_authorize_url": "https://login.ticktix.com/connect/authorize",
      "ticktix_token_url": "https://login.ticktix.com/connect/token",
      "ticktix_tenant_param": "tenant"
    }
    ```

* **Mobile App Support**

  * Mobile app collects tenant domain (or code).
  * App redirects user to login with `tenant` included.
  * After login, access/refresh tokens returned to Frappe and mobile app.

---

## Deliverables

* Custom Frappe app:

  * Overrides login route.
  * Adds TickTix social login provider automatically.
  * Supports tenant-aware redirect.
  * Provisions users both in Frappe and TickTix Identity Server.


## Configuration from `common_site_config.json`

```json
{
  "ticktix_client_id": "**your_client_id**",
  "ticktix_authorize_url": "https://login.ticktix.com/connect/authorize",
  "ticktix_token_url": "https://login.ticktix.com/connect/token",
  "ticktix_tenant_param": "tenant"
}

actual value 
clientid- your_oauth_client_id
client secret - `ticktix!@#100#@!`
base url - https://login.ticktix.com
authorize - /connect/authorize
token - /connect/token
redirecturl - https://{tenant}.ticktix.com/api/method/frappe.integrations.oauth2_logins.custom/ticktix
userinfo - /connect/userinfo
authurldata - { "response_type": "code", "scope": "openid profile email" }

these details need to set while configuring the Ticktix as social login and these configuration should comes from common_site_setings under sites