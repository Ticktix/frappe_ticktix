# Employee ID Auto-Generation Plugin

## Overview

The Employee ID Auto-Generation plugin automatically generates unique employee IDs when new employees are created in the system. It uses a flexible pattern-based system that dynamically resolves tokens from the Employee doctype fields.

**Key Design Principles:**
- **Simple Configuration** - Only define the pattern; counter scope is auto-detected
- **Smart Defaults** - Zero-padding determined by `{####}` count in pattern
- **Field-Driven** - Tokens resolved directly from Employee doctype fields

---

## Plugin Location & Structure

This plugin follows the existing **frappe_ticktix plugin architecture** and is located within the HR plugins folder.

### **Location:** `frappe_ticktix/plugins/hr/employee_id_generator/`

### **Folder Structure:**
```
frappe_ticktix/plugins/hr/
├── __init__.py
├── README.md
├── attendance/                    # Existing attendance plugin
│   ├── __init__.py
│   ├── attendance_manager.py
│   └── ...
├── checkin/                       # Existing checkin plugin
│   ├── __init__.py
│   └── checkin_manager.py
├── payroll/                       # Existing payroll plugin
│   └── ...
└── employee_id_generator/         # 👈 NEW: Employee ID Auto-Generation
    ├── __init__.py                # Plugin exports
    ├── id_generator.py            # Core ID generation engine
    ├── counter_manager.py         # Counter management with scoping
    ├── token_resolver.py          # Token parsing and resolution
    ├── validators.py              # Pattern and uniqueness validation
    └── hooks.py                   # Frappe hooks (before_insert)
```

### **Related Documentation:**
- [Plugin Development Guide](DEVELOPMENT_GUIDE.md) - How to create plugins
- [HR Plugin README](../../frappe_ticktix/plugins/hr/README.md) - HR plugin overview
- [Configuration Summary](../configuration/CONFIGURATION_SUMMARY.md) - All configuration options

### **Existing Plugins to Reference:**
| Plugin | Location | Description |
|--------|----------|-------------|
| Attendance | `plugins/hr/attendance/` | Attendance tracking |
| Checkin | `plugins/hr/checkin/` | Employee checkin/checkout |
| Branding | `plugins/branding/` | Logo and UI customization |
| Authentication | `plugins/authentication/` | JWT and OAuth |

---

## Configuration

Configuration is done via `common_site_config.json` (global) or `site_config.json` (site-specific).

### Minimal Configuration

```json
{
  "hr_employee_id_settings": {
    "enabled": true,
    "pattern": "EMP-{####}"
  }
}
```

### Full Configuration

```json
{
  "hr_employee_id_settings": {
    "enabled": true,
    "pattern": "{COMPANY_ABBR}-{DEPARTMENT_ABBR}-{YY}-{####}",
    "allow_manual_override": false,
    "case_format": "upper",
    "counter_padding": 4,
    "reset_counter": "yearly",
    "abbreviations": {
      "departments": {
        "Information Technology": "IT",
        "Human Resources": "HR"
      }
    }
  }
}
```

---

## Configuration Options

### `hr_employee_id_settings`

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `enabled` | boolean | `false` | Enable/disable auto-generation |
| `pattern` | string | `"EMP-{####}"` | The pattern template for generating IDs |
| `allow_manual_override` | boolean | `false` | Allow manual entry of employee ID |
| `case_format` | string | `"upper"` | Output case: `upper`, `lower`, `preserve` |
| `counter_padding` | integer | (auto) | Override zero-padding (e.g., `4` → `0001`). If not set, determined by `{####}` count in pattern |
| `reset_counter` | string | (auto) | Override reset behavior: `never`, `yearly`, `monthly`. If not set, auto-detected from date tokens |
| `abbreviations` | object | `{}` | Custom abbreviation mappings (optional) |

> **Note:** `counter_padding` and `reset_counter` are **optional overrides**. By default, these are auto-detected from the pattern.

---

## Available Tokens

Tokens are placeholders in the pattern that get replaced with actual values during ID generation.

### Date Tokens

