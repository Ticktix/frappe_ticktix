# Multi-Site Payroll & Billing

**Scenario:** Employee works at **multiple sites on the same day**  
**Example:** First half at Site A, second half at Site B  
**Last Updated:** 2025-11-01

---

## 🎯 Overview

When an employee works at **multiple sites on the same day**, the system creates **separate attendance records** for each site-shift combination. Payroll and billing are calculated based on **actual hours worked per site**, enabling accurate:

- ✅ **Site-specific billing** to different clients
- ✅ **Project-based cost allocation**
- ✅ **Split payroll** based on site rates (if different)
- ✅ **50/50 split** or any other ratio based on actual hours

---

## 📊 How Multi-Site Attendance Works

### **Scenario: Employee Works 2 Sites Same Day**

**Employee:** HR-EMP-00001 (Ganesh)  
**Date:** November 3, 2025

| Time | Site | Shift | Hours | Client |
|------|------|-------|-------|--------|
| **08:00 - 12:00** | Site A (Mall) | Morning Shift | 4 hours | Client X |
| **13:00 - 18:00** | Site B (Office) | Afternoon Shift | 5 hours | Client Y |

**Total:** 9 hours (4h @ Site A + 5h @ Site B)

---

## 🔑 Key Concept: One Attendance Record Per Site-Shift

### **Current System Design**

The system creates **separate attendance records** for each shift:

```python
# Attendance Record 1 - Site A (Morning)
{
    "employee": "HR-EMP-00001",
    "attendance_date": "2025-11-03",
    "shift": "Morning Shift",
    "site": "Site A (Mall)",
    "project": "Project Alpha",
    "operations_shift": "OPS-SHIFT-001",
    "status": "Present",
    "working_hours": 4.0,
    "roster_type": "Basic",
    "sale_item": "Security Guard - Mall"
}

# Attendance Record 2 - Site B (Afternoon)
{
    "employee": "HR-EMP-00001",
    "attendance_date": "2025-11-03",
    "shift": "Afternoon Shift",
    "site": "Site B (Office)",
    "project": "Project Beta",
    "operations_shift": "OPS-SHIFT-002",
    "status": "Present",
    "working_hours": 5.0,
    "roster_type": "Basic",
    "sale_item": "Security Guard - Office"
}
```

**Key Point:** Each shift has its own attendance record because they have **different shifts**, even though they're on the same date.

---

## ⚙️ Technical Implementation

### **1. Duplicate Check Logic**

```python
# From attendance_manager.py line 402
def validate_duplicate_record(self):
    """
    Check for duplicate attendance
    Key: employee + date + shift + roster_type
    
    Allows multiple attendance records per day if:
    - Different shifts (Morning vs Afternoon)
    - Different roster types (Basic vs Over-Time)
    """
    roster_type = self.get('roster_type', 'Basic')
    
    duplicates = AttendanceManager.get_duplicate_attendance(
        self.employee,
        self.attendance_date,
        self.shift,  # ← Different shifts = different records allowed
        roster_type,
        self.name
    )
```

**What This Means:**
- ✅ **Allowed:** Same employee, same date, **different shifts** (Site A Morning + Site B Afternoon)
- ✅ **Allowed:** Same employee, same date, same shift, **different roster types** (Basic + Over-Time)
- ❌ **Blocked:** Same employee, same date, same shift, same roster type (duplicate)

---

### **2. Auto-Population of Site/Project Fields**

