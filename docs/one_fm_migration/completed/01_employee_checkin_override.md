# Employee Checkin Override# Employee Checkin Module - Override Documentation# Employee Checkin Module - Override Documentation



**Module:** Employee Checkin  

**Status:** ✅ Complete  

**LOC:** ~450 lines**Module:** Employee Checkin  **Module:** Employee Checkin  



---**Plugin:** `frappe_ticktix.plugins.hr.checkin`  **Plugin:** `frappe_ticktix.plugins.hr.checkin`  



## 🔵 What Frappe Has**Status:** ✅ Completed  **Status:** ✅ Completed  



- Basic Employee Checkin doctype**Date:** October 25, 2025**Date:** October 25, 2025

- Employee validation

- Optional shift linking

- Standard CRUD

------

## 🟢 What We Added



| Feature | Frappe | Our Override |

|---------|--------|--------------|## ℹ️ About This Document## 📋 Table of Contents

| Duplicate detection | ❌ | ✅ |

| Auto-detect shift | ❌ | ✅ |

| Late entry flag | ❌ | ✅ |

| Early exit flag | ❌ | ✅ |This document shows **what Frappe provides by default** vs **what we've overridden** in the Employee Checkin module. For code implementation, see `frappe_ticktix/plugins/hr/checkin/checkin_manager.py`.1. [Frappe Default Functionality](#frappe-default-functionality)

| Supervisor notifications | ❌ | ✅ |

