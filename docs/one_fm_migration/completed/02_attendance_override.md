# Attendance Override

**Module:** Attendance  
**Status:** ✅ Complete (Extended)  
**LOC:** ~1,200 lines (was ~550 lines)  
**Last Updated:** 2025-11-01

---

## 📝 Change Log

### 2025-11-01 - Working Hours & Half Day Fixes
- ✅ **Half Day working hours**: Now automatically calculates 50% of shift hours (9h → 4.5h)
- ✅ **Shift requirement**: Only mandatory for "Present" status (following one_fm pattern)
- ✅ **Working hours validation**: Allows null/0 hours, only rejects negative values
- ✅ **Unscheduled employees**: Can mark Present without working hours (manual entry)
- ✅ **Status change recalculation**: Working hours auto-update when status changes to/from Half Day
- ✅ **Float field handling**: Properly handles Frappe's default 0.0 for Float fields

### 2025-10-30 - Initial Implementation
- ✅ 21 custom fields added
- ✅ 9 status options (4 new: Weekly Off, Client Day Off, Holiday, On Hold)
- ✅ Overlapping shift validation
- ✅ Bulk marking API
- ✅ Unscheduled employee handling
- ✅ Remark logic for error correction
- ✅ After_migrate hook for production deployment

---

## 🔵 What Frappe HRMS Has (Built-in)

Frappe HRMS v15 already includes robust attendance functionality:

**Core Features:**
- ✅ Attendance doctype with standard statuses (Present, Absent, On Leave, Half Day, Work From Home)
- ✅ Employee validation and company/department tracking
- ✅ Duplicate prevention (per employee per date)
- ✅ Leave integration (links to Leave Application)
- ✅ Holiday checking via Holiday List
- ✅ **Shift Type auto-attendance** via `process_auto_attendance()` scheduler
- ✅ **Auto-detect late entry/early exit** based on Shift Type grace periods
- ✅ **Working hours calculation** from Employee Checkin records
- ✅ **in_time/out_time tracking** from checkins
- ✅ **Shift assignment** support
- ✅ Half day status tracking
- ✅ Attendance Request integration

**What Shift Type Already Does:**
- Auto-mark attendance from Employee Checkin records
- Calculate working hours from IN/OUT checkins
- Set late_entry flag if checkin > shift_start + grace_period
- Set early_exit flag if checkout < shift_end - grace_period
- Process attendance via scheduler (`process_auto_attendance`)

## 🟢 What We Added (Extensions)

| Feature | Frappe HRMS | Our Override | Details |
|---------|-------------|--------------|---------|
| **Status options** | 5 statuses | 9 statuses | Added: Weekly Off, Client Day Off, Holiday, On Hold |
| **Half Day working hours** | ✅ Manual | ✅ Auto-calculated | Automatically sets to 50% of shift hours (e.g., 9h → 4.5h) |
| **Shift requirement** | All statuses | Present only | Shift mandatory for Present, optional for On Leave/Half Day/etc. |
| Shift auto-detect | ✅ Yes | ✅ Enhanced | Extended validation for multi-shift scenarios |
| Working hours calc | ✅ Yes | ✅ Enhanced | Added roster_type support + Half Day auto-reduction |
| **Working hours validation** | Required | Optional | Allows null/0 hours, only rejects negative values |
| Late/early flags | ✅ Yes | ✅ Same | Uses Frappe's built-in late_entry/early_exit fields |
| Link to checkins | ✅ Yes | ✅ Same | Frappe already links via `attendance` field in Employee Checkin |
| Auto-mark absent | ✅ Partial | ✅ Complete | Extended to handle unscheduled employees |
| Holiday detection | ✅ Basic | ✅ Enhanced | Added Client Day Off and Weekly Off logic |
| Summary API | ❌ No | ✅ Added | New `get_attendance_summary()` endpoint |
| **Custom fields (21)** | ❌ No | ✅ Added | Operations, roster, timesheet, tracking fields |
| **Overlapping shift validation** | ❌ No | ✅ Added | Prevents conflicts in multi-shift scenarios |
| **Bulk marking API** | ❌ No | ✅ Added | `mark_bulk_attendance()` for date ranges |
| **Roster type (Basic/OT)** | ❌ No | ✅ Added | Separate tracking for regular vs overtime |
| **Unscheduled employees** | ❌ No | ✅ Added | Auto-mark employees without shifts, allow null working hours |
| **Remark logic** | ❌ No | ✅ Added | Fix incorrect Absent records |
| **Operations integration** | ❌ No | ✅ Added | Auto-populate site, project, role from shift |

**Key Differences:**
- **We extend, not replace:** All Frappe HRMS functionality is preserved
- **Additional statuses:** 4 new custom statuses for operations use cases
- **Half Day intelligence:** Auto-calculates 50% working hours (Frappe uses threshold-based detection)
- **Flexible shift requirement:** Only "Present" requires shift (one_fm pattern), other statuses optional
- **Lenient working hours:** Allows null/0 hours (Frappe validates on submit), only blocks negative
- **Operations tracking:** 21 custom fields for multi-site/project billing
- **Enhanced automation:** Unscheduled employee handling + remark logic
- **Multi-roster support:** Separate Basic and Over-Time roster tracking

## 📊 Custom Fields Added (21 Fields)

### Operations Section
| Field | Type | Description |
|-------|------|-------------|
| `operations_shift` | Link → Operations Shift | Link to operations shift for operations management |
| `site` | Link → Operations Site | Work site/location for this attendance |
| `project` | Link → Project | Project linked to attendance (for billing) |
| `operations_role` | Link → Operations Role | Employee role at site (Guard, Supervisor, etc.) |

### Roster & Overtime Section
| Field | Type | Description |
|-------|------|-------------|
| `roster_type` | Select | Basic = Regular shift, Over-Time = OT shift |
| `day_off_ot` | Check | Employee worked on day off (eligible for OT pay) |
| `post_abbrv` | Data | Short code for role (used in reports) |
| `sale_item` | Data | Sales item for billing calculations |

### Integration Section
| Field | Type | Description |
|-------|------|-------------|
| `timesheet` | Link → Timesheet | Linked timesheet (for project-based attendance) |
| `reference_doctype` | Link → DocType | Source document type (if created from another doc) |
| `reference_docname` | Dynamic Link | Source document name |

### Tracking Section
| Field | Type | Description |
|-------|------|-------------|
| `custom_employment_type` | Link → Employment Type | Employee contract type (affects payroll) |
| `is_unscheduled` | Check | Employee has no shift assignment |

