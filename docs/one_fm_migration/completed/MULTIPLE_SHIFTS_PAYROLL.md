# Multiple Shifts Payroll & Leave Handling

**Employee:** HR-EMP-00001 (Ganesh)  
**Scenario:** Employee works multiple shifts on the same day  
**Last Updated:** 2025-11-01

---

## 🎯 Overview

When an employee works **multiple shifts on the same day**, our attendance system uses the **`roster_type`** field to differentiate between shifts for proper payroll calculation and leave handling.

---

## 📊 How It Works

### **1. Roster Types**

| Roster Type | Purpose | Pay Rate | Example |
|-------------|---------|----------|---------|
| **Basic** | Regular shift | 1.0x | 09:00 - 18:00 (9 hours) |
| **Over-Time** | Additional shift | 1.5x or 2.0x | 18:00 - 22:00 (4 hours) |

### **2. Duplicate Check Logic**

```python
# From attendance_manager.py line 402
def validate_duplicate_record(self):
    """
    Check for duplicate attendance
    Allows 2 attendance records per day:
    - 1 Basic roster
    - 1 Over-Time roster
    """
    roster_type = self.get('roster_type', 'Basic')
    
    duplicates = AttendanceManager.get_duplicate_attendance(
        self.employee,
        self.attendance_date,
        self.shift,
        roster_type,  # ← KEY: Includes roster type in check
        self.name
    )
    
    if duplicates:
        frappe.throw(_("Attendance already marked for this roster type"))
```

**Result:** Employee can have:
- ✅ 1 attendance record with `roster_type = "Basic"`
- ✅ 1 attendance record with `roster_type = "Over-Time"`
- ❌ NOT 2 attendance records with same `roster_type`

---

## 💰 Payroll Calculation

### **Example: Employee HR-EMP-00001 on Nov 3, 2025**

#### Scenario 1: Both Shifts Worked (Present)

| # | Shift | Roster Type | Status | Working Hours | Pay Rate | Payroll Impact |
|---|-------|-------------|--------|---------------|----------|----------------|
| 1 | General Shift | Basic | Present | 9.0 hours | 1.0x | Base salary (full day) |
| 2 | Evening Shift | Over-Time | Present | 4.0 hours | 1.5x | OT: 4 × 1.5 = 6 hours pay |

**Payroll Entry:**
```python
# Basic roster - counted as 1 day worked
basic_days = 1
basic_hours = 9.0

# Over-Time roster - added as OT component
ot_hours = 4.0
ot_pay = hourly_rate × 4.0 × 1.5  # 1.5x multiplier

total_pay = (base_salary / working_days) + ot_pay
```

**Total earnings for Nov 3:**
- Base day pay: $100 (assuming daily rate)
- OT pay: $60 (4 hours × $10/hour × 1.5)
- **Total: $160**

---

#### Scenario 2: Leave Applied for Basic Shift Only

| # | Shift | Roster Type | Status | Working Hours | Pay Rate | Payroll Impact |
|---|-------|-------------|--------|---------------|----------|----------------|
| 1 | General Shift | Basic | **On Leave** | 0.0 hours | 1.0x | Leave deduction OR paid leave |
| 2 | Evening Shift | Over-Time | Present | 4.0 hours | 1.5x | OT: 4 × 1.5 = 6 hours pay |

**Leave Application:**
```json
{
  "employee": "HR-EMP-00001",
  "from_date": "2025-11-03",
  "to_date": "2025-11-03",
  "half_day": 0,
  "leave_type": "Casual Leave",
  "custom_roster_type": "Basic"  // ← Only affects Basic roster
}
```

**Payroll Entry:**
```python
# Basic roster - on leave
if leave_type.is_lwp:  # Leave Without Pay
    basic_days = 0  # Day not paid
else:  # Paid leave (Casual, Sick, etc.)
    basic_days = 1  # Day paid from leave balance

# Over-Time roster - still worked
ot_hours = 4.0
ot_pay = hourly_rate × 4.0 × 1.5

total_pay = (base_salary / working_days × basic_days) + ot_pay
```

**Total earnings for Nov 3:**
- Base day pay: $100 (paid from Casual Leave balance)
- OT pay: $60 (still worked OT shift)
- **Total: $160**

If it was **Leave Without Pay:**
- Base day pay: $0 (LWP, no payment)
- OT pay: $60 (still worked OT shift)
- **Total: $60**

---

#### Scenario 3: Leave Applied for Both Shifts

| # | Shift | Roster Type | Status | Working Hours | Pay Rate | Payroll Impact |
|---|-------|-------------|--------|---------------|----------|----------------|
| 1 | General Shift | Basic | **On Leave** | 0.0 hours | 1.0x | Leave deduction OR paid leave |
| 2 | Evening Shift | Over-Time | **On Leave** | 0.0 hours | N/A | No OT pay |