| Background processing | ❌ | ✅ |2. [What We've Overridden](#what-weve-overridden)

| Grace period support | ❌ | ✅ |

| Time window validation | ❌ | ✅ |---3. [Additional Features Added](#additional-features-added)



## 📊 Methods Override4. [API Endpoints](#api-endpoints)



| Method | Enhancement |## 🔵 Frappe Default Functionality5. [Database Schema](#database-schema)

|--------|-------------|

| `validate()` | Added duplicate check, shift detection, late/early flags |6. [Comparison Table](#comparison-table)

| `before_insert()` | Auto-set date from time |

| `after_insert()` | Background notifications |### **Default DocType: Employee Checkin**



## 🌐 APIs Added**Location:** `hrms/hr/doctype/employee_checkin/`---



1. `get_current_shift_for_employee` - Get active shift

2. `create_checkin` - Create with validation

**Default Fields:**## ℹ️ About This Document

## 🎯 Summary

- name (ID)

**Added:** 6 new validations, 2 APIs, background notifications  

**From one_fm:** Migrated duplicate detection, shift auto-detection, late/early flagging  - employee (Link)This document shows **what Frappe provides by default** vs **what we've overridden** in the Employee Checkin module. It focuses on the differences and improvements without including code examples. For code implementation, see the source files in `frappe_ticktix/plugins/hr/checkin/`.

**Integration:** Document event hooks (no core changes)

- employee_name (Data)

---

- log_type (Select: IN/OUT)---

*For code: see `frappe_ticktix/plugins/hr/checkin/checkin_manager.py`*

- time (Datetime)

- device_id (Data)## 🔵 Frappe Default Functionality

- skip_auto_attendance (Check)

- shift, shift_start, shift_end### **Default DocType: Employee Checkin**

- shift_actual_start, shift_actual_end

**Location:** `hrms/hr/doctype/employee_checkin/`

**Default Validation:**

- ✅ Validates employee is active**Default Fields:**

- ✅ Links to shift if available```python

- ❌ No duplicate detection{

- ❌ No late/early detection    "name": "Unique ID",

- ❌ No supervisor notifications    "employee": "Link to Employee",

- ❌ No automatic shift assignment    "employee_name": "Employee Name (auto-fetched)",

    "log_type": "IN or OUT",

---    "time": "Datetime of checkin/checkout",

    "device_id": "Device identifier (optional)",

## 🟢 What We've Overridden    "skip_auto_attendance": "Boolean (0 or 1)",

    "shift": "Link to Shift Type",

### **1. Enhanced validate() Method**    "shift_start": "Shift start time",

    "shift_end": "Shift end time",

| Feature | Frappe Default | Our Override |    "shift_actual_start": "Actual shift start",

|---------|----------------|--------------|    "shift_actual_end": "Actual shift end"

| Employee validation | ✅ Yes | ✅ Yes (kept) |}

| Duplicate detection | ❌ No | ✅ **Added** - Prevents same-time checkins |```

| Shift detection | ❌ No | ✅ **Added** - Auto-finds current shift |

| Late entry flag | ❌ No | ✅ **Added** - With grace period |**Default Controller:** `employee_checkin.py`

| Early exit flag | ❌ No | ✅ **Added** - With grace period |

| Error messages | ⚠️ Basic | ✅ **Improved** - With clickable links |```python

class EmployeeCheckin(Document):

### **2. before_insert() Method**    def validate(self):

        # Basic validation

| Feature | Frappe Default | Our Override |        validate_active_employee(self.employee)

|---------|----------------|--------------|    

| Auto-set date | ❌ No | ✅ **Added** - Date from time |    @frappe.whitelist()

    def fetch_shift(self):

### **3. after_insert() Method**        # Fetch shift details for the employee

        pass

| Feature | Frappe Default | Our Override |```

|---------|----------------|--------------|

| Background processing | ❌ No | ✅ **Added** - Async notifications |**Default Validation:**

| Supervisor notifications | ❌ No | ✅ **Added** - Email alerts |- ✅ Validates employee is active

| Error logging | ❌ No | ✅ **Added** - Comprehensive logging |- ✅ Links to shift if available

- ❌ No duplicate detection

---- ❌ No late/early detection

- ❌ No supervisor notifications

## 🆕 Additional Features Added- ❌ No automatic shift assignment



### **Helper Class: EmployeeCheckinManager****Default Behavior:**

- Creates checkin record

| Method | Purpose | Frappe Equivalent |- Optionally links to shift

|--------|---------|-------------------|- Can be used for auto-attendance marking

| `validate_duplicate_log()` | Check for duplicate checkins | ❌ None |- Basic validation only

| `get_current_shift()` | Find active shift with time windows | ⚠️ Partial |

| `calculate_late_early_flags()` | Detect late/early with grace | ❌ None |---



### **Notification System**## 🟢 What We've Overridden



| Function | Purpose | Frappe Equivalent |### **Our Override: EmployeeCheckinOverride**

|----------|---------|-------------------|

| `notify_late_checkin()` | Email supervisor for late arrivals | ❌ None |**Location:** `frappe_ticktix/plugins/hr/checkin/checkin_manager.py`

| `notify_early_checkout()` | Email supervisor for early exits | ❌ None |

| `process_checkin_background()` | Async notification processing | ❌ None |**Class Definition:**

```python

---class EmployeeCheckinOverride(EmployeeCheckin):

    """

## 🌐 API Endpoints    Extends Frappe's default EmployeeCheckin with:

    - Duplicate detection

### **1. get_current_shift_for_employee**    - Automatic shift assignment

- **Purpose:** Get active shift for employee    - Late/early detection

- **Frappe Equivalent:** ❌ None    - Supervisor notifications

- **Parameters:** employee (optional - defaults to current user)    - Background processing

- **Returns:** Shift details with start/end times    """

```

### **2. create_checkin**

- **Purpose:** Create validated checkin record### **1. Enhanced validate() Method**

- **Frappe Equivalent:** ⚠️ Partial (basic create, no validation)

- **Parameters:** employee, log_type, time, device_id, skip_auto_attendance**Frappe Default:**

- **Returns:** Created checkin with late/early flags```python

def validate(self):

---    validate_active_employee(self.employee)

```

## 🗄️ Database Schema

**Our Override:**

### **Fields We Use**```python

def validate(self):

| Field | Frappe Default | Our Usage |    # ✅ Frappe default validation

|-------|----------------|-----------|    validate_active_employee(self.employee)

| employee | ✅ Required | ✅ Same |    

| time | ✅ Required | ✅ Same |    # ➕ NEW: Check for duplicate checkin

| log_type | ✅ Required (IN/OUT) | ✅ Same |    duplicate = EmployeeCheckinManager.validate_duplicate_log(

| device_id | ✅ Optional | ✅ Same |        self.employee, 

| shift_assignment | ⚠️ Manual | ✅ **Auto-populated** |        self.time, 

| shift_type | ⚠️ Manual | ✅ **Auto-populated** |        self.name

| late_entry | ❌ N/A | ✅ **Calculated & set** |    )

| early_exit | ❌ N/A | ✅ **Calculated & set** |    

| date | ❌ N/A | ✅ **Auto-set from time** |    if duplicate:

        doc_link = frappe.get_desk_link("Employee Checkin", duplicate.name)

---        frappe.throw(

            _("This employee already has a log with the same timestamp. {0}").format(doc_link)

## 📊 Comparison Table        )

    

| Feature | Frappe Default | Our Override | Improvement |    # ➕ NEW: Auto-detect current shift

|---------|----------------|--------------|-------------|    if not self.shift_assignment:

| **Validation** | | | |        curr_shift = EmployeeCheckinManager.get_current_shift(

| Active employee check | ✅ | ✅ | Same |            self.employee, 

| Duplicate detection | ❌ | ✅ | **NEW** |            self.time

| Shift validation | ⚠️ Basic | ✅ Enhanced | **Better** |        )

| **Shift Detection** | | | |        

| Manual shift entry | ✅ | ✅ | Same |        if curr_shift:

| Auto-detect shift | ❌ | ✅ | **NEW** |            self.shift_assignment = curr_shift['name']

| Time window check | ❌ | ✅ | **NEW** |            self.shift = curr_shift['shift_type']

| Overnight shift support | ⚠️ Partial | ✅ Full | **Better** |            self.shift_type = curr_shift['shift_type']

| **Late/Early Detection** | | | |            self.shift_actual_start = curr_shift['start_datetime']

| Late entry flag | ❌ | ✅ | **NEW** |            self.shift_actual_end = curr_shift['end_datetime']

| Early exit flag | ❌ | ✅ | **NEW** |            

| Grace period support | ❌ | ✅ | **NEW** |            # ➕ NEW: Calculate late/early flags

| Supervisor notification | ❌ | ✅ | **NEW** |            flags = EmployeeCheckinManager.calculate_late_early_flags(

| **Processing** | | | |                self.time,

| Synchronous save | ✅ | ✅ | Same |                curr_shift['start_datetime'],

| Background processing | ❌ | ✅ | **NEW** |                curr_shift['end_datetime'],

| Error logging | ⚠️ Basic | ✅ Enhanced | **Better** |                curr_shift['shift_type_doc'],

| **API** | | | |                self.log_type

| Standard CRUD API | ✅ | ✅ | Same |            )

| Get current shift | ❌ | ✅ | **NEW** |            

| Create with validation | ⚠️ Basic | ✅ Enhanced | **Better** |            self.late_entry = flags['late_entry']

| Mobile app ready | ⚠️ Partial | ✅ Full | **Better** |            self.early_exit = flags['early_exit']

```

---

**What Changed:**

## 🎯 Summary- ✅ **Kept:** Employee active validation

- ➕ **Added:** Duplicate detection with error message and link

### **What Frappe Provides**- ➕ **Added:** Automatic shift detection from current time

1. Basic Employee Checkin doctype- ➕ **Added:** Late entry flag (respects grace period)

2. Employee validation- ➕ **Added:** Early exit flag (respects grace period)

3. Optional shift linking- ➕ **Added:** Auto-populate shift fields

4. Standard CRUD operations

---

### **What We Added**

1. ✅ Duplicate detection with helpful error messages### **2. Enhanced before_insert() Method**

2. ✅ Automatic shift detection from current time

3. ✅ Late/early detection with grace period support**Frappe Default:**

4. ✅ Supervisor email notifications```python

5. ✅ Background processing for notifications# No before_insert() method in default implementation

6. ✅ Enhanced API endpoints for mobile apps```

7. ✅ Time window validation (before/after shift times)

8. ✅ Overnight shift support**Our Override:**

9. ✅ Comprehensive error logging```python

def before_insert(self):

### **Integration Method**    """Set date from time"""

- Uses Frappe's **document event hooks** (no core modifications)    self.date = getdate(self.time)

- Hooks registered in `hooks.py````

- Can be disabled by removing hooks

- Fully backward compatible**What Changed:**

- ➕ **Added:** Auto-set date field from time (convenience)

### **From one_fm to frappe_ticktix**

**Migrated:**---

- ✅ Duplicate detection

- ✅ Shift auto-detection### **3. Enhanced after_insert() Method**

- ✅ Late/early flagging

- ✅ Supervisor notifications**Frappe Default:**

```python

**Simplified:**# No after_insert() method in default implementation

- ✅ Removed GPS validation (can be re-added)```

- ✅ Removed photo capture (can be re-added)

- ✅ Removed operations shift dependencies**Our Override:**

```python

**Improved:**def after_insert(self):

- ✅ Cleaner code structure    """

- ✅ Better error messages    Post-insert processing

- ✅ Standard hooks usage    - Send notifications

- ✅ Enhanced documentation    - Update shift details in background

    """

---    try:

        frappe.db.commit()

*Last Updated: October 25, 2025*        self.reload()

        
        # ➕ Enqueue background processing
        frappe.enqueue(
            'frappe_ticktix.plugins.hr.checkin.checkin_manager.process_checkin_background',
            employee_checkin=self.name,
            queue='default',
            timeout=300
        )
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), 'Employee Checkin After Insert')
```

**What Changed:**
- ➕ **Added:** Background processing queue
- ➕ **Added:** Error logging
- ➕ **Added:** Notification system

---

### **4. Background Processing**

**Frappe Default:**
```python
# No background processing
```

**Our Addition:**
```python
def process_checkin_background(employee_checkin):
    """
    Background processing for checkin
    - Update shift details
    - Send supervisor notifications
    """
    try:
        checkin = frappe.get_doc("Employee Checkin", employee_checkin)
        
        # Send notifications based on checkin type
        if checkin.log_type == "IN":
            notify_late_checkin(checkin)
        elif checkin.log_type == "OUT":
            notify_early_checkout(checkin)
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), 'Process Checkin Background')
```

**What Added:**
- ➕ **NEW:** Asynchronous notification system
- ➕ **NEW:** Late checkin notifications to supervisor
- ➕ **NEW:** Early checkout notifications to supervisor

---

## 🆕 Additional Features Added

### **1. EmployeeCheckinManager Helper Class**

**Purpose:** Utility methods for checkin operations

**Methods:**

#### `validate_duplicate_log(employee, time, name)`
```python
@staticmethod
def validate_duplicate_log(employee, time, name=None):
    """
    Check if a checkin already exists for the same employee at the same time
    
    Returns: dict or None
    """