```python
# From attendance_manager.py line 577
def populate_operations_fields(self):
    """
    Auto-populate site, project, operations fields from Shift Assignment
    Each shift assignment has its own site and project
    """
    if not self.shift_assignment:
        return
    
    # Get shift data including site
    shift_data = frappe.db.get_value("Shift Assignment", 
        self.shift_assignment,
        ['shift', 'site', 'shift_type'],
        as_dict=True
    )
    
    # Set site from shift assignment
    if shift_data.get('site'):
        self.site = shift_data.site
        
        # Get project from site
        if frappe.db.exists("Operations Site", shift_data.site):
            project = frappe.db.get_value("Operations Site", 
                shift_data.site, 'project')
            if project:
                self.project = project
    
    # Get operations shift details (role, sale_item, etc.)
    if shift_data.get('shift'):
        self.operations_shift = shift_data.shift
        
        if frappe.db.exists("Operations Shift", shift_data.shift):
            ops_shift = frappe.db.get_value("Operations Shift",
                shift_data.shift,
                ['operations_role', 'post_abbrv', 'sale_item'],
                as_dict=True
            )
            
            if ops_shift:
                self.operations_role = ops_shift.operations_role
                self.post_abbrv = ops_shift.post_abbrv
                self.sale_item = ops_shift.sale_item
```

**Result:** Each attendance record automatically gets:
- Site from Shift Assignment
- Project from Operations Site
- Sale Item from Operations Shift
- Role from Operations Shift

---

## 💰 Payroll Calculation (Split by Site)

### **Scenario: 50/50 Split (4 hours + 5 hours)**

#### **Option A: Same Hourly Rate**

**Employee Base Salary:** $3,000/month (22 working days = $136.36/day)  
**Hourly Rate:** $136.36 ÷ 9 hours = $15.15/hour

| Site | Hours | Calculation | Amount |
|------|-------|-------------|---------|
| Site A | 4.0 | 4 × $15.15 | $60.60 |
| Site B | 5.0 | 5 × $15.15 | $75.75 |
| **Total** | **9.0** | | **$136.36** |

**Payroll Entry:**
```python
# Salary Slip - Basic Salary Component
{
    "employee": "HR-EMP-00001",
    "attendance_date": "2025-11-03",
    "basic_salary": 136.36,  # Full day pay (9 hours worked)
    "component_breakdown": [
        {"site": "Site A", "hours": 4.0, "amount": 60.60},
        {"site": "Site B", "hours": 5.0, "amount": 75.75}
    ]
}
```

**Result:** Employee gets full day pay, but **cost is split** between sites for billing purposes.

---

#### **Option B: Different Rates Per Site**

Some sites pay different rates (e.g., hazardous locations, premium clients).

**Site A (Mall):** $18/hour (premium rate)  
**Site B (Office):** $12/hour (standard rate)

| Site | Hours | Rate | Calculation | Amount |
|------|-------|------|-------------|---------|
| Site A | 4.0 | $18/hr | 4 × $18 | $72.00 |
| Site B | 5.0 | $12/hr | 5 × $12 | $60.00 |
| **Total** | **9.0** | | | **$132.00** |

**Implementation:**
```python
# Custom Salary Slip calculation
def calculate_site_based_salary(employee, from_date, to_date):
    """
    Calculate salary based on different rates per site
    """
    attendance_records = frappe.get_all('Attendance',
        filters={
            'employee': employee,
            'attendance_date': ['between', [from_date, to_date]],
            'status': 'Present',
            'docstatus': 1
        },
        fields=['site', 'working_hours', 'sale_item', 'project']
    )
    
    total_earnings = 0
    site_breakdown = {}
    
    for att in attendance_records:
        # Get hourly rate from Operations Site or Sale Item
        rate = get_hourly_rate_for_site(att.site, att.sale_item)
        
        # Calculate earnings
        earnings = att.working_hours * rate
        total_earnings += earnings
        
        # Track per site
        if att.site not in site_breakdown:
            site_breakdown[att.site] = {'hours': 0, 'amount': 0}
        
        site_breakdown[att.site]['hours'] += att.working_hours
        site_breakdown[att.site]['amount'] += earnings
    
    return {
        'total_earnings': total_earnings,
        'site_breakdown': site_breakdown
    }
```

---

## 📑 Client Billing (Split by Site)

### **Scenario: Bill Different Clients**

**Site A (Mall)** → Client X pays $25/hour  
**Site B (Office)** → Client Y pays $20/hour

| Site | Client | Hours | Rate | Amount |
|------|--------|-------|------|--------|
| Site A | Client X | 4.0 | $25/hr | $100.00 |
| Site B | Client Y | 5.0 | $20/hr | $100.00 |
| **Total Billing** | | **9.0** | | **$200.00** |