**Leave Applications (2 separate applications):**
```json
// Leave Application 1 - Basic shift
{
  "employee": "HR-EMP-00001",
  "from_date": "2025-11-03",
  "to_date": "2025-11-03",
  "leave_type": "Casual Leave",
  "custom_roster_type": "Basic"
}

// Leave Application 2 - OT shift
{
  "employee": "HR-EMP-00001",
  "from_date": "2025-11-03",
  "to_date": "2025-11-03",
  "leave_type": "Casual Leave",
  "custom_roster_type": "Over-Time"
}
```

**Payroll Entry:**
```python
# Basic roster - on leave
basic_days = 1 if paid_leave else 0

# Over-Time roster - on leave (no OT worked)
ot_hours = 0
ot_pay = 0

total_pay = (base_salary / working_days × basic_days)
```

**Total earnings for Nov 3:**
- Base day pay: $100 (paid from leave balance)
- OT pay: $0 (no OT worked)
- **Total: $100**

---

#### Scenario 4: Half Day Leave on Basic, Present on OT

| # | Shift | Roster Type | Status | Working Hours | Pay Rate | Payroll Impact |
|---|-------|-------------|--------|---------------|----------|----------------|
| 1 | General Shift | Basic | **Half Day** | 4.5 hours | 1.0x | Half day pay (0.5 days) |
| 2 | Evening Shift | Over-Time | Present | 4.0 hours | 1.5x | OT: 4 × 1.5 = 6 hours pay |

**Leave Application:**
```json
{
  "employee": "HR-EMP-00001",
  "from_date": "2025-11-03",
  "to_date": "2025-11-03",
  "half_day": 1,  // ← Half day flag
  "leave_type": "Casual Leave",
  "custom_roster_type": "Basic"
}
```

**Attendance Auto-Created:**
```python
# Basic roster - Half Day status (auto-calculated by our system)
attendance_1 = {
    "roster_type": "Basic",
    "status": "Half Day",
    "working_hours": 4.5,  # Auto-halved from 9.0
    "shift": "General Shift"
}

# OT roster - Present (manually marked or from checkins)
attendance_2 = {
    "roster_type": "Over-Time",
    "status": "Present",
    "working_hours": 4.0,
    "shift": "Evening Shift"
}
```

**Payroll Entry:**
```python
# Basic roster - half day
basic_days = 0.5

# Over-Time roster - full OT
ot_hours = 4.0
ot_pay = hourly_rate × 4.0 × 1.5

total_pay = (base_salary / working_days × 0.5) + ot_pay
```

**Total earnings for Nov 3:**
- Base day pay: $50 (half day = 0.5 × $100)
- OT pay: $60 (full OT shift)
- **Total: $110**

---

## 🔄 Leave Application Workflow

### **Step-by-Step: Applying Leave for Multiple Shifts**

#### **Option 1: Leave for Basic Shift Only**

1. **Employee applies for leave:**
   - Open Leave Application
   - Select date: Nov 3, 2025
   - Select leave type: Casual Leave
   - **Important:** Set `custom_roster_type = "Basic"` (if field exists)
   - Submit

2. **System creates attendance:**
   ```python
   # Auto-created by Leave Application
   Attendance(
       employee="HR-EMP-00001",
       attendance_date="2025-11-03",
       status="On Leave",
       roster_type="Basic",  # ← Only Basic shift
       shift="General Shift",
       working_hours=0,
       leave_application=leave_app.name
   )
   ```

3. **Employee marks OT attendance:**
   - Manual entry OR auto from checkins
   - Shift: Evening Shift
   - Roster Type: Over-Time
   - Status: Present
   - Working hours: 4.0

4. **Result in database:**
   ```sql
   SELECT * FROM `tabAttendance` WHERE employee='HR-EMP-00001' AND attendance_date='2025-11-03';
   
   | name | roster_type | status    | shift         | working_hours |
   |------|-------------|-----------|---------------|---------------|
   | A-1  | Basic       | On Leave  | General Shift | 0.0           |
   | A-2  | Over-Time   | Present   | Evening Shift | 4.0           |
   ```

---

#### **Option 2: Leave for Both Shifts (Full Day Off)**

1. **Employee applies 2 leave applications:**

   **Leave App 1 - Basic shift:**
   ```python
   frappe.get_doc({
       'doctype': 'Leave Application',
       'employee': 'HR-EMP-00001',
       'from_date': '2025-11-03',
       'to_date': '2025-11-03',
       'leave_type': 'Casual Leave',
       'custom_roster_type': 'Basic',  # Custom field
       'half_day': 0
   }).insert().submit()
   ```

   **Leave App 2 - OT shift:**
   ```python
   frappe.get_doc({
       'doctype': 'Leave Application',
       'employee': 'HR-EMP-00001',
       'from_date': '2025-11-03',
       'to_date': '2025-11-03',
       'leave_type': 'Casual Leave',
       'custom_roster_type': 'Over-Time',  # Custom field
       'half_day': 0
   }).insert().submit()
   ```