```

**Frappe Equivalent:** ❌ None (we added this)

---

#### `get_current_shift(employee, time)`
```python
@staticmethod
def get_current_shift(employee, time=None):
    """
    Get the current shift assignment for an employee
    Considers check-in window (before/after shift times)
    
    Returns: dict with shift details or None
    """
```

**Frappe Equivalent:** ⚠️ Partial (Frappe has `get_employee_shift`, but doesn't consider time windows)

**Our Enhancement:**
- ✅ Considers `begin_check_in_before_shift_start_time`
- ✅ Considers `allow_check_out_after_shift_end_time`
- ✅ Handles overnight shifts
- ✅ Returns complete shift object with shift_type_doc

---

#### `calculate_late_early_flags(checkin_time, shift_start, shift_end, shift_type, log_type)`
```python
@staticmethod
def calculate_late_early_flags(...):
    """
    Calculate if checkin is late or early based on grace periods
    
    Returns: {'late_entry': bool, 'early_exit': bool}
    """
```

**Frappe Equivalent:** ❌ None (we added this)

**Logic:**
```python
if log_type == 'IN':
    if shift_type.enable_entry_grace_period:
        grace_period = shift_type.late_entry_grace_period or 0
        if checkin_time > (shift_start + timedelta(minutes=grace_period)):
            late_entry = 1