**Employee Cost:** $136.36 (from payroll)  
**Total Billing:** $200.00  
**Gross Margin:** $63.64 (31.8%)

**Sales Invoice Generation:**
```python
# Invoice to Client X (Site A)
{
    "customer": "Client X",
    "project": "Project Alpha",
    "items": [
        {
            "item_code": "Security Guard - Mall",
            "qty": 4.0,  # hours
            "rate": 25.00,
            "amount": 100.00,
            "reference": "Attendance for HR-EMP-00001 on 2025-11-03"
        }
    ],
    "total": 100.00
}

# Invoice to Client Y (Site B)
{
    "customer": "Client Y",
    "project": "Project Beta",
    "items": [
        {
            "item_code": "Security Guard - Office",
            "qty": 5.0,  # hours
            "rate": 20.00,
            "amount": 100.00,
            "reference": "Attendance for HR-EMP-00001 on 2025-11-03"
        }
    ],
    "total": 100.00
}
```

---

## 📊 Actual Split Calculation (50/50 Example)

### **Question: Does it split 50/50?**

**Answer:** It splits based on **actual hours worked per site**, not a fixed 50/50 ratio.

#### **Example 1: Exactly 50/50 (4.5h + 4.5h)**

| Site | Hours | % of Total | Amount (of $136.36) |
|------|-------|------------|---------------------|
| Site A | 4.5 | 50% | $68.18 |
| Site B | 4.5 | 50% | $68.18 |
| **Total** | **9.0** | **100%** | **$136.36** |

**Yes, this is exactly 50/50!**

---

#### **Example 2: Not 50/50 (4h + 5h)**

| Site | Hours | % of Total | Amount (of $136.36) |
|------|-------|------------|---------------------|
| Site A | 4.0 | 44.4% | $60.60 |
| Site B | 5.0 | 55.6% | $75.76 |
| **Total** | **9.0** | **100%** | **$136.36** |

**No, this is 44.4% / 55.6% split based on actual hours!**

---

#### **Example 3: Extreme Split (2h + 7h)**

| Site | Hours | % of Total | Amount (of $136.36) |
|------|-------|------------|---------------------|
| Site A | 2.0 | 22.2% | $30.30 |
| Site B | 7.0 | 77.8% | $106.06 |
| **Total** | **9.0** | **100%** | **$136.36** |

**No, this is 22.2% / 77.8% split!**

---

## 🔄 Shift Assignment Setup

### **How to Assign Employee to Multiple Sites**

**Step 1: Create Shift Assignment for Site A (Morning)**

```python
shift_assignment_1 = frappe.get_doc({
    'doctype': 'Shift Assignment',
    'employee': 'HR-EMP-00001',
    'shift_type': 'Morning Shift',  # 08:00 - 12:00
    'site': 'Site A (Mall)',
    'start_date': '2025-11-01',
    'end_date': '2025-11-30',
    'roster_type': 'Basic'
}).insert().submit()
```

**Step 2: Create Shift Assignment for Site B (Afternoon)**

```python
shift_assignment_2 = frappe.get_doc({
    'doctype': 'Shift Assignment',
    'employee': 'HR-EMP-00001',
    'shift_type': 'Afternoon Shift',  # 13:00 - 18:00
    'site': 'Site B (Office)',
    'start_date': '2025-11-01',
    'end_date': '2025-11-30',
    'roster_type': 'Basic'
}).insert().submit()
```

**Result:** System auto-creates 2 attendance records per day:
- 1 for Morning Shift @ Site A
- 1 for Afternoon Shift @ Site B

---

## 📈 Reporting & Analytics

### **1. Site-wise Cost Report**

```sql
-- Total hours and cost per site for November
SELECT 
    site,
    COUNT(DISTINCT employee) as total_employees,
    SUM(working_hours) as total_hours,
    SUM(working_hours) * 15.15 as total_cost  -- Assuming $15.15/hour
FROM `tabAttendance`
WHERE attendance_date BETWEEN '2025-11-01' AND '2025-11-30'
    AND status = 'Present'
    AND docstatus = 1
GROUP BY site
ORDER BY total_cost DESC;
```