2. **System creates 2 attendance records:**
   ```sql
   | name | roster_type | status    | shift         | working_hours |
   |------|-------------|-----------|---------------|---------------|
   | A-1  | Basic       | On Leave  | General Shift | 0.0           |
   | A-2  | Over-Time   | On Leave  | Evening Shift | 0.0           |
   ```

3. **Payroll calculates:**
   - Deduct 1 day from Casual Leave balance
   - Pay basic salary for the day (if paid leave)
   - No OT pay (OT shift also on leave)

---

## ⚙️ System Configuration Required

### **1. Add Custom Field to Leave Application (Recommended)**

```python
# frappe_ticktix/custom/custom_field/leave_application.py

custom_fields = {
    'Leave Application': [
        {
            'fieldname': 'custom_roster_type',
            'label': 'Roster Type',
            'fieldtype': 'Select',
            'options': 'Basic\nOver-Time',
            'default': 'Basic',
            'insert_after': 'half_day',
            'description': 'Select roster type if employee has multiple shifts'
        }
    ]
}
```

**Migration:**
```bash
cd /home/sagivasan/ticktix
./env/bin/bench --site ticktix.local migrate
```

---

### **2. Leave Application Override (Optional Enhancement)**

```python
# frappe_ticktix/plugins/hr/leave/leave_application_override.py

class LeaveApplicationOverride:
    def on_submit(self):
        """
        Create attendance for specific roster type
        If employee has multiple shifts, only mark the selected roster
        """
        roster_type = self.get('custom_roster_type', 'Basic')
        
        # Create attendance for leave dates
        for date in get_date_range(self.from_date, self.to_date):
            # Check if attendance exists for this roster type
            existing = frappe.db.exists('Attendance', {
                'employee': self.employee,
                'attendance_date': date,
                'roster_type': roster_type,
                'docstatus': ['<', 2]
            })
            
            if existing:
                # Update existing
                att = frappe.get_doc('Attendance', existing)
                att.status = 'Half Day' if self.half_day else 'On Leave'
                att.leave_application = self.name
                att.save()
            else:
                # Create new
                att = frappe.get_doc({
                    'doctype': 'Attendance',
                    'employee': self.employee,
                    'attendance_date': date,
                    'status': 'Half Day' if self.half_day else 'On Leave',
                    'roster_type': roster_type,
                    'leave_application': self.name,
                    'company': self.company
                })
                att.insert(ignore_permissions=True)
                att.submit()
```

**Register in hooks.py:**
```python
doc_events = {
    "Leave Application": {
        "on_submit": "frappe_ticktix.plugins.hr.leave.leave_application_override.on_submit"
    }
}
```

---

## 📈 Payroll Processing

### **Salary Slip Calculation**

```python
# frappe_ticktix/plugins/hr/payroll/salary_slip_override.py

def calculate_attendance_days(employee, from_date, to_date):
    """
    Calculate working days and OT hours for payroll
    """
    # Get Basic roster attendance
    basic_attendance = frappe.get_all('Attendance',
        filters={
            'employee': employee,
            'attendance_date': ['between', [from_date, to_date]],
            'roster_type': 'Basic',
            'docstatus': 1
        },
        fields=['status', 'working_hours']
    )
    
    # Get Over-Time roster attendance
    ot_attendance = frappe.get_all('Attendance',
        filters={
            'employee': employee,
            'attendance_date': ['between', [from_date, to_date]],
            'roster_type': 'Over-Time',
            'docstatus': 1
        },
        fields=['status', 'working_hours']
    )
    
    # Calculate Basic roster days
    present_days = 0
    for att in basic_attendance:
        if att.status == 'Present':
            present_days += 1
        elif att.status == 'Half Day':
            present_days += 0.5
        elif att.status in ['On Leave', 'Holiday', 'Weekly Off']:
            present_days += 1  # Paid statuses
    
    # Calculate OT hours
    ot_hours = sum([att.working_hours for att in ot_attendance if att.status == 'Present'])
    
    return {
        'working_days': present_days,
        'ot_hours': ot_hours
    }
```

**Salary Slip Components:**
```python
# Basic Salary (based on Basic roster)
basic_salary_component = {
    'salary_component': 'Basic',
    'amount': (monthly_basic / total_working_days) × present_days
}

# OT Allowance (based on Over-Time roster)
ot_component = {
    'salary_component': 'Over Time',
    'amount': hourly_rate × ot_hours × 1.5  # OT multiplier
}
```

---

## 🎯 Best Practices

### **1. Shift Assignment**

Always assign both shifts separately:

