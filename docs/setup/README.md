# Setup & Configuration

This folder contains all documentation related to installing, configuring, and setting up the TickTix OAuth integration.

## Files in this folder

### 📋 **[setup_guide.md](setup_guide.md)**
Complete step-by-step installation and configuration guide covering:
- Installation via bench
- Site configuration
- OAuth provider setup
- Initial testing

### 📝 **[requirements.md](requirements.md)**
Login requirements and specifications including:
- Forced redirect to TickTix IdentityServer
- Tenant information handling
- User provisioning requirements

### 🔗 **[social_login_mapping_explanation.md](social_login_mapping_explanation.md)**
Detailed explanation of how users are mapped between systems:
- Frappe User Social Login table structure
- Bidirectional user synchronization
- Administrator account handling

## Quick Setup Flow

1. **Read requirements** → [requirements.md](requirements.md)
2. **Follow setup guide** → [setup_guide.md](setup_guide.md)
3. **Understand user mapping** → [social_login_mapping_explanation.md](social_login_mapping_explanation.md)
4. **Test installation** → [../testing/verification_guide.md](../testing/verification_guide.md)

## Next Steps

After completing setup, proceed to:
- **Authentication flows**: [../authentication/](../authentication/)
- **Mobile integration**: [../mobile/](../mobile/)
- **UI customization**: [../ui/](../ui/)