**Output:**
```
| site           | total_employees | total_hours | total_cost |
|----------------|-----------------|-------------|------------|
| Site A (Mall)  | 120             | 9,600       | $145,440   |
| Site B (Office)| 80              | 6,400       | $96,960    |
| Site C (Bank)  | 50              | 4,000       | $60,600    |
```

---

### **2. Project-wise Billing Report**

```sql
-- Total hours and billing per project
SELECT 
    project,
    site,
    sale_item,
    SUM(working_hours) as total_hours,
    COUNT(DISTINCT employee) as employees,
    SUM(working_hours) * 25.00 as total_billing  -- Assuming $25/hour billing
FROM `tabAttendance`
WHERE attendance_date BETWEEN '2025-11-01' AND '2025-11-30'
    AND status = 'Present'
    AND docstatus = 1
GROUP BY project, site, sale_item
ORDER BY project, site;
```

**Output:**
```
| project       | site          | sale_item              | total_hours | employees | total_billing |
|---------------|---------------|------------------------|-------------|-----------|---------------|
| Project Alpha | Site A (Mall) | Security Guard - Mall  | 4,800       | 60        | $120,000      |
| Project Beta  | Site B (Office)| Security Guard - Office| 6,400       | 80        | $160,000      |
```

---

### **3. Employee Multi-Site Analysis**

```sql
-- Employees working at multiple sites
SELECT 
    employee,
    employee_name,
    COUNT(DISTINCT site) as sites_worked,
    GROUP_CONCAT(DISTINCT site) as site_list,
    SUM(working_hours) as total_hours
FROM `tabAttendance`
WHERE attendance_date BETWEEN '2025-11-01' AND '2025-11-30'
    AND status = 'Present'
    AND docstatus = 1
GROUP BY employee
HAVING sites_worked > 1
ORDER BY sites_worked DESC, total_hours DESC;
```

**Output:**
```
| employee      | employee_name | sites_worked | site_list                      | total_hours |
|---------------|---------------|--------------|--------------------------------|-------------|
| HR-EMP-00001  | Ganesh        | 3            | Site A,Site B,Site C          | 220         |
| HR-EMP-00025  | Rajesh        | 2            | Site A,Site B                 | 180         |
| HR-EMP-00042  | Priya         | 2            | Site B,Site C                 | 176         |
```

---

## 💡 Use Cases & Examples

### **Use Case 1: Security Guard Covering Multiple Locations**

**Scenario:**
- Employee covers sick colleague at different site for afternoon
- Morning: Regular site (4 hours)
- Afternoon: Backup site (5 hours)

**Result:**
- 2 attendance records created
- Payroll: Full day pay (9 hours)
- Billing: Split between 2 clients based on actual hours

---

### **Use Case 2: Supervisor Visiting Multiple Sites**

**Scenario:**
- Supervisor inspects 3 sites in one day
- Site A: 3 hours (inspection)
- Site B: 2 hours (meeting)
- Site C: 4 hours (training)

**Result:**
- 3 attendance records created (different shifts or manual entries)
- Payroll: Full day pay (9 hours)
- Billing: 3 separate invoices to 3 clients

---

### **Use Case 3: Project-Based Work**

**Scenario:**
- Employee works on 2 different projects
- Project Alpha @ Site A: 5 hours
- Project Beta @ Site B: 4 hours

**Result:**
- 2 attendance records (different projects)
- Cost allocation: 55.6% to Project Alpha, 44.4% to Project Beta
- Accurate project profitability tracking

---

## ⚠️ Important Considerations

### **1. Overlapping Shift Validation**

The system **validates overlapping shifts** on the same day:

```python
# From attendance_manager.py
def validate_overlapping_shift(self):
    """
    Prevents marking attendance for overlapping shifts
    """
    overlapping = AttendanceManager.get_overlapping_shift_attendance(...)
    
    if overlapping:
        frappe.throw(_("Attendance for overlapping shift already exists"))
```

