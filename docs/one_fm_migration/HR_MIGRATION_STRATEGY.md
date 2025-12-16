# frappe_ticktix HR Migration Strategy

**Context:** frappe_ticktix is a **facility management tool** with:
- ✅ Authentication (TickTix OAuth/JWT) 
- ✅ Branding (Dynamic logos)
- 🔄 HR Features (to be migrated from one_fm)

---

## 🎯 Migration Approach

### **Why Not Install one_fm?**
- ❌ Compatibility issues with current apps
- ❌ Monolithic structure conflicts with plugin architecture
- ❌ Contains bloat we don't need

### **Strategy: Extract & Adapt**
✅ Extract needed HR features from one_fm  
✅ Adapt to frappe_ticktix plugin architecture  
✅ Integrate with TickTix authentication  
✅ One feature at a time, tested incrementally  

---

## 📦 one_fm HR Features Available

### **1. Operations Module** (`apps/one_fm/one_fm/operations/`)
Core facility management operations:
- Shift management
- Roster planning
- Attendance tracking
- Site operations
- Checkpoint management
- Cleaning/maintenance tasks

### **2. Hiring Module** (`apps/one_fm/one_fm/hiring/`)
Recruitment & onboarding:
- Employee onboarding
- Hiring workflows
- ERF (Employee Requisition Form)

### **3. HR Overrides** (`apps/one_fm/one_fm/overrides/`)
Customizations to standard ERPNext HR:
- Salary slip customizations
- Payroll entry modifications
- Leave management overrides
- Attendance overrides

---

## 🚀 Quick Start: First Migration

### **Recommended First Feature: Shift Management**

**Why Start Here?**
- ✅ Core to facility management
- ✅ Self-contained functionality
- ✅ Medium complexity (good learning curve)
- ✅ Foundation for attendance & roster

### **Implementation Steps:**

#### 1. Create Plugin Structure
```bash
cd /home/sagivasan/ticktix/apps/frappe_ticktix

# Create HR plugin
mkdir -p frappe_ticktix/plugins/hr/{shifts,attendance,roster}
touch frappe_ticktix/plugins/hr/__init__.py
touch frappe_ticktix/plugins/hr/shifts/__init__.py
```

#### 2. Extract Shift Logic from one_fm
```bash
# Find shift-related files in one_fm
find apps/one_fm -name "*shift*" -type f | grep -E "\.py$|\.json$"
```

#### 3. Create Shift Manager in frappe_ticktix
```python
# frappe_ticktix/plugins/hr/shifts/shift_manager.py
"""
Shift Management for Facility Management
Adapted from one_fm with improvements
"""

import frappe
from frappe import _

@frappe.whitelist()
def get_shift_schedule(employee, date):
    """Get employee shift schedule for date"""
    pass

@frappe.whitelist()
def create_shift_assignment(employee, shift_type, from_date, to_date):
    """Assign shift to employee"""
    pass

def validate_shift_assignment(doc, method):
    """Validate shift assignment"""
    pass
```

#### 4. Register in hooks.py
```python
# frappe_ticktix/hooks.py

# HR - Shift Management
override_whitelisted_methods.update({
    "frappe_ticktix.plugins.hr.shifts.shift_manager.get_shift_schedule": 
        "frappe_ticktix.plugins.hr.shifts.shift_manager.get_shift_schedule",
    "frappe_ticktix.plugins.hr.shifts.shift_manager.create_shift_assignment": 
        "frappe_ticktix.plugins.hr.shifts.shift_manager.create_shift_assignment",
})

doc_events.update({
    "Shift Assignment": {
        "validate": "frappe_ticktix.plugins.hr.shifts.shift_manager.validate_shift_assignment"
    }
})
```

---

## 📋 Next Steps - What Do You Want to Do?

### **Option A: Start with Analysis** 
```bash
# I'll analyze one_fm's shift management code
# Extract the logic, dependencies, and structure
# Create a migration blueprint
```

### **Option B: Start Building**
```bash
# Create the plugin structure for HR
# Implement first feature (shifts/attendance)
# Test and iterate
```

### **Option C: Fix one_fm Installation**
```bash
# Fix the lending app compatibility issue
# Get one_fm running
# Then gradually migrate features
```

---

## ❓ Questions for You:

1. **Which HR feature is most urgent?**
   - [ ] Shift management
   - [ ] Attendance tracking
   - [ ] Leave management
   - [ ] Payroll
   - [ ] Other: ___________

2. **Do you want to:**
   - [ ] Start fresh (build in frappe_ticktix)
   - [ ] Try to fix one_fm installation first
   - [ ] Analyze one_fm code first, then decide

3. **Timeline:**
   - When do you need the first HR feature working?
   - Is this for development or production?

---

## 🎯 Recommended Path Forward

**My Recommendation:**

1. ✅ **First:** Analyze one_fm shift & attendance modules (1-2 days)
2. ✅ **Second:** Create HR plugin structure in frappe_ticktix (1 day)
3. ✅ **Third:** Migrate shift management (1 week)
4. ✅ **Fourth:** Migrate attendance tracking (1 week)
5. ✅ **Fifth:** Test thoroughly (2-3 days)

Then repeat for other HR features as needed.

---

**Ready to start! What would you like to tackle first?** 🚀
