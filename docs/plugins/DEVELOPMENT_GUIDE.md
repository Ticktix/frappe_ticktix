# Frappe TickTix Plugin Development Guide

## 📖 **Overview**

This guide explains how to develop new plugins for the Frappe TickTix app using the established plugin architecture.

## 🏗️ **Plugin Structure**

### **Basic Plugin Layout:**
```
plugins/your_plugin/
├── __init__.py           # Plugin initialization
├── config.py            # Plugin configuration (optional)  
├── main_module.py       # Core functionality
├── hooks.py             # Frappe hooks (if needed)
└── tests/               # Plugin-specific tests
    └── test_main.py
```

### **Complex Plugin Layout:**
```
plugins/your_plugin/
├── __init__.py
├── config.py
├── submodule1/
│   ├── __init__.py
│   ├── feature1.py
│   └── feature2.py
├── submodule2/
│   ├── __init__.py
│   └── feature3.py
├── hooks.py
└── tests/
    ├── test_submodule1.py
    └── test_submodule2.py
```

## 🔧 **Configuration Integration**

### **Using Config Manager:**
```python
# Always import from core.config_manager
from frappe_ticktix.core.config_manager import get_config_manager

def your_plugin_function():
    config_manager = get_config_manager()
    
    # Get specific configuration
    your_setting = config_manager.get_config_value('your_plugin_setting', 'default_value')
    
    # Or get plugin-specific config group
    plugin_config = config_manager.get_config_value('your_plugin_config', {})
```

### **Configuration Schema Example:**
```json
// In common_site_config.json
{
  "your_plugin_config": {
    "enabled": true,
    "feature_flags": {
      "advanced_mode": false,
      "beta_features": true
    },
    "settings": {
      "timeout": 30,
      "max_retries": 3
    }
  }
}
```

## 🎣 **Hooks Integration**

### **Plugin Hooks Registration:**
```python
# plugins/your_plugin/hooks.py
import frappe

def your_before_insert_hook(doc, method):
    """Hook that runs before document insert"""
    # Your plugin logic here
    pass

def your_after_save_hook(doc, method):
    """Hook that runs after document save"""
    # Your plugin logic here
    pass

# Register in main hooks.py
# Add to frappe_ticktix/hooks.py:
doc_events = {
    "Your DocType": {
        "before_insert": "frappe_ticktix.plugins.your_plugin.hooks.your_before_insert_hook",
        "after_save": "frappe_ticktix.plugins.your_plugin.hooks.your_after_save_hook"
    }
}
```

## 🌐 **API Endpoints**

### **Creating Plugin APIs:**
```python
# plugins/your_plugin/api.py
import frappe

@frappe.whitelist()
def your_api_endpoint():
    """API endpoint for your plugin"""
    # Your API logic here
    return {
        "status": "success",
        "data": "your_data"
    }

@frappe.whitelist(allow_guest=True)
def public_endpoint():
    """Public API endpoint"""
    return {"message": "Hello, World!"}
```

### **API Registration:**
```python
# In hooks.py, add to override_whitelisted_methods:
override_whitelisted_methods["frappe_ticktix.plugins.your_plugin.api.your_api_endpoint"] = "frappe_ticktix.plugins.your_plugin.api.your_api_endpoint"
```

## 🧪 **Testing Your Plugin**

### **Test Structure:**
```python
# plugins/your_plugin/tests/test_main.py
import unittest
import frappe
from frappe_ticktix.plugins.your_plugin.main_module import your_function

class TestYourPlugin(unittest.TestCase):
    
    def setUp(self):
        """Set up test data"""
        pass
    
    def test_your_function(self):
        """Test your main function"""
        result = your_function()
        self.assertTrue(result)
    
    def test_configuration(self):
        """Test configuration loading"""
        from frappe_ticktix.core.config_manager import get_config_manager
        config = get_config_manager()
        setting = config.get_config_value('your_plugin_setting')
        self.assertIsNotNone(setting)
```

### **Running Tests:**
```bash
# Run specific plugin tests
cd /home/sagivasan/ticktix
bench --site ticktix.local run-tests --app frappe_ticktix --module frappe_ticktix.plugins.your_plugin.tests

# Run all plugin tests
bench --site ticktix.local run-tests --app frappe_ticktix --module frappe_ticktix.plugins
```

## 📋 **Plugin Configuration Schema**