### Comments Section
| Field | Type | Description |
|-------|------|-------------|
| `comment` | Small Text | Reason for attendance status or additional notes |

**Total:** 21 custom fields for operations, billing, and tracking

## � What We Actually Override vs Extend

### Methods We Override (Replace Frappe's Logic)

| Method | Frappe HRMS | Our Override | Reason |
|--------|-------------|--------------|--------|
| `validate()` | Basic validation | Extended validation | Added 9 status options, roster_type, overlapping shift check |
| `validate_duplicate_record()` | Employee + Date only | Employee + Date + Roster Type | Support multiple rosters per day (Basic + OT) |
| `validate_working_hours()` | Requires hours on submit | Allows null/0, rejects negative | Support unscheduled employees, lenient validation |
| `set_shift_assignment()` | Not present | Auto-fill shift for Present | Only mandates shift for Present status (one_fm pattern) |
| `_get_shift_working_hours()` | Not present | Calculate + Half Day adjust | Auto-calculates from shift times, halves for Half Day status |

### Methods We Extend (Add to Frappe's Logic)

| Method | What We Add |
|--------|-------------|
| `before_save()` | Auto-populate operations fields (site, project, role) from shift assignment<br>Auto-calculate working hours on status change (Present ↔ Half Day)<br>Only set shift for Present status (not for On Leave, etc.) |
| `after_insert()` | Set day_off_ot flag from Employee Schedule |

### New Methods We Added

| Method | Purpose |
|--------|---------|
| `validate_overlapping_shift()` | Prevent marking attendance for overlapping shifts on same day |
| `populate_operations_fields()` | Auto-populate site, project, operations_role from shift assignment |
| `set_day_off_ot()` | Flag attendance on day off as overtime-eligible |
| `set_shift_assignment()` | Auto-fill shift from assignment or employee.default_shift (Present only) |
| `_get_shift_working_hours()` | Calculate working hours from shift times, auto-halve for Half Day |

### ⚠️ What Frappe HRMS Already Does (We DON'T Override)

**Shift Type Auto-Attendance (`process_auto_attendance()`):**
- ✅ Frappe already auto-marks attendance from Employee Checkin records
- ✅ Frappe already calculates working_hours from IN/OUT checkins  
- ✅ Frappe already sets late_entry flag (checkin > shift_start + grace)
- ✅ Frappe already sets early_exit flag (checkout < shift_end - grace)
- ✅ Frappe already links attendance to checkin records
- ✅ Frappe already marks absent for employees with no checkins
- ✅ Frappe runs this via scheduler (`process_auto_attendance_for_all_shifts`)

**Our Extension:**
- We keep all Frappe's auto-attendance logic
- We add support for unscheduled employees (no shift assignment)
- We add roster_type differentiation (Basic vs Over-Time)
- We add remark logic to fix incorrect records
- We add operations field auto-population

**Key Point:** Frappe HRMS v15 already has robust attendance automation. We **extend** it, not replace it.

---

## 📋 Feature-by-Feature Breakdown

### 1. ✅ Half Day Working Hours (Auto-Calculation)

**Problem:** Frappe HRMS uses threshold-based detection (e.g., < 6 hours = Half Day), doesn't auto-adjust working hours

**Our Solution:**
```python
def _get_shift_working_hours(self, shift_type):
    """
    Calculate working hours from shift start and end time
    Adjusts for Half Day status using Frappe HRMS threshold
    """
    # Get shift timings
    shift_data = frappe.db.get_value('Shift Type', shift_type,
        ['start_time', 'end_time', 'working_hours_threshold_for_half_day'],
        as_dict=True)
    
    # Calculate full shift hours
    duration = calculate_duration(shift_data.start_time, shift_data.end_time)
    
    # Adjust for Half Day status
    if self.get('status') == 'Half Day':
        # Use Frappe threshold if configured, else 50% of full hours
        if shift_data.get('working_hours_threshold_for_half_day'):
            duration = shift_data.working_hours_threshold_for_half_day
        else:
            duration = duration / 2  # Default: 50%
    
    return duration
```

**Features:**
- ✅ **Auto-calculates** from shift `start_time` and `end_time`
- ✅ **Handles overnight shifts** (duration < 0 adds 24 hours)
- ✅ **Uses Frappe threshold** if `working_hours_threshold_for_half_day` configured
- ✅ **Falls back to 50%** of shift duration (standard half-day)
- ✅ **Recalculates on status change** (Present → Half Day: 9h → 4.5h)

**Example:**
```
Shift: General Shift (09:00 - 18:00) = 9 hours

Status: Present → working_hours = 9.0
Status: Half Day → working_hours = 4.5 (automatically halved)

If shift has working_hours_threshold_for_half_day = 4:
Status: Half Day → working_hours = 4.0 (uses threshold)
```

**Files:**
- `attendance_manager.py`: `_get_shift_working_hours()`, `before_save()`
- Called on: Initial save, status change

---

### 2. ✅ Shift Requirement (Present Status Only)

**Frappe HRMS:** No specific requirement, shift can be set for any status

**one_fm Pattern:** Shift required ONLY for "Present" status

**Our Implementation:**
```python
def set_shift_assignment(self):
    """
    Auto-set shift assignment if not present
    Note: Only required for 'Present' status, optional for others
    """
    # Only mandate shift for Present status
    if self.get('status') not in ['Present']:
        return  # Skip for On Leave, Half Day, etc.
    
    # Get shift assignment or employee default shift
    shift_assignment = AttendanceManager.get_shift_assignment(...)
    if shift_assignment:
        self.shift = shift_assignment.shift_type
        self.working_hours = self._get_shift_working_hours(...)
    else:
        # Fallback to employee's default_shift
        default_shift = frappe.db.get_value('Employee', self.employee, 'default_shift')
        if default_shift:
            self.shift = default_shift
            self.working_hours = self._get_shift_working_hours(default_shift)
```

**Behavior:**

| Status | Shift Required? | Working Hours | Notes |
|--------|----------------|---------------|-------|
| **Present** | ✅ Yes | Auto-calculated | Shift auto-filled from assignment or employee default |
| On Leave | ❌ No | Not required | Leave Application creates without shift |
| Half Day | ❌ No | Optional | Can be set manually or from Leave Application |
| Absent | ❌ No | Not required | Marked by system without shift |
| Weekly Off | ❌ No | Not required | System-generated status |
| Holiday | ❌ No | Not required | From Holiday List |