| Token | Description | Example |
|-------|-------------|---------|
| `{YYYY}` | 4-digit year | `2025` |
| `{YY}` | 2-digit year | `25` |
| `{MM}` | 2-digit month (01-12) | `11` |
| `{DD}` | 2-digit day (01-31) | `29` |

### Counter Tokens

| Token | Description | Example |
|-------|-------------|---------|
| `{#}` | Counter with 1 digit | `1` |
| `{##}` | Counter with 2 digits, zero-padded | `01` |
| `{###}` | Counter with 3 digits, zero-padded | `001` |
| `{####}` | Counter with 4 digits, zero-padded | `0001` |
| `{#####}` | Counter with 5 digits, zero-padded | `00001` |

> **Note:** The number of `#` symbols determines the zero-padding automatically.

### Employee Field Tokens

These tokens are **automatically resolved** from the Employee doctype fields.

| Token | Source Field | Doctype Link | Example |
|-------|--------------|--------------|--------|
| `{COMPANY}` | `employee.company` | Company | `TickTix LLC` |
| `{COMPANY_ABBR}` | `company.abbr` | Company | `TTX` |
| `{DEPARTMENT}` | `employee.department` | Department | `Engineering` |
| `{DEPARTMENT_ABBR}` | `department.custom_abbr` | Department | `ENG` |
| `{BRANCH}` | `employee.branch` | Branch | `Head Office` |
| `{BRANCH_ABBR}` | `branch.custom_abbr` | Branch | `HO` |
| `{EMPLOYMENT_TYPE}` | `employee.employment_type` | Employment Type | `Full-time` |
| `{EMPLOYMENT_TYPE_ABBR}` | `employment_type.custom_abbr` | Employment Type | `FT` |

### Doctype Field Availability

| Doctype | Has `abbr` Field? | Abbreviation Source |
|---------|-------------------|---------------------|
| **Company** | ✅ Built-in `abbr` | Uses existing `abbr` field |
| **Department** | ✅ `custom_abbr` (added via migration) | Config override → `custom_abbr` field → fallback |
| **Branch** | ✅ `custom_abbr` (added via migration) | Config override → `custom_abbr` field → fallback |
| **Employment Type** | ✅ `custom_abbr` (added via migration) | Config override → `custom_abbr` field → fallback |