### **Optional config.py:**
```python
# plugins/your_plugin/config.py
PLUGIN_CONFIG = {
    'name': 'your_plugin',
    'version': '1.0.0',
    'description': 'Description of your plugin',
    'author': 'Your Name',
    'dependencies': ['hrms'],  # Required apps
    'hooks': [
        'before_insert',
        'after_save'
    ],
    'api_endpoints': [
        '/api/method/frappe_ticktix.plugins.your_plugin.api.your_endpoint'
    ],
    'config_schema': {
        'your_plugin_config': {
            'type': 'dict',
            'required': False,
            'default': {}
        }
    },
    'permissions': {
        'System Manager': ['full'],
        'Your Role': ['read', 'write']
    }
}
```

## 🎯 **Best Practices**

### **1. Naming Conventions:**
- Plugin folders: lowercase with underscores (`hr_extensions`, `custom_reports`)
- Python modules: lowercase with underscores (`employee_id.py`, `attendance_rules.py`)
- Functions: lowercase with underscores (`generate_employee_id()`)
- Classes: PascalCase (`EmployeeIdGenerator`)

### **2. Error Handling:**
```python
import frappe

def your_function():
    try:
        # Your logic here
        result = perform_operation()
        return result
    except Exception as e:
        frappe.log_error(f"Error in your_function: {e}", "Your Plugin")
        frappe.throw(f"Operation failed: {str(e)}")
```

### **3. Logging:**
```python
import frappe

# Info logging
frappe.logger().info("Plugin operation completed successfully")

# Error logging with traceback
frappe.log_error("Error details", "Plugin Name")

# Debug logging (only in development)
if frappe.conf.developer_mode:
    frappe.logger().debug("Debug information")
```

### **4. Configuration Validation:**
```python
def validate_plugin_config():
    """Validate plugin configuration"""
    from frappe_ticktix.core.config_manager import get_config_manager
    
    config = get_config_manager()
    plugin_config = config.get_config_value('your_plugin_config', {})
    
    # Validate required fields
    required_fields = ['field1', 'field2']
    for field in required_fields:
        if field not in plugin_config:
            frappe.throw(f"Missing required configuration: {field}")
    
    return plugin_config
```

## 🔗 **Integration Examples**

### **With Existing Plugins:**
```python
# Using branding plugin from your plugin
from frappe_ticktix.plugins.branding.logo_manager import get_branding_config

def your_function():
    branding = get_branding_config()
    app_name = branding.get('app_name', 'Default App')
    # Use app_name in your logic
```

### **With Core Config Manager:**
```python
# Reading HR configuration in your plugin
from frappe_ticktix.core.config_manager import get_hr_config

def your_hr_function():
    hr_config = get_hr_config()
    employee_patterns = hr_config.get('hr_employee_id_patterns', {})
    # Use patterns in your logic
```

## 📚 **Plugin Examples**

### **Simple Utility Plugin:**
```python
# plugins/utils/string_helpers.py
def format_employee_name(first_name, last_name):
    """Format employee name consistently"""
    return f"{last_name}, {first_name}".title()

def generate_display_name(employee_doc):
    """Generate display name for employee"""
    return format_employee_name(employee_doc.first_name, employee_doc.last_name)
```

### **DocType Hook Plugin:**
```python
# plugins/custom_validation/employee_validator.py
import frappe

def validate_employee_email(doc, method):
    """Validate employee email domain"""
    from frappe_ticktix.core.config_manager import get_config_manager
    
    config = get_config_manager()
    allowed_domains = config.get_config_value('allowed_email_domains', [])
    
    if allowed_domains:
        email_domain = doc.user_id.split('@')[1] if '@' in doc.user_id else ''
        if email_domain not in allowed_domains:
            frappe.throw(f"Email domain {email_domain} is not allowed")
```

## 🚀 **Publishing Your Plugin**

### **Documentation Requirements:**
1. **README.md** - Plugin overview and installation
2. **API.md** - API endpoint documentation
3. **CONFIG.md** - Configuration options
4. **CHANGELOG.md** - Version history

### **Testing Checklist:**
- [ ] All functions have unit tests
- [ ] Integration tests with existing plugins
- [ ] Configuration validation tests
- [ ] API endpoint tests
- [ ] Error handling tests
- [ ] Performance tests (if applicable)

### **Code Quality:**
- [ ] Follow PEP 8 style guidelines
- [ ] Type hints where appropriate
- [ ] Docstrings for all functions
- [ ] Error handling and logging
- [ ] No hardcoded values (use configuration)

This guide should help you develop robust, well-integrated plugins for the Frappe TickTix app!