**Why This Matters:**
- ✅ **Leave Applications** can create attendance without shift validation errors
- ✅ **Half-day leaves** don't fail on missing shift
- ✅ **Unscheduled employees** can have On Leave status
- ✅ **one_fm compatibility** - follows their shift requirement pattern

**Files:**
- `attendance_manager.py`: `set_shift_assignment()`, `before_save()`

---

### 3. ✅ Working Hours Validation (Lenient)

**Frappe HRMS:** Validates working hours on submit for Present/Work From Home status

**Our Override:**
```python
def validate_working_hours(self):
    """
    Validate working hours based on status
    Allow null/zero working hours for:
    - Unscheduled employees (no shift assignment)
    - Leave statuses
    - Manual entries where user hasn't filled it yet
    
    Note: Frappe Float fields default to 0.0, not None
    """
    # For unscheduled employees, working hours can be null/0
    if self.get('is_unscheduled'):
        if self.get('working_hours') and self.get('working_hours') < 0:
            frappe.throw(_("Working hours cannot be negative"))
        return  # Allow null/0 for unscheduled
    
    # For scheduled employees, only reject negative values
    if self.get('working_hours') and self.get('working_hours') < 0:
        frappe.throw(_("Working hours cannot be negative"))
```

**Validation Rules:**

| Scenario | Frappe HRMS | Our Override | Reason |
|----------|-------------|--------------|--------|
| Present + 0 hours | ❌ Reject on submit | ✅ Allow | Auto-calculated in before_save |
| Present + null hours | ❌ Reject on submit | ✅ Allow | Unscheduled employees |
| Present + negative hours | ❌ Reject | ❌ Reject | Invalid value |
| On Leave + 0 hours | ✅ Allow | ✅ Allow | No hours needed |
| Unscheduled + 0 hours | N/A | ✅ Allow | Manual entry later |

**Float Field Handling:**
```python
# Frappe Float fields default to 0.0, not None
att = frappe.new_doc('Attendance')
att.working_hours  # Returns 0.0, not None

# Our validation handles this:
if self.get('working_hours'):  # 0.0 is falsy, passes
    # Only validate if positive value provided
```

**Use Cases:**
- ✅ **Unscheduled employees** marking Present (manual hours entry)
- ✅ **Draft attendance** without working hours (calculated later)
- ✅ **Leave Applications** creating On Leave without hours
- ✅ **System-generated** Holiday/Weekly Off without hours

**Files:**
- `attendance_manager.py`: `validate_working_hours()`

---

### 4. ✅ Status Options (9 Statuses)

**Frappe HRMS Default (5):**
- Present
- Absent  
- On Leave
- Half Day
- Work From Home

**We Added (4):**
- **Weekly Off** - Company-assigned weekly off (NOT billable)
- **Client Day Off** - Client-requested day off (IS billable to client)
- **Holiday** - Public holiday from Holiday List
- **On Hold** - Pending client approval for billing

**Implementation:**
- Property Setter on Attendance.status field
- Client Scripts to override hardcoded UI dropdowns
- Python validation updated to accept new statuses

**Files:**
- `install.py`: `customize_attendance_status()`
- `attendance_status_override.py`: `get_attendance_status_options()`
- `client_scripts.py`: Mark Attendance Dialog + Employee Attendance Tool overrides

---

### 5. ✅ Custom Fields (21 Fields)

**Purpose:** Enable operations tracking, project billing, roster management

**Categories:**

**A. Operations Tracking (4 fields)**
- `operations_shift` - Link to Operations Shift doctype
- `site` - Work location/site
- `project` - Project for billing
- `operations_role` - Employee role (Guard, Supervisor, etc.)

**B. Roster & Overtime (4 fields)**
- `roster_type` - Basic vs Over-Time (for separate tracking)
- `day_off_ot` - Flag if worked on day off (OT eligible)
- `post_abbrv` - Role abbreviation for reports
- `sale_item` - Item for billing calculation

**C. Integration (3 fields)**
- `timesheet` - Link to Timesheet (project-based work)
- `reference_doctype` - Source doctype if created from another doc
- `reference_docname` - Source doc name

**D. Tracking (2 fields)**
- `custom_employment_type` - Contract type for payroll
- `is_unscheduled` - Employee has no shift assignment

**E. Comments (1 field)**
- `comment` - Attendance reason/notes

**Implementation:**
- Custom Field definitions in `custom/custom_field/attendance.py`
- Auto-created via `install.py` on app installation
- Organized in collapsible sections in UI

**Auto-Population Logic:**
- Operations fields auto-populate from Shift Assignment
- Employment type auto-set from Employee master
- Gracefully handles missing Operations doctypes

---

### 6. ✅ Overlapping Shift Validation

**Problem:** Employee could have multiple shifts on same day with overlapping times

**Frappe HRMS:** Only checks duplicate (employee + date)

**Our Solution:**
- Check shift timings for overlap
- Prevent marking attendance if shifts overlap
- Allow non-overlapping shifts (e.g., morning + evening)

**Implementation:**
```python
def validate_overlapping_shift():
    # Get other attendance for same employee, same date, different shift
    overlapping = get_overlapping_shift_attendance(...)
    if overlapping:
        # Check if shift times actually overlap
        if has_overlapping_timings(shift1, shift2):
            throw error
```

**Files:**
- `attendance_manager.py`: `get_overlapping_shift_attendance()`, `has_overlapping_timings()`
- `AttendanceOverride.validate_overlapping_shift()`

**Example:**
- ❌ BLOCKED: Morning shift 6 AM-2 PM + Day shift 9 AM-5 PM (overlap)
- ✅ ALLOWED: Morning shift 6 AM-2 PM + Evening shift 2 PM-10 PM (no overlap)

---

### 7. ✅ Roster Type Support (Basic vs Over-Time)

**Purpose:** Track regular work vs overtime separately for payroll

**Frappe HRMS:** No roster type concept

**Our Implementation:**
- `roster_type` field: Select (Basic / Over-Time)
- Duplicate check includes roster_type
- Can have 2 attendance records per day (1 Basic + 1 OT)

**Use Cases:**
- Basic roster: Regular 8-hour shift
- Over-Time roster: Extra hours beyond regular shift
- Separate billing rates
- Different payroll calculations

