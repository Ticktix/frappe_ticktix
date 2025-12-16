# Frappe TickTix - Future Implementation Roadmap

## 🎯 **HR Module Development Plan**

### **Phase 2A: Employee ID Auto-Generation** (Ready to Implement)

#### **Structure to Create:**
```
plugins/hr_extensions/employee_id/
├── __init__.py
├── id_generator.py       # Core ID generation engine
├── naming_series.py      # Pattern definitions and parsing  
├── validators.py         # Validation rules and uniqueness checks
├── config.py            # Plugin configuration
└── hooks.py             # Frappe hooks registration
```

#### **Configuration Support:**
```json
// common_site_config.json
{
  "hr_employee_id_patterns": {
    "default": "EMP-{YYYY}-{####}",
    "department_based": {
      "IT": "IT-{YY}-{####}",
      "HR": "HR-{YY}-{####}",
      "Finance": "FIN-{YY}-{####}"
    },
    "branch_based": {
      "HQ": "HQ{YY}{MM}{###}",
      "BR1": "BR1-{YYYY}-{####}"
    }
  },
  "hr_employee_id_settings": {
    "auto_generate": true,
    "validate_uniqueness": true,
    "allow_manual_override": false,
    "reset_counter_yearly": true
  }
}
```

#### **Implementation Features:**
- **Pattern Support**: `{YYYY}`, `{YY}`, `{MM}`, `{####}`, `{###}`, `{DEPT}`, `{BRANCH}`
- **Department Integration**: Auto-detect department and apply appropriate pattern
- **Branch Support**: Multi-branch ID generation
- **Validation**: Duplicate checking and format validation
- **Counter Management**: Auto-increment with yearly reset options

---

### **Phase 2B: Extended Attendance System** (Ready to Implement)

#### **Structure to Create:**
```
plugins/hr_extensions/attendance/
├── __init__.py
├── weekly_off.py         # Custom weekly off management
├── client_dayoff.py      # Client-specific day offs
├── custom_dayoff.py      # Additional day-off types
├── attendance_rules.py   # Complex validation logic
├── calendar_manager.py   # Holiday calendar integration
├── config.py            # Plugin configuration
└── hooks.py             # Attendance validation hooks
```

#### **Configuration Support:**
```json
// common_site_config.json
{
  "hr_attendance_rules": {
    "enable_client_dayoff": true,
    "enable_custom_weekly_off": true,
    "client_holiday_priority": true,
    "weekly_off_patterns": {
      "standard": ["Saturday", "Sunday"],
      "alternate": ["Friday", "Saturday"],
      "rotating": {
        "pattern": ["Mon-Tue", "Wed-Thu", "Fri-Sat", "Sun-Mon"],
        "cycle_weeks": 4
      }
    },
    "custom_dayoff_types": [
      "Training Day",
      "Compensatory Off", 
      "Client Holiday",
      "Project Milestone Day"
    ]
  }
}
```

#### **Implementation Features:**
- **Flexible Weekly Offs**: Department/employee-specific patterns
- **Client Day-Offs**: Project-specific holidays that override company calendar
- **Custom Day-Off Types**: Additional leave categories beyond standard
- **Calendar Hierarchy**: Company → Client → Project → Employee priority
- **Rotation Support**: Complex shift patterns with rotation

---

### **Phase 2C: Plugin Architecture Enhancement**

#### **Advanced Plugin System:**
```
core/
├── base_plugin.py        # Abstract base class for plugins
├── plugin_loader.py      # Dynamic plugin loading system
├── plugin_registry.py    # Plugin registration and discovery
└── exceptions.py         # Plugin-specific exception handling
```

#### **Plugin Configuration Schema:**
```python
# plugins/hr_extensions/employee_id/config.py
PLUGIN_CONFIG = {
    'name': 'employee_id_generator',
    'version': '1.0.0',
    'description': 'Auto-generate employee IDs with custom patterns',
    'dependencies': ['hrms'],  # Requires HRMS app
    'hooks': [
        {
            'hook': 'before_insert',
            'doctype': 'Employee', 
            'method': 'plugins.hr_extensions.employee_id.hooks.generate_employee_id'
        }
    ],
    'api_endpoints': [
        '/api/v1/hr/employee-id/generate',
        '/api/v1/hr/employee-id/validate'
    ],
    'config_schema': {
        'hr_employee_id_patterns': {
            'type': 'dict',
            'required': True,
            'default': {'default': 'EMP-{YYYY}-{####}'}
        }
    },
    'permissions': {
        'HR Manager': ['read', 'write', 'create'],
        'Employee': ['read']
    }
}
```