**Example:**
- ✅ **Allowed:** Morning Shift (08:00-12:00) + Afternoon Shift (13:00-18:00) - No overlap
- ❌ **Blocked:** Morning Shift (08:00-14:00) + Day Shift (09:00-17:00) - Overlap!

---

### **2. Different Roster Types**

You can also split using **roster_type** instead of different shifts:

```python
# Attendance 1 - Regular shift at Site A
{
    "shift": "General Shift",
    "site": "Site A",
    "roster_type": "Basic",
    "working_hours": 9.0
}

# Attendance 2 - Overtime at Site B (same day)
{
    "shift": "General Shift",  # Same shift type
    "site": "Site B",
    "roster_type": "Over-Time",  # Different roster type
    "working_hours": 4.0
}
```

---

### **3. Leave Application Impact**

If employee applies leave but only for one site:

**Scenario:** Leave for morning shift (Site A), still works afternoon (Site B)

```python
# Leave Application - Only for Morning Shift
{
    "employee": "HR-EMP-00001",
    "from_date": "2025-11-03",
    "to_date": "2025-11-03",
    "leave_type": "Casual Leave",
    "custom_shift": "Morning Shift"  # Specific shift
}

# Result:
# Attendance 1 - Morning @ Site A: "On Leave"
# Attendance 2 - Afternoon @ Site B: "Present" (5 hours)

# Payroll:
# Leave: 0.5 day deducted (4 hours of leave)
# Worked: 5 hours @ Site B paid
```

---

## 🔧 System Configuration

### **1. Enable Multi-Site Tracking**

Already enabled via custom fields:
- ✅ `site` field in Attendance
- ✅ `project` field in Attendance
- ✅ `operations_shift` field in Attendance
- ✅ `sale_item` field for billing

---

### **2. Configure Operations Site**

```python
# Create Operations Site with billing details
{
    'doctype': 'Operations Site',
    'site_name': 'Site A (Mall)',
    'project': 'Project Alpha',
    'customer': 'Client X',
    'hourly_rate': 25.00,  # Client billing rate
    'employee_cost_rate': 15.15  # Employee cost
}
```

---

### **3. Configure Operations Shift**

```python
# Create Operations Shift with sale item
{
    'doctype': 'Operations Shift',
    'shift_name': 'Mall Security - Morning',
    'shift_type': 'Morning Shift',
    'site': 'Site A (Mall)',
    'operations_role': 'Security Guard',
    'sale_item': 'Security Guard - Mall',
    'post_abbrv': 'SG-ML'
}
```

---

## 📋 Summary

### **Key Takeaways:**

1. ✅ **Multi-site support:** Employee can work at multiple sites on same day
2. ✅ **Automatic split:** System creates separate attendance per site-shift
3. ✅ **Flexible ratio:** Split based on actual hours worked (not fixed 50/50)
4. ✅ **Site-specific billing:** Each site billed separately to its client
5. ✅ **Project cost allocation:** Accurate tracking per project
6. ✅ **No manual calculation:** System auto-populates site, project, sale_item

### **Answer to Your Question:**

> **"Will it follow payroll based on site for 50/50?"**

**Answer:** 
- **YES**, if employee works exactly **4.5 hours at each site** (50/50 split)
- **NO**, if hours are different (e.g., 4h + 5h = 44.4% / 55.6% split)
- Split is **automatic** based on `working_hours` field in each attendance record
- Each site is **billed separately** to its client
- Employee **payroll** is sum of all attendance records for the day

**Formula:**
```
Site A % = (Site A hours / Total hours) × 100
Site A Cost = Total Day Cost × Site A %

Example: 4 hours / 9 total = 44.4%
         $136.36 × 44.4% = $60.60
```

---

*For implementation details, see:*
- *`frappe_ticktix/plugins/hr/attendance/attendance_manager.py`*
- *`frappe_ticktix/custom/custom_field/attendance.py`*
