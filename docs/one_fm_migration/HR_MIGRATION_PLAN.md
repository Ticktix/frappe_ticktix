# HR Feature Migration Plan: one_fm → frappe_ticktix

**Date:** October 20, 2025  
**Objective:** Migrate HR features from one_fm to frappe_ticktix incrementally

---

## 🎯 Current Status

### ✅ frappe_ticktix - Complete
- **Authentication System** - TickTix OAuth/JWT integration ✅
- **Branding System** - Dynamic logo management ✅
- **Plugin Architecture** - Clean, modular structure ✅

### 📦 one_fm - Source for HR Features
- **Issue:** Cannot install directly due to compatibility issues
- **Solution:** Extract and migrate HR features incrementally

---

## 🚫 Why Not Install one_fm Directly?

The current installation fails because:
1. **Compatibility Issues:**
   - `lending` app version mismatch
   - Missing function: `get_outstanding_invoices` from loan_repayment
   - Designed for different ERPNext/Frappe versions

2. **Architecture Conflict:**
   - one_fm has monolithic structure
   - frappe_ticktix uses plugin architecture
   - Direct installation would create maintenance nightmare

---

## ✅ Recommended Migration Strategy

### **Phase 1: HR Core Features** (Priority 1)

Extract basic HR functionality:

```
one_fm/one_fm/
├── doctype/
│   ├── employee_attendance/       → frappe_ticktix/plugins/hr/attendance/
│   ├── shift_management/          → frappe_ticktix/plugins/hr/shifts/
│   ├── leave_management/          → frappe_ticktix/plugins/hr/leave/
│   └── employee_checkin/          → frappe_ticktix/plugins/hr/checkin/
```

**Features to migrate:**
- Employee attendance tracking
- Shift scheduling
- Leave management
- Check-in/Check-out system

### **Phase 2: Payroll Integration** (Priority 2)

```
one_fm/overrides/
├── salary_slip.py                 → frappe_ticktix/plugins/hr/payroll/
├── payroll_entry.py               → frappe_ticktix/plugins/hr/payroll/
└── additional_salary.py           → frappe_ticktix/plugins/hr/payroll/
```

**Note:** Will need to fix lending app dependencies

### **Phase 3: Advanced HR Features** (Priority 3)

```
one_fm/hiring/                     → frappe_ticktix/plugins/hr/recruitment/
one_fm/operations/                 → frappe_ticktix/plugins/operations/
```

---

## 📋 Step-by-Step Migration Process

### Step 1: Analyze one_fm HR Structure

```bash
# List all HR-related doctypes
find /home/sagivasan/ticktix/apps/one_fm -type f -name "*.json" | grep -E "employee|attendance|shift|leave"

# List HR controllers
find /home/sagivasan/ticktix/apps/one_fm -type f -name "*.py" | grep -E "employee|attendance|shift|leave"
```

### Step 2: Create Plugin Structure in frappe_ticktix

```bash
cd /home/sagivasan/ticktix/apps/frappe_ticktix

# Create HR plugin structure
mkdir -p frappe_ticktix/plugins/hr/{attendance,shifts,leave,checkin,payroll}
mkdir -p frappe_ticktix/plugins/hr/doctype
```

### Step 3: Extract First Feature (e.g., Attendance)

```python
# frappe_ticktix/plugins/hr/attendance/attendance_manager.py

"""
Attendance Management Module
Migrated from one_fm with improvements
"""

import frappe
from frappe import _

class AttendanceManager:
    """
    Manages employee attendance tracking
    Source: one_fm.one_fm.doctype.employee_attendance
    """
    
    def validate_attendance(self, doc, method):
        """Validate attendance record"""
        pass
    
    def mark_attendance(self, employee, date, status):
        """Mark attendance for employee"""
        pass
    
    def get_attendance_summary(self, employee, from_date, to_date):
        """Get attendance summary for period"""
        pass
```

### Step 4: Register in hooks.py

```python
# Add to frappe_ticktix/hooks.py

doc_events = {
    "Attendance": {
        "validate": "frappe_ticktix.plugins.hr.attendance.attendance_manager.validate_attendance",
        "on_submit": "frappe_ticktix.plugins.hr.attendance.attendance_manager.on_attendance_submit"
    }
}
```

### Step 5: Test Each Feature Before Moving to Next

```bash
# Run tests for migrated feature
bench --site ticktix.local run-tests --app frappe_ticktix --module hr.attendance
```

---

## 🔍 First Feature to Migrate: Employee Attendance

Let me analyze what's in one_fm's attendance system:

```bash
# Check one_fm attendance structure
find apps/one_fm -path "*attendance*" -type f | head -20
```

Would you like me to:
1. ✅ Analyze one_fm's HR structure and create a detailed feature inventory
2. ✅ Extract the first HR feature (attendance/shift management)
3. ✅ Create the plugin structure for HR in frappe_ticktix
4. ✅ Start with a specific HR feature you need most urgently

**Which HR feature from one_fm do you need first?**
- Attendance tracking
- Shift management
- Leave management
- Payroll
- Other?

---

## 🎯 Benefits of This Approach

### vs. Installing one_fm Directly:
- ✅ **No Compatibility Issues** - Clean migration
- ✅ **Plugin Architecture** - Maintains your clean structure
- ✅ **Incremental Testing** - Test each feature as you go
- ✅ **Code Quality** - Improve code while migrating
- ✅ **No Bloat** - Only migrate what you need

### Migration Benefits:
- ✅ **TickTix Integration** - HR features work with TickTix auth
- ✅ **Unified Branding** - Consistent with your logo system
- ✅ **Better Maintainability** - One app instead of two
- ✅ **Modern Code** - Update during migration

---

## 📊 Estimated Effort

| Phase | Features | Complexity | Time Estimate |
|-------|----------|------------|---------------|
| Phase 1 | Attendance, Shifts, Leave | Medium | 2-3 weeks |
| Phase 2 | Payroll Integration | High | 3-4 weeks |
| Phase 3 | Advanced HR | Medium | 2-3 weeks |

**Total:** 7-10 weeks for complete HR migration

---

*Ready to start the HR migration! Let me know which feature to tackle first.* 🚀
