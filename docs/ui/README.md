# User Interface

This folder contains documentation related to UI customization, branding, and user experience improvements.

## Files in this folder

### 🎨 **[login_ui_improvements.md](login_ui_improvements.md)**
Comprehensive guide to login page customization including:

#### **Design Features**
- **Split-screen layout**: Modern 50-50 design with CSS Grid
- **Professional branding**: TickTix logo and facility management messaging
- **Responsive design**: Mobile-optimized layout that stacks vertically
- **Clean aesthetics**: Minimal, distraction-free user interface

#### **Technical Implementation**
- **CSS Architecture**: Custom styling with `login_custom.css`
- **Frappe Integration**: Working within Frappe's login system
- **Asset Management**: Logo handling and image optimization
- **Cross-browser Support**: Consistent experience across browsers

#### **Branding Elements**
- Company logo integration (local vs external URLs)
- Custom color schemes and typography
- Facility management focused messaging
- Trust-building design elements

## UI Customization Areas

### 🔧 **Login Page**
- Split-screen professional design
- Custom branding and messaging
- Responsive mobile layout
- Social login button styling

### 🖼️ **Logo Management**
- Local file vs external URL handling
- Frappe File Manager integration
- Logo resolution and optimization
- Fallback logo strategies

### 🎯 **User Experience**
- Reduced cognitive load
- Clear call-to-action
- Professional first impression
- Mobile-friendly interactions

## Implementation Components

### CSS Files
- `login_custom.css` - Main styling
- Responsive breakpoints
- Grid layout system
- Professional color palette

### Configuration
- `company_logo` - Logo URL/path setting
- `splash_image` - Login page imagery
- Frappe System Settings integration

### Assets
- Logo files (recommended: local upload)
- Background images
- Icon resources

## Logo Configuration Issues

### ❌ **Common Problem**
External logo URLs may not load on login page due to:
- Browser security restrictions
- Network dependency issues
- Frappe template expectations

### ✅ **Recommended Solution**
Upload logos to Frappe File Manager:
```bash
# Download logo
wget https://login.ticktix.com/images/ticktix.jpg -O /tmp/logo.jpg

# Upload via Frappe UI to /files/
# Update configuration:
{
  "company_logo": "/files/ticktix_logo.jpg"
}
```

## Design Philosophy

### **Professional First Impression**
- Enterprise-quality split-screen design
- Clean, modern aesthetics
- Trust-building visual elements

### **Facility Management Focus**
- Industry-specific messaging
- Relevant value propositions
- Professional service positioning

### **Mobile-First Approach**
- Responsive design patterns
- Touch-friendly interactions
- Optimized loading performance

## Related Documentation

- **Setup**: [../setup/setup_guide.md](../setup/setup_guide.md) - Logo configuration
- **Development**: [../development/technical_details.md](../development/technical_details.md) - Technical implementation
- **Testing**: [../testing/verification_guide.md](../testing/verification_guide.md) - UI testing procedures