elif log_type == 'OUT':
    if shift_type.enable_exit_grace_period:
        grace_period = shift_type.early_exit_grace_period or 0
        if checkin_time < (shift_end - timedelta(minutes=grace_period)):
            early_exit = 1
```

---

### **2. Notification System**

#### `notify_late_checkin(checkin)`
```python
def notify_late_checkin(checkin):
    """
    Notify supervisor if employee checked in late
    - Calculates delay time
    - Gets reporting manager
    - Sends email notification
    """
```

**Frappe Equivalent:** ❌ None (we added this)

**Features:**
- Calculates exact delay (hours and minutes)
- Finds reporting manager from employee master
- Sends formatted email with checkin details
- Links to checkin record in notification

---

#### `notify_early_checkout(checkin)`
```python
def notify_early_checkout(checkin):
    """
    Notify supervisor if employee checked out early
    - Calculates early departure time
    - Gets reporting manager
    - Sends email notification
    """
```

**Frappe Equivalent:** ❌ None (we added this)

---

## 🌐 API Endpoints

### **1. get_current_shift_for_employee**

**Frappe Equivalent:** ❌ None

**Our Implementation:**
```python
@frappe.whitelist()
def get_current_shift_for_employee(employee=None):
    """
    API method to get current shift for an employee
    Defaults to current user's employee if not specified
    """