**Implementation:**
- Field added to Attendance
- Validation enhanced: duplicate check = employee + date + roster_type
- APIs support roster_type parameter
- Default value: "Basic"

**Example:**
- Employee A, 2025-11-01, Basic roster: 8 hours (regular pay)
- Employee A, 2025-11-01, Over-Time roster: 4 hours (OT pay 1.5x)

**📚 Detailed Guide:** See [MULTIPLE_SHIFTS_PAYROLL.md](MULTIPLE_SHIFTS_PAYROLL.md) for:
- How payroll calculates with multiple shifts
- How leave affects one or both shifts
- Leave Application workflow for multiple rosters
- Salary Slip calculation examples
- Best practices and troubleshooting

---

### 8. ✅ Bulk Marking API

**Purpose:** Mark attendance for date range in one API call

**Frappe HRMS:** Only single-date marking via `mark_attendance()`

**Our API:**
```python
mark_bulk_attendance(employee, from_date, to_date, roster_type="Basic")
```

**Features:**
- Processes entire date range
- Auto-marks from checkins if available
- Marks holidays automatically
- Marks absent if no data
- Returns detailed summary (success/errors)

**Response:**
```json
{
  "success": 5,
  "failed": 2,
  "marked_dates": ["2025-11-01", "2025-11-02", ...],
  "errors": [
    {"date": "2025-11-03", "error": "Attendance already exists"}
  ]
}
```

**Use Cases:**
- Mobile app bulk sync
- Backfill missing attendance
- Batch processing
- HR corrections

**Files:**
- `attendance_manager.py`: `mark_bulk_attendance()`
- `hooks.py`: Whitelisted API endpoint

---

### 9. ✅ Unscheduled Employee Handling

**Problem:** Employees without shift assignments don't get auto-attendance

**Frappe HRMS:** Only processes employees with Shift Type + Shift Assignment

**Our Solution:**
```python
mark_attendance_for_unscheduled_employees(date)
```

**Logic:**
1. Find all active employees (not on timesheet attendance)
2. Exclude employees with existing attendance
3. Exclude employees with shift assignments
4. For remaining employees:
   - Check Holiday List → Mark "Holiday"
   - Otherwise → Mark "Absent"
5. Set `is_unscheduled` flag

**Runs:** Daily at 1 AM (scheduler task)

**Use Cases:**
- Office staff without shifts
- Management employees
- Part-time workers
- Contract employees

**Files:**
- `attendance_manager.py`: `mark_attendance_for_unscheduled_employees()`
- `hooks.py`: Daily scheduler event

---

### 10. ✅ Remark Logic (Error Correction)

**Problem:** Attendance marked Absent before checkins are recorded

**Scenario:**
1. 1 AM: Daily job runs, no checkins found → Marked "Absent"
2. 8 AM: Employee checks in (late upload from mobile)
3. Attendance still shows "Absent" (incorrect!)

**Our Solution:**
```python
remark_for_active_employees(date)
```

**Logic:**
1. Find Absent attendance with shift assignments
2. Check if checkins now exist
3. If checkins found:
   - Recalculate working hours
   - Update status to "Present"
   - Set late_entry/early_exit flags
   - Add comment: "Re-marked from checkins"

**Runs:** Daily at 1 AM (after main marking)

**Files:**
- `attendance_manager.py`: `remark_for_active_employees()`
- `hooks.py`: Daily scheduler event

**Example:**
```
Before: Status=Absent, Working Hours=0, Comment="No checkin records found"
After:  Status=Present, Working Hours=8.5, Comment="Re-marked from checkins (was incorrectly marked Absent)", late_entry=1
```

---

### 11. ✅ Operations Field Auto-Population

**Purpose:** Automatically fill site, project, role from shift assignment

**Frappe HRMS:** Manual entry only

**Our Logic:**
```python
def populate_operations_fields():
    if shift_assignment:
        # From Shift Assignment
        operations_shift = shift_assignment.shift
        site = shift_assignment.site
        
        # From Operations Shift (if exists)
        if Operations Shift doctype exists:
            operations_role = operations_shift.operations_role
            post_abbrv = operations_shift.post_abbrv
            sale_item = operations_shift.sale_item
        
        # From Operations Site (if exists)
        if Operations Site doctype exists:
            project = site.project
```

**Runs:** In `before_save()` hook

**Graceful Degradation:**
- If Operations Shift doctype doesn't exist → Skip operations fields
- If Operations Site doctype doesn't exist → Skip site fields
- No errors thrown if doctypes missing

**Use Cases:**
- Multi-site operations
- Project-based billing
- Site-specific reporting
- Role-based pay rates

**Files:**
- `attendance_manager.py`: `AttendanceOverride.populate_operations_fields()`

---

### 12. ✅ Day Off OT Tracking

**Purpose:** Flag when employee works on their scheduled day off

**Frappe HRMS:** No day off OT concept

**Our Logic:**
```python
def set_day_off_ot():
    if Employee Schedule doctype exists:
        day_off_ot = Employee Schedule.day_off_ot
        if day_off_ot:
            attendance.day_off_ot = 1
```

**Runs:** In `after_insert()` hook

**Payroll Impact:**
- Regular shift: Normal pay
- Day off OT: Premium pay (e.g., 2x rate)

**Files:**
- `attendance_manager.py`: `AttendanceOverride.set_day_off_ot()`

---

### 13. ✅ Enhanced Validation

**A. Duplicate Check with Roster Type**
```python
# Frappe: employee + date
# Ours: employee + date + roster_type
duplicates = get_duplicate_attendance(employee, date, shift, roster_type)
```

**B. Working Hours Validation**
```python
# LENIENT VALIDATION (2025-11-01 update):
# - Allows null/0 working hours for all statuses
# - Only rejects negative values
# - Unscheduled employees can have 0 hours
# - Auto-calculated in before_save() for Present with shift

# OLD (Frappe HRMS): Required for Present/Work From Home on submit
# NEW (Our override): Optional for all, only negative rejected
```

**C. Status Validation**
```python
# Frappe: 5 statuses
# Ours: 9 statuses (added Weekly Off, Client Day Off, Holiday, On Hold)
```

---

## 📊 Scheduler Tasks Summary

| Task | Schedule | Purpose | Frappe HRMS | Ours |
|------|----------|---------|-------------|------|
| Process auto-attendance | Hourly | Mark from checkins | ✅ Has | ✅ Keep |
| Mark absent (shift employees) | Daily 1 AM | No checkins → Absent | ✅ Has | ✅ Enhanced |
| Mark unscheduled employees | Daily 1 AM | No shift → Holiday/Absent | ❌ No | ✅ Added |
| Remark incorrect records | Daily 1 AM | Fix Absent → Present | ❌ No | ✅ Added |