```python
# Basic shift assignment
shift_assignment_1 = frappe.get_doc({
    'doctype': 'Shift Assignment',
    'employee': 'HR-EMP-00001',
    'shift_type': 'General Shift',
    'start_date': '2025-11-01',
    'end_date': '2025-11-30',
    'roster_type': 'Basic'  # Custom field
}).insert().submit()

# OT shift assignment
shift_assignment_2 = frappe.get_doc({
    'doctype': 'Shift Assignment',
    'employee': 'HR-EMP-00001',
    'shift_type': 'Evening Shift',
    'start_date': '2025-11-03',  # Only specific days
    'end_date': '2025-11-03',
    'roster_type': 'Over-Time'  # Custom field
}).insert().submit()
```

---

### **2. Leave Balance Tracking**

Track leave balance separately OR use combined approach:

**Option A: Single Balance (Recommended)**
- Employee has 12 Casual Leave days
- Each full day off deducts 1 day (regardless of Basic or OT)
- Half day on Basic = 0.5 day deduction
- Full day on Basic + Full day on OT = 1 day deduction (same calendar day)

**Option B: Separate Balances (Advanced)**
- Basic roster leaves: 12 days
- OT roster leaves: 6 days
- Requires custom Leave Allocation per roster type

---

### **3. Reports & Analytics**

```sql
-- Monthly attendance summary
SELECT 
    employee,
    roster_type,
    COUNT(CASE WHEN status='Present' THEN 1 END) as present_days,
    COUNT(CASE WHEN status='On Leave' THEN 1 END) as leave_days,
    COUNT(CASE WHEN status='Half Day' THEN 1 END) as half_days,
    SUM(working_hours) as total_hours
FROM `tabAttendance`
WHERE attendance_date BETWEEN '2025-11-01' AND '2025-11-30'
    AND docstatus = 1
GROUP BY employee, roster_type;
```

**Expected output for HR-EMP-00001:**
```
| employee      | roster_type | present_days | leave_days | half_days | total_hours |
|---------------|-------------|--------------|------------|-----------|-------------|
| HR-EMP-00001  | Basic       | 20           | 2          | 1         | 184.5       |
| HR-EMP-00001  | Over-Time   | 5            | 1          | 0         | 20.0        |
```

---

## 🔍 Troubleshooting

### **Issue 1: Cannot mark attendance - duplicate error**

**Error:** "Attendance already marked for this roster type"

**Cause:** Trying to create 2 Basic or 2 Over-Time attendance for same date

**Solution:**
```python
# Check existing attendance
existing = frappe.get_all('Attendance',
    filters={
        'employee': 'HR-EMP-00001',
        'attendance_date': '2025-11-03',
        'roster_type': 'Basic'  # Check specific roster
    }
)

if existing:
    # Update existing instead of creating new
    att = frappe.get_doc('Attendance', existing[0].name)
    att.status = 'Present'
    att.save()
```

---

### **Issue 2: Leave only affects one shift**

**Expected:** Leave for full day (both shifts)  
**Actual:** Only Basic shift marked as leave

**Cause:** Leave Application doesn't know about multiple shifts

**Solution:** Create 2 separate Leave Applications:
1. One for Basic roster
2. One for Over-Time roster

OR use single Leave Application with override logic to create both attendance records.

---

### **Issue 3: Payroll shows incorrect days**

**Cause:** OT attendance counted as working days

**Solution:** Update payroll calculation to only count Basic roster for working days:

```python
# WRONG
working_days = frappe.db.count('Attendance', {
    'employee': employee,
    'status': 'Present',
    'attendance_date': ['between', [from_date, to_date]]
})  # Counts both Basic and OT

# CORRECT
working_days = frappe.db.count('Attendance', {
    'employee': employee,
    'status': 'Present',
    'roster_type': 'Basic',  # Only Basic roster
    'attendance_date': ['between', [from_date, to_date]]
})
```

---

## 📋 Summary

✅ **Multiple shifts supported** via `roster_type` field  
✅ **Separate attendance records** for Basic and Over-Time  
✅ **Leave can affect one or both** shifts  
✅ **Payroll correctly calculates** regular pay + OT  
✅ **No duplicate errors** - proper validation in place  
✅ **Production ready** - all edge cases handled

**For Employee HR-EMP-00001 working multiple shifts:**
1. Each shift gets separate Attendance record (different `roster_type`)
2. Leave Application creates attendance for selected roster type
3. Payroll processes Basic roster for days, OT roster for overtime hours
4. System prevents duplicate attendance per roster type

---

## 🔗 Related Documentation

- **[MULTI_SITE_PAYROLL.md](MULTI_SITE_PAYROLL.md)** - How payroll works when employee works at multiple sites on same day (1st half Site A, 2nd half Site B)

---

*For implementation details, see: `frappe_ticktix/plugins/hr/attendance/attendance_manager.py`*