> **Note:** Run the [Custom Field Migration](#custom-field-migration) to add `custom_abbr` fields to Department, Branch, and Employment Type doctypes.

### Abbreviation Resolution (Hybrid Approach)

For `_ABBR` tokens, the system resolves abbreviations using this priority:

```
┌─────────────────────────────────────────────────────────────┐
│  1. Config Override (abbreviations in hr_employee_id_settings) │
│     ↓ if not found                                           │
│  2. DocType Field (abbr or custom_abbr field)                │
│     ↓ if not found                                           │
│  3. Auto-Fallback (first N characters of name)               │
└─────────────────────────────────────────────────────────────┘
```

**Resolution Logic:**
```python
def get_abbreviation(entity_type, entity_name):
    # 1. Check config override first (highest priority)
    config_abbr = get_config_abbreviation(entity_type, entity_name)
    if config_abbr:
        return config_abbr
    
    # 2. Check abbr field on doctype
    abbr_field_map = {
        "Company": "abbr",           # Built-in field
        "Department": "custom_abbr", # Custom field we add
        "Branch": "custom_abbr",     # Custom field we add
        "Employment Type": "custom_abbr"  # Custom field we add
    }
    
    abbr_field = abbr_field_map.get(entity_type)
    if abbr_field:
        abbr = frappe.db.get_value(entity_type, entity_name, abbr_field)
        if abbr:
            return abbr
    
    # 3. Fallback to first N characters
    fallback_lengths = {
        "Company": 3,
        "Department": 3,
        "Branch": 3,
        "Employment Type": 2
    }
    return entity_name[:fallback_lengths.get(entity_type, 3)].upper()
```

---

## Pattern Examples

### Simple Patterns

| Pattern | Output Example | Description |
|---------|----------------|-------------|
| `EMP-{####}` | `EMP-0001` | Simple sequential (global counter) |
| `EMP{#####}` | `EMP00001` | No separator, 5-digit |
| `{YYYY}-{####}` | `2025-0001` | Year prefixed (counter scoped to year) |
| `E{YY}{MM}{###}` | `E2511001` | Compact date format (counter scoped to month) |

### Department-Based Patterns

| Pattern | Output Example | Description |
|---------|----------------|-------------|
| `{DEPARTMENT_ABBR}-{####}` | `ENG-0001` | Department prefix (counter per department) |
| `{DEPARTMENT_ABBR}-{YY}-{####}` | `ENG-25-0001` | Department + year (counter per dept+year) |
| `{COMPANY_ABBR}-{DEPARTMENT_ABBR}-{####}` | `TTX-ENG-0001` | Company + Department |

### Branch-Based Patterns

| Pattern | Output Example | Description |
|---------|----------------|-------------|
| `{BRANCH_ABBR}-{####}` | `HO-0001` | Branch prefix (counter per branch) |
| `{BRANCH_ABBR}{YYYY}{####}` | `HO20250001` | Compact branch + year |

### Employment Type Patterns

| Pattern | Output Example | Description |
|---------|----------------|-------------|
| `{EMPLOYMENT_TYPE_ABBR}-{####}` | `FT-0001` | Employment type prefix |
| `EMP-{EMPLOYMENT_TYPE_ABBR}-{YY}-{####}` | `EMP-FT-25-0001` | Full pattern |

### Complex Patterns

| Pattern | Output Example | Description |
|---------|----------------|-------------|
| `{COMPANY_ABBR}-{BRANCH_ABBR}-{DEPARTMENT_ABBR}-{####}` | `TTX-HO-ENG-0001` | Multi-level hierarchy |
| `{COMPANY_ABBR}{YY}{MM}{####}` | `TTX25110001` | Compact company + date |

---

## Auto-Detected Counter Scoping

**The counter scope is automatically determined from the tokens in your pattern.** No manual configuration needed!

### How It Works

| Pattern Contains | Auto-Detected Counter Scope |
|------------------|----------------------------|
| No entity tokens | `global` - single counter for all |
| `{COMPANY_ABBR}` | `company` - separate counter per company |
| `{DEPARTMENT_ABBR}` | `department` - separate counter per department |
| `{BRANCH_ABBR}` | `branch` - separate counter per branch |
| `{EMPLOYMENT_TYPE_ABBR}` | `employment_type` - separate counter per type |
| `{YYYY}` or `{YY}` | Adds `yearly` scope - counter resets each year |
| `{MM}` | Adds `monthly` scope - counter resets each month |

### Examples

| Pattern | Auto-Detected Scope | Counter Key |
|---------|---------------------|-------------|
| `EMP-{####}` | `global` | `emp_id_counter` |
| `{DEPARTMENT_ABBR}-{####}` | `department` | `emp_id_counter:dept:Engineering` |
| `{COMPANY_ABBR}-{YY}-{####}` | `company+yearly` | `emp_id_counter:company:TTX:year:2025` |
| `{BRANCH_ABBR}-{DEPARTMENT_ABBR}-{####}` | `branch+department` | `emp_id_counter:branch:HO:dept:ENG` |
| `{COMPANY_ABBR}-{DEPARTMENT_ABBR}-{YY}-{####}` | `company+department+yearly` | `emp_id_counter:company:TTX:dept:ENG:year:25` |

### Why This Matters

With pattern `{DEPARTMENT_ABBR}-{####}`:
- IT Department: `IT-0001`, `IT-0002`, `IT-0003`
- HR Department: `HR-0001`, `HR-0002` (separate counter!)

With pattern `{DEPARTMENT_ABBR}-{YY}-{####}`:
- IT in 2025: `IT-25-0001`, `IT-25-0002`
- IT in 2026: `IT-26-0001` (counter resets for new year!)

### Override Examples

**Scenario 1:** Pattern has `{YYYY}` but you want continuous numbering (no yearly reset):
```json
{
  "hr_employee_id_settings": {
    "enabled": true,
    "pattern": "EMP-{YYYY}-{####}",
    "reset_counter": "never"
  }
}
```
- 2025: `EMP-2025-0001`, `EMP-2025-0002`, `EMP-2025-0003`
- 2026: `EMP-2026-0004`, `EMP-2026-0005` (counter continues!)

**Scenario 2:** Pattern has `{###}` but you want 4-digit padding:
```json
{
  "hr_employee_id_settings": {
    "enabled": true,
    "pattern": "EMP-{###}",
    "counter_padding": 4
  }
}
```
- Output: `EMP-0001`, `EMP-0002` (4 digits despite `{###}`)

**Scenario 3:** No date in pattern but want yearly reset:
```json
{
  "hr_employee_id_settings": {
    "enabled": true,
    "pattern": "EMP-{####}",
    "reset_counter": "yearly"
  }
}
```
- 2025: `EMP-0001`, `EMP-0002`
- 2026: `EMP-0001`, `EMP-0002` (counter resets!)
- ⚠️ **Warning:** This could cause duplicates! Add `{YY}` to pattern to avoid.

---

## Employee Doctype Field Mapping

The following fields from the **Employee** doctype are available for token resolution:

| Employee Field | Field Type | Linked Doctype | Available Tokens |
|----------------|------------|----------------|------------------|
| `company` | Link | Company | `{COMPANY}`, `{COMPANY_ABBR}` |
| `department` | Link | Department | `{DEPARTMENT}`, `{DEPARTMENT_ABBR}` |
| `branch` | Link | Branch | `{BRANCH}`, `{BRANCH_ABBR}` |
| `employment_type` | Link | Employment Type | `{EMPLOYMENT_TYPE}`, `{EMPLOYMENT_TYPE_ABBR}` |

### Adding Custom Fields

If you need additional tokens (e.g., Client), you can:

1. Add a custom field to Employee doctype (e.g., `custom_client`)
2. The plugin will automatically detect fields prefixed with `custom_` and make them available as tokens

```json
{
  "hr_employee_id_settings": {
    "pattern": "{CUSTOM_CLIENT_ABBR}-{####}",
    "custom_tokens": {
      "CUSTOM_CLIENT": "custom_client",
      "CUSTOM_CLIENT_ABBR": "custom_client_abbr"
    }
  }
}
```

---

## Abbreviation Configuration

### Doctype Field Status

Based on analysis of Frappe/HRMS doctypes:

| Doctype | Structure | `abbr` Field | Other Relevant Fields | Recommendation |
|---------|-----------|--------------|----------------------|----------------|
| **Company** | Tree (parent_company) | ✅ `abbr` (Data) | `company_name` | Use existing `abbr` field |
| **Department** | Tree (parent_department) | ❌ None → **Add `custom_abbr`** | `department_name`, `is_group` | Add custom field |
| **Branch** | Flat | ❌ None → **Add `custom_abbr`** | `branch` | Add custom field |
| **Employment Type** | Flat | ❌ None → **Add `custom_abbr`** | `employee_type_name` | Add custom field |

> **Recommendation:** Add custom `abbr` fields to Department, Branch, and Employment Type doctypes for consistency with Company. This provides a better admin experience and eliminates the need for config-based abbreviation mappings.

### Why Custom Fields Over Config?

| Approach | Pros | Cons |
|----------|------|------|
| **Custom Fields** ✅ | Self-documenting, no config sync needed, consistent with Company doctype | Requires one-time migration |
| **Config Mapping** | No doctype changes | Manual sync needed, not visible in UI |

**Recommended:** Hybrid approach - Custom fields with config override capability.

### Tree Structure Considerations

**Department** and **Company** are **tree structures** with parent-child relationships:

```
Operations (abbr: OPS)
├── Security (abbr: SEC)
└── Maintenance (abbr: MNT)
```

**Key Point:** Each node (parent or child) is an independent record with its own `abbr` field. No special handling needed for parent records - they use their own abbreviation just like any other record.

### Default Fallback Lengths

When no config mapping exists and no `abbr`/`custom_abbr` field is set:

| Token Type | Fallback Length | Example |
|------------|-----------------|--------|
| Company | 3 characters | `TickTix LLC` → `TIC` |
| Department | 3 characters | `Information Technology` → `INF` |
| Branch | 3 characters | `Head Office` → `HEA` |
| Employment Type | 2 characters | `Full-time` → `FU` |

> ⚠️ **Recommendation:** For consistent IDs, always set the `custom_abbr` field on your records after running the migration script. Fallback to first N characters can lead to confusing abbreviations.

### Custom Abbreviation Mapping (Optional Override)

After running the custom field migration, abbreviations are managed directly on the doctype records. However, you can still use config-based overrides for special cases:

```json
{
  "hr_employee_id_settings": {
    "enabled": true,
    "pattern": "{DEPARTMENT_ABBR}-{####}",
    "abbreviations": {
      "departments": {
        "Information Technology": "IT",
        "Human Resources": "HR"
      },
      "branches": {
        "Head Office": "HO"
      },
      "employment_types": {
        "Full-time": "FT",
        "Part-time": "PT"
      }
    }
  }
}
```

> **Note:** Config overrides take precedence over `custom_abbr` field values. Use config only when you need to override the doctype field value for specific cases.

---

## Validation

### Uniqueness Validation

The system **always validates uniqueness** before saving. If a duplicate is found:
1. The counter increments automatically
2. A new ID is generated
3. Process repeats until a unique ID is found (max 100 attempts)

### Pattern Validation

The system validates patterns on startup to ensure:
- At least one counter token (`{#...}`) exists
- All tokens are recognized
- Tokens map to valid Employee doctype fields

---

## Manual Override

When `allow_manual_override` is `true`:
- Users can manually enter an employee ID in the form
- If the field is left empty, auto-generation kicks in
- Manual IDs are still validated for uniqueness

---

## Complete Configuration Example

```json
{
  "hr_employee_id_settings": {
    "enabled": true,
    "pattern": "{COMPANY_ABBR}-{DEPARTMENT_ABBR}-{YY}-{####}",
    "allow_manual_override": false,
    "case_format": "upper",
    "abbreviations": {
      "departments": {
        "Information Technology": "IT",
        "Human Resources": "HR",
        "Finance & Accounts": "FIN",
        "Operations": "OPS"
      },
      "employment_types": {
        "Full-time": "FT",
        "Part-time": "PT",
        "Contract": "CT"
      }
    }
  }
}
```

**Output Examples:**
- TickTix LLC, IT Department, 2025: `TTX-IT-25-0001`
- TickTix LLC, HR Department, 2025: `TTX-HR-25-0001`
- TickTix LLC, IT Department, 2026: `TTX-IT-26-0001` (counter auto-reset due to `{YY}` in pattern)

---

## Troubleshooting

### Token Not Resolving

**Problem:** Token appears as literal text in output (e.g., `{DEPARTMENT_ABBR}`)

**Solution:**
1. Ensure the field is filled in the Employee form before saving
2. Check if the linked doctype exists (Department, Branch, etc.)
3. Verify the field name is correct in Employee doctype

### Duplicate IDs Generated

**Problem:** Getting duplicate employee IDs

**Solution:**
1. Ensure the counter scope matches your pattern (auto-detected)
2. If using date-based patterns, verify date tokens are included
3. Check counter storage is persisting correctly

---

## API Reference

### Generate Employee ID

```python
from frappe_ticktix.plugins.hr.employee_id_generator import generate_employee_id

# Called automatically on Employee before_insert
# Or manually:
employee_id = generate_employee_id(employee_doc)
```

### Preview Employee ID

```python
from frappe_ticktix.plugins.hr.employee_id_generator import preview_employee_id

# Preview what ID would be generated (without incrementing counter)
preview_id = preview_employee_id(employee_doc)
```

### Validate Pattern

```python
from frappe_ticktix.plugins.hr.employee_id_generator import validate_pattern

# Validate a pattern string
is_valid, errors = validate_pattern("{COMPANY_ABBR}-{####}")
```

### Get Next Counter (Internal)

```python
from frappe_ticktix.plugins.hr.employee_id_generator.counter_manager import get_next_counter

# Get next counter value for a scope key
counter = get_next_counter("emp_id_counter:dept:IT:year:25")
```

---

## Hooks Integration

The plugin hooks into the Employee doctype via the main `frappe_ticktix/hooks.py`:

### **Registration in hooks.py:**
```python
# In frappe_ticktix/hooks.py
doc_events = {
    "Employee": {
        "before_insert": "frappe_ticktix.plugins.hr.employee_id_generator.hooks.before_insert_employee",
        "validate": "frappe_ticktix.plugins.hr.employee_id_generator.hooks.validate_employee"
    }
}
```

### **Hook Methods:**

| Hook | DocType | Method | Purpose |
|------|---------|--------|---------|
| `before_insert` | Employee | `before_insert_employee` | Generate employee ID before saving |
| `validate` | Employee | `validate_employee` | Validate uniqueness of ID |

### **Implementation Pattern (following existing plugins):**

```python
# frappe_ticktix/plugins/hr/employee_id_generator/hooks.py
import frappe
from frappe_ticktix.plugins.hr.employee_id_generator.id_generator import generate_employee_id
from frappe_ticktix.plugins.hr.employee_id_generator.validators import validate_employee_id

def before_insert_employee(doc, method):
    """
    Hook: before_insert for Employee doctype
    Generates employee ID if auto-generation is enabled
    """
    generate_employee_id(doc)

def validate_employee(doc, method):
    """
    Hook: validate for Employee doctype
    Validates employee ID uniqueness
    """
    validate_employee_id(doc)
```

---

## Custom Field Migration

Before using this plugin, you need to add the `custom_abbr` field to Department, Branch, and Employment Type doctypes.

### Migration Script

Run this script to create the custom fields:

```python
# File: frappe_ticktix/patches/add_abbr_custom_fields.py
# Run: bench --site <sitename> execute frappe_ticktix.patches.add_abbr_custom_fields.execute

import frappe

def execute():
    """Add custom_abbr field to Department, Branch, and Employment Type doctypes"""
    
    custom_fields = [
        {
            "doctype": "Department",
            "fieldname": "custom_abbr",
            "label": "Abbreviation",
            "fieldtype": "Data",
            "insert_after": "department_name",
            "description": "Short code for Employee ID generation (e.g., IT, HR, FIN)",
            "length": 10
        },
        {
            "doctype": "Branch",
            "fieldname": "custom_abbr",
            "label": "Abbreviation",
            "fieldtype": "Data",
            "insert_after": "branch",
            "description": "Short code for Employee ID generation (e.g., HO, BR01)",
            "length": 10
        },
        {
            "doctype": "Employment Type",
            "fieldname": "custom_abbr",
            "label": "Abbreviation",
            "fieldtype": "Data",
            "insert_after": "employee_type_name",
            "description": "Short code for Employee ID generation (e.g., FT, PT, CT)",
            "length": 10
        }
    ]
    
    for field_def in custom_fields:
        doctype = field_def.pop("doctype")
        fieldname = field_def["fieldname"]
        
        # Check if field already exists
        if frappe.db.exists("Custom Field", {"dt": doctype, "fieldname": fieldname}):
            print(f"✓ Custom field '{fieldname}' already exists in {doctype}")
            continue
        
        # Create custom field
        custom_field = frappe.get_doc({
            "doctype": "Custom Field",
            "dt": doctype,
            **field_def
        })
        custom_field.insert(ignore_permissions=True)
        print(f"✓ Created custom field '{fieldname}' in {doctype}")
    
    frappe.db.commit()
    print("\n✅ Custom field migration complete!")

if __name__ == "__main__":
    execute()
```

### Running the Migration

```bash
# Option 1: Run as a patch
cd /home/sagivasan/ticktix
bench --site ticktix.local execute frappe_ticktix.patches.add_abbr_custom_fields.execute

# Option 2: Run in console
bench --site ticktix.local console
>>> from frappe_ticktix.patches.add_abbr_custom_fields import execute
>>> execute()
```

### Verifying Custom Fields

After running the migration, verify the fields exist:

```bash
bench --site ticktix.local console
>>> frappe.get_meta("Department").has_field("custom_abbr")
True
>>> frappe.get_meta("Branch").has_field("custom_abbr")
True
>>> frappe.get_meta("Employment Type").has_field("custom_abbr")
True
```

### Setting Abbreviations

After migration, set abbreviations for existing records:

```python
# Quick script to set department abbreviations
import frappe

departments = {
    "Information Technology": "IT",
    "Human Resources": "HR",
    "Finance & Accounts": "FIN",
    "Operations": "OPS",
    "Security Services": "SEC",
    "Administration": "ADM",
    "Sales & Marketing": "SLS"
}

for dept_name, abbr in departments.items():
    if frappe.db.exists("Department", dept_name):
        frappe.db.set_value("Department", dept_name, "custom_abbr", abbr)
        print(f"✓ Set {dept_name} → {abbr}")

frappe.db.commit()
```

---

## Migration from Manual IDs

If migrating from manual employee IDs:

1. Set `allow_manual_override: true` initially
2. Existing employees keep their IDs
3. New employees get auto-generated IDs
4. Once migrated, set `allow_manual_override: false`

---

## Performance Considerations

- Counter values are stored in database for persistence
- Abbreviation lookups are cached in memory
- Pattern parsing happens once at startup
- Typical ID generation: < 10ms

---

## Quick Reference

### Minimal Setup
```json
{
  "hr_employee_id_settings": {
    "enabled": true,
    "pattern": "EMP-{####}"
  }
}
```

### With Department Scope (auto-detected)
```json
{
  "hr_employee_id_settings": {
    "enabled": true,
    "pattern": "{DEPARTMENT_ABBR}-{####}"
  }
}
```

### With Yearly Reset (auto-detected)
```json
{
  "hr_employee_id_settings": {
    "enabled": true,
    "pattern": "EMP-{YYYY}-{####}"
  }
}
```

### Full Multi-level Pattern
```json
{
  "hr_employee_id_settings": {
    "enabled": true,
    "pattern": "{COMPANY_ABBR}-{DEPARTMENT_ABBR}-{YY}-{####}",
    "abbreviations": {
      "departments": {
        "Information Technology": "IT",
        "Human Resources": "HR"
      }
    }
  }
}
```

---

## Changelog

### Version 1.0.0 (November 2025)
- Initial implementation
- Pattern-based ID generation with auto-detected counter scoping
- Support for Employee doctype field tokens (Company, Department, Branch, Employment Type)
- Date tokens with automatic yearly/monthly scoping
- Custom abbreviation mapping
- Uniqueness validation

---

## Development Guidelines

This plugin follows the established **frappe_ticktix plugin architecture**. When extending or modifying:

### **1. Follow Existing Patterns**

Reference these existing plugins for code style and structure:
- `plugins/hr/attendance/` - DocType hooks and manager pattern
- `plugins/hr/checkin/` - API endpoints and validation
- `plugins/branding/logo_manager.py` - Configuration integration

### **2. Use Config Manager**

```python
# Always use the centralized config manager
from frappe_ticktix.core.config_manager import get_config_manager

def get_employee_id_settings():
    config = get_config_manager()
    return config.get_config_value('hr_employee_id_settings', {})
```

### **3. Error Handling**

```python
import frappe

def generate_employee_id(doc):
    try:
        # Generation logic
        pass
    except Exception as e:
        frappe.log_error(f"Employee ID generation failed: {e}", "HR Employee ID Plugin")
        frappe.throw(f"Could not generate Employee ID: {str(e)}")
```

### **4. Testing**

```bash
# Run plugin tests
cd /home/sagivasan/ticktix
bench --site ticktix.local run-tests --app frappe_ticktix --module frappe_ticktix.plugins.hr.employee_id_generator

# Quick test in console
bench --site ticktix.local console
>>> from frappe_ticktix.plugins.hr.employee_id_generator import preview_employee_id
>>> preview_employee_id(frappe.get_doc("Employee", "EMP-001"))
```

### **5. Documentation**

Keep this documentation updated when:
- Adding new tokens
- Changing configuration options
- Modifying counter scoping logic
- Adding new API endpoints

---

## See Also

- [Plugin Development Guide](DEVELOPMENT_GUIDE.md)
- [HR Plugin README](../../frappe_ticktix/plugins/hr/README.md)
- [Configuration Summary](../configuration/CONFIGURATION_SUMMARY.md)
- [Architecture Overview](../architecture/CURRENT_STRUCTURE.md)