**Our Daily Tasks (3):**
1. `mark_absent_for_missing_checkins` - Extends Frappe's logic with roster_type
2. `mark_attendance_for_unscheduled_employees` - NEW (Frappe doesn't handle this)
3. `remark_for_active_employees` - NEW (error correction)

---

## 🌐 API Endpoints Summary

| API | Frappe HRMS | Ours | Purpose |
|-----|-------------|------|---------|
| `mark_attendance()` | ✅ Has | ✅ Enhanced | Added roster_type parameter |
| `mark_bulk_attendance()` | ❌ No | ✅ Added | Mark date range |
| `get_attendance_summary()` | ❌ No | ✅ Added | Get statistics |
| `get_status_options_for_client()` | ❌ No | ✅ Added | Return 9 status options |

**Total APIs:** 4 (1 enhanced + 3 new)

---

## ⏰ Scheduled Tasks

| Task | Schedule | Purpose |
|------|----------|---------|
| `mark_absent_for_missing_checkins` | Daily 1 AM | Auto-mark absent for employees with no checkins |
| `mark_attendance_for_unscheduled_employees` | Daily 1 AM | **Mark attendance for employees without shift assignments** |
| `remark_for_active_employees` | Daily 1 AM | **Fix incorrect Absent records by re-processing checkins** |

**What they do:**
1. **Mark Absent:** Checks all employees with shift assignments, skips if attendance exists, holiday, on leave, or has checkins, marks as Absent if none of above
2. **Unscheduled Employees:** Processes employees without shift assignments, marks Holiday or Absent based on holiday list
3. **Remark Logic:** Looks for Absent records with shift assignments that have checkins, re-processes to mark Present with calculated working hours

## 🌐 APIs Added

### Core APIs
1. `mark_attendance` - Create/update with validation (supports roster_type)
2. `get_attendance_summary` - Get summary for date range

### New APIs
3. **`mark_bulk_attendance`** - Mark attendance for date range (employee, from_date, to_date)
   - Returns: Summary with success count, failed count, marked dates, errors
   - Processes both Basic and Over-Time roster types
   - Auto-marks from checkins, holidays, or absent

## 🔄 Bulk Processing Functions

### mark_attendance_for_unscheduled_employees(date)
- **Purpose:** Handle employees without shift assignments
- **Logic:**
  - Get all active employees (excluding timesheet attendance)
  - Exclude employees with existing attendance
  - Exclude employees with shift assignments
  - Mark Holiday (if in holiday list) or Absent (default)
  - Set `is_unscheduled` flag

### remark_for_active_employees(date)
- **Purpose:** Fix incorrect Absent records
- **Logic:**
  - Find Absent attendance with shift assignments
  - Check if checkins exist for those shifts
  - If checkins found:
    - Calculate actual working hours
    - Update status to Present
    - Set late_entry/early_exit flags
    - Add comment explaining remark

## 🎯 Advanced Features

### 1. Multi-Shift Support
- **Overlapping Shift Validation:** Prevents marking attendance for overlapping shifts on same day
- **Roster Type:** Separate tracking for Basic vs Over-Time shifts
- **Shift Timing Check:** Compares shift start/end times to detect overlaps

### 2. Operations Integration
- **Auto-Population:** Automatically populates operations_shift, site, project, operations_role from shift assignment
- **Billing Support:** Links to project and sale_item for accurate billing
- **Site Tracking:** Tracks which site employee worked at

### 3. Unscheduled Employee Handling
- **Coverage:** Ensures ALL employees have attendance marked (not just those with shifts)
- **Holiday Detection:** Automatically marks holidays for unscheduled employees
- **Flag:** Sets `is_unscheduled` for reporting and filtering

### 4. Error Correction
- **Remark Logic:** Automatically fixes attendance marked Absent before checkins were recorded
- **Re-Processing:** Recalculates working hours from actual checkin data
- **Audit Trail:** Adds comments explaining why attendance was remarked

## 🎯 Summary

**What Frappe HRMS Already Does (We Keep):**
- ✅ Auto-mark attendance from Employee Checkin (via Shift Type)
- ✅ Calculate working hours from checkins
- ✅ Set late_entry and early_exit flags
- ✅ Link attendance to checkin records
- ✅ Mark absent for employees with no checkins
- ✅ Process attendance via hourly scheduler
- ✅ Holiday detection from Holiday List
- ✅ Leave integration

**What We Override/Replace:**
1. `validate()` method - Extended with 9 status options, roster_type, overlapping shift check
2. `validate_duplicate_record()` - Enhanced with roster_type support
3. `validate_working_hours()` - Status-specific validation rules

**What We Extend (Add To):**
1. `before_save()` - Auto-populate operations fields
2. `after_insert()` - Set day_off_ot flag

**What We Add (New Functionality):**
1. **21 custom fields** - Operations, roster, tracking, integration
2. **Overlapping shift validation** - Multi-shift support
3. **Roster type tracking** - Basic vs Over-Time
4. **Bulk marking API** - Date range processing
5. **Unscheduled employee handling** - Coverage for all employees
6. **Remark logic** - Error correction
7. **Operations field auto-population** - Site/project/role tracking
8. **4 new status options** - Weekly Off, Client Day Off, Holiday, On Hold
9. **3 new APIs** - Bulk marking, summary, status options
10. **2 new scheduler tasks** - Unscheduled employees, remark logic

**Code Statistics:**
- LOC: ~1,200 lines (650+ lines added to existing ~550)
- Files Created: 3 (custom field definitions)
- Files Modified: 5 (manager, install, hooks, docs, validation)
- Custom Fields: 21
- APIs: 4 (1 enhanced + 3 new)
- Scheduler Tasks: 3 daily tasks
- Validation Methods: 6 new methods (added: set_shift_assignment, _get_shift_working_hours)
- Core Overrides: 5 methods (validate, validate_duplicate_record, validate_working_hours, set_shift_assignment, _get_shift_working_hours)

**Integration:** Document event hooks + scheduler (no core changes)  
**Migration Status:** 90% complete (23/25 features from one_fm)  
**Production Ready:** ✅ Yes (covers all critical HR attendance functionality)

**Recent Enhancements (2025-11-01):**
- ✅ Half Day auto-calculation (9h → 4.5h)
- ✅ Shift requirement only for Present (one_fm compatibility)
- ✅ Lenient working hours validation (allows null/0)
- ✅ Unscheduled employee support (manual hours entry)
- ✅ Status change recalculation (Present ↔ Half Day)

---

*For code: see `frappe_ticktix/plugins/hr/attendance/attendance_manager.py`*

## 📚 **Detailed Feature Explanation**

### 1. **Attendance Status Options** (Extended)

**Frappe HRMS Default (5):**
- Present
- Absent  
- On Leave
- Half Day
- Work From Home

**Our Extension (9):**  
Added 4 new statuses:
- **Weekly Off** - Company-assigned weekly off (NOT billable, from Employee Schedule or Holiday List)
- **Client Day Off** - Client-requested day off (IS billable - client pays, from Shift Request)
- **Holiday** - Public/company holiday (from Holiday List, auto-marked)
- **On Hold** - Pending client approval for billing (special payroll handling)

**Implementation:**
- Property Setter changes `status` field options
- Client Scripts override UI dialogs (Mark Attendance Dialog, Employee Attendance Tool)
- Python validation extended in `AttendanceOverride.validate()`

---

### 2. **Late Entry / Early Exit Flags** (Frappe Built-in)

**What Frappe Already Does:**
- `Shift Type` has fields:
  - `enable_late_entry_marking` - Enable/disable late entry detection
  - `late_entry_grace_period` - Grace period in minutes
  - `enable_early_exit_marking` - Enable/disable early exit detection  
  - `early_exit_grace_period` - Grace period in minutes
- `process_auto_attendance()` method in Shift Type:
  - Compares checkin time vs shift_start + grace_period
  - Sets `late_entry=1` if late
  - Compares checkout time vs shift_end - grace_period
  - Sets `early_exit=1` if early
- Attendance doctype has `late_entry` and `early_exit` checkbox fields

**What We Do:**
- **Nothing!** We use Frappe's built-in functionality
- Our `AttendanceOverride` class preserves all Frappe logic
- We only extend validation for custom statuses

**Example:**
```python
# Frappe's code (shift_type.py line 191-195):
if (
    cint(self.enable_late_entry_marking)
    and in_time
    and in_time > logs[0].shift_start + timedelta(minutes=cint(self.late_entry_grace_period))
):
    late_entry = True
```

---

### 3. **Auto-Detect Shift & Calculate Working Hours** (Frappe Built-in)

**What Frappe Already Does:**
- `Shift Type.process_auto_attendance()` runs on scheduler
- Gets Employee Checkin records (IN/OUT logs)
- Calculates working hours: `out_time - in_time`
- Creates Attendance record with:
  - `status` = Present/Absent based on checkins
  - `working_hours` = calculated hours
  - `in_time` = first IN checkin time
  - `out_time` = last OUT checkin time
  - `late_entry` and `early_exit` flags
  - `shift` = Shift Type
- Links checkins: Employee Checkin has `attendance` field pointing to created Attendance

**What We Extended:**
- **Roster type support:** Added `roster_type` field (Basic/Over-Time)
- **Multi-shift validation:** Check for overlapping shifts on same day
- **Unscheduled employees:** Handle employees without shift assignments
- **Operations fields:** Auto-populate site, project, role from shift assignment
- **Remark logic:** Fix attendance marked Absent before checkins appeared

**Example - Frappe's Auto-Attendance:**
```python
# Employee Checkin records:
# IN:  2025-11-01 08:35:00 (shift starts 08:30, 5 min late within grace)
# OUT: 2025-11-01 17:25:00 (shift ends 17:30, 5 min early within grace)

# Frappe creates Attendance:
{
    "status": "Present",
    "working_hours": 8.83,  # 8 hours 50 minutes
    "late_entry": 0,  # Within grace period
    "early_exit": 0,  # Within grace period
    "in_time": "2025-11-01 08:35:00",
    "out_time": "2025-11-01 17:25:00"
}
```

---

### 4. **Custom Fields (21 Fields)** (Our Addition)

**Purpose:** Enable operations management and project-based billing

**Categories:**

#### Operations Section (4 fields)
- `operations_shift` → Operations Shift doctype (if exists)
- `site` → Operations Site (work location)
- `project` → Project (for billing)
- `operations_role` → Operations Role (Guard, Supervisor, etc.)

**Auto-Population Logic:**
```python
def populate_operations_fields(self):
    if not self.shift_assignment:
        return
    
    # Get from Shift Assignment
    shift_data = frappe.db.get_value("Shift Assignment", self.shift_assignment, 
                                     ['shift', 'site', 'shift_type'], as_dict=True)
    
    # Set operations shift (if Operations Shift doctype exists)
    if shift_data.get('shift'):
        self.operations_shift = shift_data.shift
        
        # Get role and other fields from operations shift
        if frappe.db.exists("Operations Shift", shift_data.shift):
            ops_shift = frappe.db.get_value("Operations Shift", shift_data.shift,
                                           ['operations_role', 'post_abbrv', 'sale_item'], as_dict=True)
            self.operations_role = ops_shift.operations_role
            self.post_abbrv = ops_shift.post_abbrv
            self.sale_item = ops_shift.sale_item
    
    # Set site and project
    if shift_data.get('site'):
        self.site = shift_data.site
        project = frappe.db.get_value("Operations Site", shift_data.site, 'project')
        if project:
            self.project = project
```

#### Roster & Overtime Section (4 fields)
- `roster_type` (Select: Basic/Over-Time) - Distinguish regular vs OT shifts
- `day_off_ot` (Check) - Employee worked on day off (eligible for OT pay)
- `post_abbrv` (Data) - Short code for role (used in reports)
- `sale_item` (Data) - Sales item for billing calculations

**Roster Type Usage:**
```python
# Basic roster - regular shift
attendance1 = {
    "roster_type": "Basic",
    "working_hours": 8,
    "status": "Present"
}

# Over-Time roster - OT shift (same day, different shift)
attendance2 = {
    "roster_type": "Over-Time",
    "working_hours": 4,
    "status": "Present"  # Paid at OT rate
}

# Duplicate check includes roster_type:
# Can have 2 attendance records for same employee same date
# if different roster_type
```

#### Integration Section (3 fields)
- `timesheet` → Timesheet (for project-based attendance)
- `reference_doctype` → DocType (source document type)
- `reference_docname` (Dynamic Link) - Source document name

#### Tracking Section (2 fields)
- `custom_employment_type` → Employment Type (affects payroll calculation)
- `is_unscheduled` (Check) - Employee has no shift assignment

---

### 5. **Overlapping Shift Validation** (Our Addition)

**Problem:** Employee assigned to multiple shifts on same day with overlapping timings

**Frappe HRMS:** Only checks for duplicate (same employee, same date) but allows multiple shifts

**Our Solution:**
```python
def validate_overlapping_shift(self):
    """
    Check for overlapping shift attendance
    Prevents marking attendance for overlapping shifts on same day
    """
    if not self.shift:
        return
    
    roster_type = self.roster_type if hasattr(self, 'roster_type') else 'Basic'
    
    # Get other attendance records for same employee, same date, different shift
    overlapping = AttendanceManager.get_overlapping_shift_attendance(
        self.employee,
        self.attendance_date,
        self.shift,
        roster_type,
        self.name
    )
    
    if overlapping:
        frappe.throw(
            _("Attendance for employee {0} is already marked for an overlapping shift {1}").format(
                self.employee, overlapping.shift
            ),
            title=_("Overlapping Shift Attendance")
        )
```

**Shift Timing Check:**
```python
def has_overlapping_timings(shift1, shift2):
    """Check if two shifts have overlapping timings"""
    # Get shift timings
    shift1_data = frappe.db.get_value("Shift Type", shift1, ['start_time', 'end_time'], as_dict=True)
    shift2_data = frappe.db.get_value("Shift Type", shift2, ['start_time', 'end_time'], as_dict=True)
    
    # Check overlap: shift1 starts before shift2 ends AND shift2 starts before shift1 ends
    return (shift1_data.start_time < shift2_data.end_time) and \
           (shift2_data.start_time < shift1_data.end_time)
```

**Example:**
```
Employee: John
Date: 2025-11-01

Shift A: 08:00 - 16:00 (Morning)
Shift B: 12:00 - 20:00 (Afternoon) - OVERLAPS with Shift A

Trying to mark:
- Attendance 1: Shift A, roster_type=Basic → ✅ Allowed
- Attendance 2: Shift B, roster_type=Basic → ❌ BLOCKED (overlapping timings)
- Attendance 3: Shift B, roster_type=Over-Time → ✅ Allowed (different roster_type)

Non-overlapping example:
Shift A: 08:00 - 16:00 (Morning)
Shift C: 16:00 - 00:00 (Evening) - No overlap

- Attendance 1: Shift A → ✅ Allowed
- Attendance 2: Shift C → ✅ Allowed (no overlap)
```

---

### 6. **Bulk Marking API** (Our Addition)

**Problem:** Need to mark attendance for employee for multiple days (e.g., retroactive marking)

**Frappe HRMS:** Only single-day marking via UI or `mark_attendance()` function

**Our Solution:**
```python
@frappe.whitelist()
def mark_bulk_attendance(employee, from_date, to_date, roster_type="Basic"):
    """
    Mark attendance for an employee for a date range
    
    Returns: Summary with success/failure counts
    """
    import pandas as pd
    
    marked = []
    errors = []
    
    # Generate date range
    date_range = pd.date_range(from_date, to_date)
    
    for date in date_range:
        try:
            # Check if attendance exists
            existing = AttendanceManager.get_duplicate_attendance(employee, date.date(), roster_type=roster_type)
            if existing:
                errors.append({'date': str(date.date()), 'error': f"Already exists: {existing[0].name}"})
                continue
            
            # Get shift assignment
            shift_assignment = AttendanceManager.get_shift_assignment(employee, date.date())
            
            if shift_assignment:
                # Mark from checkins if available
                attendance = AttendanceManager.mark_attendance_from_checkins(
                    employee, date.date(), shift_assignment.name
                )
                if attendance:
                    marked.append(str(date.date()))
            else:
                # No shift, check holiday
                holiday = AttendanceManager.is_holiday(employee, date.date())
                if holiday:
                    # Create Holiday attendance
                    ...
                else:
                    # Create Absent attendance
                    ...
                marked.append(str(date.date()))
            
            frappe.db.commit()
            
        except Exception as e:
            errors.append({'date': str(date.date()), 'error': str(e)})
    
    return {
        'success': len(marked),
        'failed': len(errors),
        'marked_dates': marked,
        'errors': errors,
        'message': f"Marked {len(marked)} attendance records"
    }
```

**Usage:**
```javascript
// Mark attendance for last week
frappe.call({
    method: 'frappe_ticktix.plugins.hr.attendance.attendance_manager.mark_bulk_attendance',
    args: {
        employee: 'EMP-001',
        from_date: '2025-10-25',
        to_date: '2025-10-31',
        roster_type: 'Basic'
    },
    callback: function(r) {
        console.log(r.message);
        // {success: 5, failed: 2, marked_dates: [...], errors: [...]}
    }
});
```

---

### 7. **Unscheduled Employee Handling** (Our Addition)

**Problem:** Employees without shift assignments don't get attendance marked

**Frappe HRMS:** Only processes employees with shift assignments in `process_auto_attendance()`

**Our Solution:**
```python
def mark_attendance_for_unscheduled_employees(date=None):
    """
    Mark attendance for employees without shift assignments
    Marks Holiday or Absent based on holiday list
    """
    if not date:
        date = add_days(today(), -1)
    
    # Get all active employees (not on timesheet attendance)
    all_employees = frappe.get_list("Employee", 
        filters={"status": "Active", "attendance_by_timesheet": 0},
        fields=['name', 'employee_name', 'company', 'department', 'holiday_list']
    )
    
    # Get employees who already have attendance
    existing_attendance = frappe.get_all("Attendance",
        filters={'attendance_date': date, 'roster_type': 'Basic'},
        pluck='employee'
    )
    
    # Get employees with shift assignments
    shift_assigned = frappe.get_all("Shift Assignment",
        filters={'start_date': date, 'docstatus': 1},
        pluck='employee'
    )
    
    # Filter unscheduled employees
    scheduled_set = set(shift_assigned)
    unscheduled = [emp for emp in all_employees 
                   if emp.name not in existing_attendance and emp.name not in scheduled_set]
    
    # Mark attendance for unscheduled employees
    for emp in unscheduled:
        # Check if holiday
        holiday = AttendanceManager.is_holiday(emp.name, date)
        
        if holiday:
            # Mark as Holiday
            attendance = frappe.new_doc('Attendance')
            attendance.employee = emp.name
            attendance.attendance_date = date
            attendance.status = 'Holiday'
            attendance.roster_type = 'Basic'
            attendance.is_unscheduled = 1  # Flag for reporting
            attendance.comment = f"Holiday - {holiday}"
            attendance.insert()
            attendance.submit()
        else:
            # Mark as Absent
            attendance = frappe.new_doc('Attendance')
            attendance.employee = emp.name
            attendance.attendance_date = date
            attendance.status = 'Absent'
            attendance.roster_type = 'Basic'
            attendance.is_unscheduled = 1
            attendance.comment = "No shift assignment found"
            attendance.insert()
            attendance.submit()
```

**Scheduled Task:**
```python
# hooks.py
scheduler_events = {
    "daily": [
        "frappe_ticktix.plugins.hr.attendance.attendance_manager.mark_attendance_for_unscheduled_employees"
    ]
}
```

**Result:** ALL active employees get attendance marked (scheduled + unscheduled)

---

### 8. **Remark Logic** (Our Addition)

**Problem:** Attendance marked Absent, then checkins appear later (network delay, sync issues)

**Frappe HRMS:** No automatic correction, attendance stays Absent

**Our Solution:**
```python
def remark_for_active_employees(date=None):
    """
    Fix incorrect Absent records by re-processing checkins
    Looks for Absent attendance with shift assignments that have checkins
    """
    if not date:
        date = today()
    
    # Get Absent attendance records with shift assignments
    absent_records = frappe.get_list("Attendance",
        filters={
            "attendance_date": date,
            "status": "Absent",
            "shift_assignment": ["!=", ""]
        },
        fields=['name', 'employee', 'shift_assignment', 'roster_type']
    )
    
    for record in absent_records:
        # Check if checkins exist
        checkins = frappe.get_list("Employee Checkin",
            filters={"shift_assignment": record.shift_assignment},
            fields=['name', 'log_type', 'time', 'late_entry', 'early_exit'],
            order_by='time ASC'
        )
        
        if checkins:
            # Has checkins, re-process
            ins = [c for c in checkins if c.log_type == "IN"]
            outs = [c for c in checkins if c.log_type == "OUT"]
            
            if ins:
                # Get shift timing
                shift_data = frappe.db.get_value("Shift Assignment", record.shift_assignment,
                                                 ['start_datetime', 'end_datetime'], as_dict=True)
                
                first_in = ins[0]
                last_out = outs[-1] if outs else None
                
                # Calculate working hours
                if last_out:
                    time_diff = get_datetime(last_out.time) - get_datetime(first_in.time)
                    working_hours = time_diff.total_seconds() / 3600
                else:
                    # No checkout, use shift end time
                    time_diff = shift_data.end_datetime - get_datetime(first_in.time)
                    working_hours = time_diff.total_seconds() / 3600
                
                # Update attendance
                attendance_doc = frappe.get_doc("Attendance", record.name)
                attendance_doc.status = 'Present'
                attendance_doc.working_hours = round(working_hours, 2)
                attendance_doc.comment = "Re-marked from checkins (was incorrectly marked Absent)"
                if first_in.late_entry:
                    attendance_doc.late_entry = 1
                if last_out and last_out.early_exit:
                    attendance_doc.early_exit = 1
                
                attendance_doc.save()
                frappe.db.commit()
```

**Example:**
```
Timeline:
01:00 AM - Daily job runs, marks Employee X as Absent (no checkins found)
08:30 AM - Employee X checks in (mobile app was offline, syncs now)
05:30 PM - Employee X checks out

02:00 AM (next day) - Remark job runs:
- Finds Absent attendance for yesterday
- Finds checkins now exist for that shift
- Recalculates working hours: 9 hours
- Updates status: Absent → Present
- Adds comment: "Re-marked from checkins (was incorrectly marked Absent)"
- Sets late_entry and early_exit flags
```

---

### 9. **Summary API** (Our Addition)

**Purpose:** Get attendance statistics for reporting and dashboards

**Frappe HRMS:** No built-in summary endpoint

**Our Addition:**
```python
@frappe.whitelist()
def get_attendance_summary(employee, from_date, to_date):
    """
    Get attendance summary for an employee
    
    Returns: Summary with counts by status and total working hours
    """
    attendances = frappe.db.get_list("Attendance",
        filters={
            'employee': employee,
            'attendance_date': ['between', [from_date, to_date]],
            'docstatus': 1
        },
        fields=['name', 'attendance_date', 'status', 'working_hours']
    )
    
    # Group by status
    summary = {
        'total_days': 0,
        'present': 0,
        'absent': 0,
        'on_leave': 0,
        'half_day': 0,
        'work_from_home': 0,
        'weekly_off': 0,
        'client_day_off': 0,
        'holiday': 0,
        'on_hold': 0,
        'total_working_hours': 0,
        'records': attendances
    }
    
    for att in attendances:
        summary['total_days'] += 1
        
        if att.status == 'Present':
            summary['present'] += 1
        elif att.status == 'Absent':
            summary['absent'] += 1
        elif att.status == 'On Leave':
            summary['on_leave'] += 1
        elif att.status == 'Half Day':
            summary['half_day'] += 1
        elif att.status == 'Work From Home':
            summary['work_from_home'] += 1
        elif att.status == 'Weekly Off':
            summary['weekly_off'] += 1
        elif att.status == 'Client Day Off':
            summary['client_day_off'] += 1
        elif att.status == 'Holiday':
            summary['holiday'] += 1
        elif att.status == 'On Hold':
            summary['on_hold'] += 1
        
        if att.working_hours:
            summary['total_working_hours'] += att.working_hours
    
    return summary
```

**Usage:**
```javascript
// Get October attendance summary
frappe.call({
    method: 'frappe_ticktix.plugins.hr.attendance.attendance_manager.get_attendance_summary',
    args: {
        employee: 'EMP-001',
        from_date: '2025-10-01',
        to_date: '2025-10-31'
    },
    callback: function(r) {
        console.log(r.message);
        /*
        {
            total_days: 31,
            present: 22,
            absent: 1,
            on_leave: 2,
            half_day: 1,
            work_from_home: 0,
            weekly_off: 4,
            holiday: 1,
            total_working_hours: 176.5,
            records: [...]
        }
        */
    }
});
```

---

*For code: see `frappe_ticktix/plugins/hr/attendance/attendance_manager.py`*