---

## 🚀 **Phase 3: Advanced Features**

### **Payroll Extensions:**
```
plugins/hr_extensions/payroll/
├── custom_allowances.py  # Additional allowance types
├── deduction_rules.py    # Custom deduction logic
├── tax_calculations.py   # Region-specific tax rules
└── salary_structures.py  # Dynamic salary structure templates
```

### **Performance Management:**
```
plugins/hr_extensions/performance/
├── appraisal_flows.py    # Custom appraisal workflows
├── goal_tracking.py      # Objective and KPI management
├── feedback_system.py    # 360-degree feedback
└── performance_analytics.py # Performance reporting
```

### **Leave Management Extensions:**
```
plugins/hr_extensions/leave/
├── advanced_policies.py  # Complex leave policies
├── encashment_rules.py   # Leave encashment logic
├── accrual_engine.py     # Leave accrual calculations
└── approval_workflows.py # Multi-level approval flows
```

---

## 📊 **Implementation Timeline**

### **Phase 2A - Employee ID (2-3 weeks)**
- Week 1: Core ID generation engine
- Week 2: Pattern system and validation
- Week 3: Testing and documentation

### **Phase 2B - Attendance (3-4 weeks)** 
- Week 1: Weekly off management
- Week 2: Client day-off system
- Week 3: Custom day-off types
- Week 4: Integration and testing

### **Phase 2C - Plugin Enhancement (2-3 weeks)**
- Week 1: Base plugin architecture
- Week 2: Plugin loader and registry
- Week 3: Configuration schema system

---

## 💻 **Development Guidelines**

### **Plugin Development Pattern:**
```python
# plugins/hr_extensions/employee_id/id_generator.py
from frappe_ticktix.core.config_manager import get_hr_config
import frappe

def generate_employee_id(employee_doc, method=None):
    """Generate employee ID before employee creation"""
    if employee_doc.employee:
        return  # ID already set
    
    config = get_hr_config()
    patterns = config.get('hr_employee_id_patterns', {})
    
    # Determine pattern based on department/branch
    pattern = determine_pattern(employee_doc, patterns)
    
    # Generate ID from pattern
    new_id = generate_from_pattern(pattern, employee_doc)
    
    # Validate uniqueness
    if not is_unique_employee_id(new_id):
        new_id = generate_unique_variant(new_id)
    
    employee_doc.employee = new_id
    
def determine_pattern(employee_doc, patterns):
    """Determine which pattern to use"""
    if employee_doc.department in patterns.get('department_based', {}):
        return patterns['department_based'][employee_doc.department]
    elif employee_doc.branch in patterns.get('branch_based', {}):
        return patterns['branch_based'][employee_doc.branch]
    else:
        return patterns.get('default', 'EMP-{YYYY}-{####}')
```

### **Configuration Integration:**
```python
# Always use config_manager for settings
from frappe_ticktix.core.config_manager import get_hr_config

config = get_hr_config()
patterns = config.get('hr_employee_id_patterns', {})
settings = config.get('hr_employee_id_settings', {})
```

### **Testing Pattern:**
```python
# tests/hr_extensions/test_employee_id.py
def test_employee_id_generation():
    """Test ID generation with various patterns"""
    # Test default pattern
    # Test department-based pattern
    # Test uniqueness validation
    # Test manual override (if enabled)
```

---

## 🎯 **Success Metrics**

### **Phase 2A Success Criteria:**
- ✅ Employee IDs auto-generated on creation
- ✅ Multiple pattern support functional
- ✅ Department/branch integration working
- ✅ Uniqueness validation prevents duplicates
- ✅ Configuration through common_site_config.json

### **Phase 2B Success Criteria:**
- ✅ Flexible weekly off assignments
- ✅ Client-specific day-offs override company holidays
- ✅ Custom day-off types supported
- ✅ Attendance validation considers all rules
- ✅ Calendar hierarchy respected

---

## 🛠️ **Development Resources**

### **Required Skills:**
- Python (Frappe framework)
- Database design (MySQL/MariaDB)
- API development (REST)
- Configuration management
- Testing (Unit & Integration)

### **Documentation to Create:**
- Plugin development guide
- HR configuration reference  
- API endpoint documentation
- Testing guidelines
- Deployment procedures

### **Tools & Environment:**
- Frappe Bench for development
- Git for version control
- Automated testing pipeline
- Configuration validation tools