```

**Usage:**
```bash
GET /api/method/frappe_ticktix.plugins.hr.checkin.checkin_manager.get_current_shift_for_employee?employee=EMP-001
```

**Response:**
```json
{
  "name": "SHIFT-2025-001",
  "shift_type": "Morning Shift",
  "start_datetime": "2025-10-25 06:00:00",
  "end_datetime": "2025-10-25 14:00:00"
}
```

---

### **2. create_checkin**

**Frappe Equivalent:** ⚠️ Partial (can create via standard API, but no validation)

**Our Implementation:**
```python
@frappe.whitelist()
def create_checkin(employee, log_type, time=None, device_id=None, skip_auto_attendance=0):
    """
    API method to create employee checkin
    - Validates input
    - Auto-detects shift
    - Calculates late/early
    - Returns created document
    """
```

**Usage:**
```bash
POST /api/method/frappe_ticktix.plugins.hr.checkin.checkin_manager.create_checkin
{
  "employee": "EMP-001",
  "log_type": "IN",
  "device_id": "mobile_app_001"
}
```

**Response:**
```json
{
  "name": "HR-EMP-CHK-2025-001",
  "employee": "EMP-001",
  "log_type": "IN",
  "time": "2025-10-25 06:15:00",
  "late_entry": 1,
  "shift_assignment": "SHIFT-2025-001"
}
```

---

## 🗄️ Database Schema

### **Frappe Default Fields**

```
Employee Checkin
├── name (PK)
├── employee (Link)
├── employee_name (Data)
├── log_type (Select: IN/OUT)
├── time (Datetime)
├── device_id (Data)
├── skip_auto_attendance (Check)
├── shift (Link to Shift Type)
├── shift_start (Datetime)
├── shift_end (Datetime)
└── shift_actual_start (Datetime)
```

### **Fields We Use/Populate**

All Frappe fields **PLUS** we populate these additional fields that may exist:

```
Employee Checkin (Our Usage)
├── All Frappe default fields ✅
├── shift_assignment (Link) ➕ We auto-populate
├── shift_type (Link) ➕ We auto-populate
├── operations_shift (Link) ⚠️ If available (one_fm field)
├── late_entry (Check) ➕ We calculate and set
├── early_exit (Check) ➕ We calculate and set
├── roster_type (Select) ⚠️ If available (one_fm field)
└── date (Date) ➕ We auto-set from time
```

**Note:** We don't create custom fields. We use whatever fields are available in the Employee Checkin doctype.

---

## 📊 Comparison Table

| Feature | Frappe Default | Our Override | Improvement |
|---------|----------------|--------------|-------------|
| **Validation** | | | |
| Active employee check | ✅ Yes | ✅ Yes | Same |
| Duplicate detection | ❌ No | ✅ Yes | **NEW** |
| Shift validation | ⚠️ Basic | ✅ Enhanced | **Better** |
| | | | |
| **Shift Detection** | | | |
| Manual shift entry | ✅ Yes | ✅ Yes | Same |
| Auto-detect shift | ❌ No | ✅ Yes | **NEW** |
| Time window check | ❌ No | ✅ Yes | **NEW** |
| Overnight shift support | ⚠️ Partial | ✅ Full | **Better** |
| | | | |
| **Late/Early Detection** | | | |
| Late entry flag | ❌ No | ✅ Yes | **NEW** |
| Early exit flag | ❌ No | ✅ Yes | **NEW** |
| Grace period support | ❌ No | ✅ Yes | **NEW** |
| Supervisor notification | ❌ No | ✅ Yes | **NEW** |
| | | | |
| **Processing** | | | |
| Synchronous save | ✅ Yes | ✅ Yes | Same |
| Background processing | ❌ No | ✅ Yes | **NEW** |
| Error logging | ⚠️ Basic | ✅ Enhanced | **Better** |
| | | | |
| **API** | | | |
| Standard CRUD API | ✅ Yes | ✅ Yes | Same |
| Get current shift | ❌ No | ✅ Yes | **NEW** |
| Create with validation | ⚠️ Basic | ✅ Enhanced | **Better** |
| Mobile app ready | ⚠️ Partial | ✅ Full | **Better** |
| | | | |
| **Notifications** | | | |
| Email on late | ❌ No | ✅ Yes | **NEW** |
| Email on early exit | ❌ No | ✅ Yes | **NEW** |
| Notification links | ❌ No | ✅ Yes | **NEW** |

**Legend:**
- ✅ Fully supported
- ⚠️ Partially supported
- ❌ Not supported
- **NEW** = Feature we added
- **Better** = Enhancement over Frappe default

---

## 🎯 Summary

### **What Frappe Provides**
1. Basic Employee Checkin doctype
2. Employee validation
3. Optional shift linking
4. Standard CRUD operations

### **What We Added**
1. ✅ Duplicate detection with helpful error messages
2. ✅ Automatic shift detection from current time
3. ✅ Late/early detection with grace period support
4. ✅ Supervisor email notifications
5. ✅ Background processing for notifications
6. ✅ Enhanced API endpoints for mobile apps
7. ✅ Time window validation (before/after shift times)
8. ✅ Overnight shift support
9. ✅ Comprehensive error logging

### **What We Kept from Frappe**
1. ✅ Base doctype structure
2. ✅ Employee validation
3. ✅ Standard fields
4. ✅ Permissions system
5. ✅ Database integration

### **Integration Method**
We use Frappe's **document event hooks** to extend functionality without modifying core:

```python
# In hooks.py
doc_events = {
    "Employee Checkin": {
        "validate": "frappe_ticktix.plugins.hr.checkin.checkin_manager.EmployeeCheckinOverride.validate",
        "before_insert": "...",
        "after_insert": "..."
    }
}
```

This means:
- ✅ No core Frappe files modified
- ✅ Clean separation of concerns
- ✅ Easy to maintain and upgrade
- ✅ Can be disabled by removing hooks

---

## 🔄 Migration Path

**From:** one_fm Employee Checkin override  
**To:** frappe_ticktix HR Plugin  

**Changes Made:**
- ✅ Removed Kuwait-specific features (PACI, etc.)
- ✅ Removed operations shift dependencies (will come in operations plugin)
- ✅ Simplified GPS validation (can be re-added)
- ✅ Removed photo capture (can be re-added)
- ✅ Kept core attendance functionality
- ✅ Improved code structure and documentation

---

*Last Updated: October 25, 2025*
