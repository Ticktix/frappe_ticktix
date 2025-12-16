# Feature Breakdown & Business Value Guide

**Version:** 1.0  
**Date:** October 20, 2025  
**Purpose:** Understand what each feature does and why you need it

---

## 📋 Table of Contents

1. [How to Use This Guide](#how-to-use-this-guide)
2. [HR & Payroll Features](#hr--payroll-features)
3. [Operations Features](#operations-features)
4. [Recruitment Features](#recruitment-features)
5. [Accommodation Features](#accommodation-features)
6. [Compliance Features](#compliance-features)
7. [Fleet Features](#fleet-features)
8. [Procurement Features](#procurement-features)
9. [Support Features](#support-features)

---

## 📖 How to Use This Guide

### **Format for Each Feature:**

**Feature Name**
- **What It Does:** Plain English explanation
- **Why You Need It:** Business value/problem it solves
- **Who Uses It:** Target users (HR, Operations, Managers, etc.)
- **End Goal:** What you achieve by implementing this
- **Customizations from one_fm:** Specific custom fields, options, overrides added
- **Dependencies:** What else needs to be in place
- **Priority:** HIGH / MEDIUM / LOW
- **Example Scenario:** Real-world use case

---

## 👥 HR & PAYROLL FEATURES

### **CATEGORY: Attendance & Shifts**

---

#### **1. Shift Types & Templates**

**What It Does:**
Defines different types of work shifts (Morning, Evening, Night, Split shifts) with specific start/end times, break times, and working hours.

**Why You Need It:**
- Standardize shift timings across your organization
- Automatically calculate working hours for payroll
- Support 24/7 operations with rotating shifts
- Handle split shifts (e.g., 6am-10am, then 2pm-6pm)

**Who Uses It:**
- HR Manager (creates shift templates)
- Operations Manager (assigns shifts to sites)
- Employees (view their shift schedule)

**End Goal:**
✅ **Consistent shift management** - Everyone knows exact working hours  
✅ **Automated time tracking** - No manual calculation of hours worked  
✅ **Fair scheduling** - Transparent shift rotation and distribution  

**Customizations from one_fm:**
- **Custom Fields Added (15+ fields):**
  - `shift_type` - Category: Morning/Afternoon/Evening/Day/Night
  - `duration` - Shift duration in hours
  - `shift_work` - Enable shift-based work flag
  - `deadline` - Auto-absent deadline after shift start
  - `edit_start_time_and_end_time` - Allow runtime time modification
  - `has_split_shift` - Enable split shift functionality
  - `first_shift_start_time` - First part of split shift
  - `first_shift_end_time` - First part end time
  - `second_shift_start_time` - Second part start time
  - `second_shift_end_time` - Second part end time
  - `notification_reminder_after_shift_start` - Employee reminder (mins)
  - `supervisor_reminder_shift_start` - Supervisor reminder (mins)
  - `notification_reminder_after_shift_end` - End reminder (mins)
  - `supervisor_reminder_start_ends` - Supervisor end reminder (mins)

- **Override File:** `one_fm/overrides/shift_type.py`
- **Lines of Code:** ~350 lines custom logic

**Dependencies:**
- Employee master data
- Company working hours configuration

**Priority:** ⭐ **HIGH** - Foundation for attendance tracking

**Example Scenario:**
```
Security Company Scenario:
- Morning Shift: 6:00 AM - 2:00 PM (8 hours)
- Evening Shift: 2:00 PM - 10:00 PM (8 hours)
- Night Shift: 10:00 PM - 6:00 AM (8 hours)
- Split Shift: 6:00 AM - 10:00 AM, 6:00 PM - 10:00 PM (8 hours total)

Result: Guards automatically assigned correct shift, overtime calculated 
when they work beyond shift end time.
```

---

#### **2. Shift Assignment**

**What It Does:**
Assigns specific employees to specific shifts for a date range. Tracks who works which shift, when, and for how long.

**Why You Need It:**
- Plan workforce ahead of time
- Prevent scheduling conflicts (employee can't be in 2 places)
- Track shift changes and history
- Enable automatic attendance marking based on shift

**Who Uses It:**
- Operations Manager (assigns shifts)
- Site Supervisor (requests shift changes)
- Employees (view assigned shifts)

**End Goal:**
✅ **Proactive scheduling** - Plan weeks/months in advance  
✅ **Conflict prevention** - System blocks overlapping assignments  
✅ **Audit trail** - Know who was supposed to work when  

**Customizations from one_fm:**
- **Custom Fields Added:**
  - `operations_shift` - Link to Operations Shift
  - `operations_role` - Link to Operations Role
  - `operations_site` - Link to Operations Site
  - `post_type` - Post type reference
  - `roster_type` - Basic/Overtime roster type
  - `shift_working` - Shift working hours calculation
  - `assignment_based_on` - Auto-assignment logic (Roster/Manual)

- **Override File:** `one_fm/overrides/shift_assignment.py`
- **Custom Logic:**
  - Overlapping shift validation
  - Operations site integration
  - Auto-assignment from roster
  - Shift change tracking
  - Real-time shift updates across operations

- **Lines of Code:** ~280 lines

**Dependencies:**
- Shift Types configured
- Employee master data
- Operations sites (if site-specific shifts)

**Priority:** ⭐ **HIGH** - Core operations functionality

**Example Scenario:**
```
Facility Management Scenario:
- Guard John assigned to Site A, Morning Shift, Jan 1-15
- Guard Sarah assigned to Site A, Evening Shift, Jan 1-15
- System blocks attempt to assign John to Site B morning shift on Jan 10
  (already assigned to Site A)

Result: No double-booking, clear visibility of who works where and when.
```

---

#### **3. Shift Requests**

**What It Does:**
Allows employees to request shift changes, swaps, or time-off. Managers can approve/reject with reason tracking.

**Why You Need It:**
- Empower employees to manage their schedule
- Formalize shift change process
- Maintain approval workflow and accountability
- Track why shifts were changed

**Who Uses It:**
- Employees (submit requests)
- Supervisors (approve/reject)
- HR (monitor patterns)

**End Goal:**
✅ **Employee flexibility** - Workers can request changes when needed  
✅ **Controlled process** - All changes go through approval  
✅ **Better morale** - Employees feel heard and accommodated  

**Customizations from one_fm:**
- **Custom DocType:** `one_fm/one_fm/doctype/shift_request/`
- **Custom Fields:**
  - `from_shift` - Current shift
  - `to_shift` - Requested shift
  - `reason` - Reason for change
  - `approval_status` - Pending/Approved/Rejected
  - `approver` - Manager who approved/rejected
  - `approval_date` - Date of decision

- **Custom Logic:**
  - Auto-notification to supervisor
  - Integration with shift assignment
  - Swap validation (both employees must agree)
  - History tracking

- **Lines of Code:** ~150 lines

**Dependencies:**
- Shift Assignment system
- Approval workflow configuration

**Priority:** 🟡 **MEDIUM** - Nice to have, improves employee satisfaction

**Example Scenario:**
```
Shift Swap Scenario:
- Guard Maria has family emergency on Tuesday
- She requests shift swap with Guard David (who's off Tuesday)
- Supervisor reviews request
- Approves swap
- System updates both assignments automatically

Result: Emergency handled, coverage maintained, all documented.
```

---

#### **4. Employee Checkin/Checkout**

**What It Does:**
Records exact time when employee arrives (check-in) and leaves (check-out) work location. Can use mobile app, biometric device, or manual entry.

**Why You Need It:**
- Accurate time tracking for payroll
- Verify employees are at assigned location
- Calculate overtime automatically
- Detect late arrivals and early departures

**Who Uses It:**
- Employees (check in/out via mobile or kiosk)
- Supervisors (monitor real-time attendance)
- Payroll team (use data for salary calculation)

**End Goal:**
✅ **Accurate payroll** - Pay for actual hours worked  
✅ **Location verification** - Confirm employee at correct site  
✅ **Real-time monitoring** - Know who's working right now  

**Customizations from one_fm:**
- **Custom Fields Added (10+ fields):**
  - `operations_shift` - Link to operations shift
  - `operations_site` - Link to site location
  - `operations_role` - Role at time of checkin
  - `shift_assignment` - Link to assigned shift
  - `latitude` - GPS latitude
  - `longitude` - GPS longitude
  - `location` - Address/location description
  - `skip_auto_attendance` - Manual override flag
  - `attendance` - Auto-created attendance link
  - `device_id` - Mobile device identifier
  - `checkin_photo` - Photo captured at checkin (optional)

- **Override File:** `one_fm/overrides/employee_checkin.py`
- **Custom Logic:**
  - GPS location capture and validation
  - Site boundary verification (geofencing)
  - Auto-attendance creation on checkout
  - Late/early detection and flagging
  - Photo capture integration
  - Device tracking for security

- **Lines of Code:** ~420 lines

**Dependencies:**
- Shift Assignment (to know expected check-in time)
- Mobile app or checkin device
- GPS/location tracking (optional)

**Priority:** ⭐ **HIGH** - Essential for accurate payroll

**Example Scenario:**
```
Mobile Checkin Scenario:
- Guard assigned to Site A, Morning Shift (6 AM - 2 PM)
- Guard arrives at 5:55 AM, checks in via mobile app
- App captures GPS location, timestamp, photo (optional)
- Guard leaves at 2:05 PM, checks out
- System calculates: 8 hours 10 minutes worked
- 10 minutes overtime automatically flagged for payroll

Result: Exact hours worked, proof of location, automated OT calculation.
```

---

#### **5. Attendance Tracking**

**What It Does:**
Consolidated record of employee work attendance - Present, Absent, Half Day, Leave, Holiday, etc. Links checkin/checkout data with shift assignments.

**Why You Need It:**
- Single source of truth for "who worked when"
- Calculate monthly attendance for payroll
- Track attendance patterns and absenteeism
- Generate attendance reports for clients

**Who Uses It:**
- HR team (review attendance records)
- Payroll team (calculate salary based on attendance)
- Managers (monitor team attendance)
- Clients (receive attendance reports)

**End Goal:**
✅ **Payroll accuracy** - Pay only for days worked  
✅ **Compliance** - Meet labor law attendance requirements  
✅ **Performance management** - Identify attendance issues  
✅ **Client reporting** - Transparent billing based on actual attendance  

**Customizations from one_fm:**
- **Custom Status Options (Extended from 4 to 9):**
  - Standard Frappe: Present, Absent, On Leave, Half Day
  - **Added by one_fm:**
    - `Work From Home` - Remote work tracking
    - `Day Off` - Scheduled day off
    - `Holiday` - Public holiday
    - `On Hold` - Employment on hold
    - `Client Day Off` - Client-specific holidays

- **Custom Fields Added (20+ fields):**
  - `shift_assignment` - Link to shift assignment
  - `operations_shift` - Link to operations shift
  - `operations_role` - Link to operations role
  - `operations_site` - Link to operations site
  - `project` - Link to project
  - `post_type` - Post type
  - `post_abbrv` - Post abbreviation
  - `sale_item` - Billable item code
  - `roster_type` - Basic/Over-Time
  - `day_off_ot` - Day off overtime flag
  - `is_unscheduled` - Unscheduled work flag
  - `timesheet` - Link to timesheet
  - `reference_doctype` - Dynamic reference
  - `reference_docname` - Dynamic reference name
  - `custom_employment_type` - Employment type
  - `comment` - Additional comments
  - `late_entry` - Late arrival flag
  - `early_exit` - Early departure flag
  - `working_hours` - Actual hours worked

- **Override File:** `one_fm/overrides/attendance.py` (1,391 lines!)
- **Custom Logic:**
  - Weekly off detection based on holiday list
  - Day off OT rate application (1.5x, 2x)
  - Overlapping shift validation
  - Auto-status setting based on schedule
  - Integration with payroll for OT
  - Operations shift integration for billing
  - Project-based attendance tracking
  - Site-specific validation
  - Mobile attendance support

- **Lines of Code:** ~1,391 lines (largest override)

**Dependencies:**
- Shift Assignments
- Employee Checkin/Checkout
- Leave Management (to mark approved leaves)
- Holiday List

**Priority:** ⭐ **HIGH** - Critical for payroll and billing

**Example Scenario:**
```
Monthly Attendance Scenario:
Employee: Guard Ahmed
Month: January 2025

Attendance Record:
- Days Present: 26 days (checked in/out on time)
- Days Absent: 1 day (no checkin record, not on leave)
- Days on Leave: 2 days (approved annual leave)
- Holidays: 1 day (national holiday)
- Half Days: 1 day (left early with permission)

Payroll Calculation:
- Base salary for 26 full days
- Deduction for 1 absent day
- 2 paid leave days
- 1 paid holiday
- 0.5 day deduction for half day

Result: Accurate salary calculation, clear attendance history.
```

---

#### **6. Auto-Attendance Marking**

**What It Does:**
Automatically creates attendance records based on checkin/checkout data and shift assignments. Marks absent if no checkin by deadline.

**Why You Need It:**
- Eliminate manual attendance entry
- Reduce HR workload
- Ensure no attendance is missed
- Immediate visibility of who's working

**Who Uses It:**
- System (runs automatically)
- HR team (monitors and corrects exceptions)

**End Goal:**
✅ **Zero manual work** - Attendance marked automatically  
✅ **Real-time data** - Know attendance status immediately  
✅ **Error reduction** - No human data entry mistakes  

**Customizations from one_fm:**
- **Custom Scheduled Tasks:**
  - `mark_attendance_from_checkin` - Hourly job
  - `mark_absent_for_no_checkin` - Runs after shift deadline
  - `process_auto_attendance` - Daily reconciliation
  - `send_attendance_alerts` - Notify supervisors

- **Custom Logic:**
  - Smart status detection (Present/Late/Half Day/Absent)
  - Shift-based attendance marking
  - Operations shift integration
  - Checkin-checkout pairing
  - Working hours calculation
  - OT hours detection and flagging
  - Holiday/day-off handling
  - Exception handling for incomplete data

- **Implementation:**
  - File: `one_fm/one_fm/api/tasks.py`
  - Scheduler configuration in `hooks.py`

- **Lines of Code:** ~280 lines

**Dependencies:**
- Shift Assignments
- Employee Checkin system
- Scheduled task runner

**Priority:** ⭐ **HIGH** - Major time saver

**Example Scenario:**
```
Automated Process (runs every hour):
9:00 AM: System checks all 6 AM - 2 PM shifts
- Guard John: Checked in 5:55 AM → Mark "Present"
- Guard Sarah: Checked in 7:30 AM (90 mins late) → Mark "Present" + "Late" flag
- Guard David: No checkin record → Mark "Absent"

2:00 PM: System checks checkout
- Guard John: Checked out 2:05 PM → Normal (5 min tolerance)
- Guard Sarah: No checkout yet → Send reminder notification

Result: Attendance marked without HR intervention, exceptions flagged.
```

---

#### **7. Penalty Management**

**What It Does:**
Tracks disciplinary actions and financial penalties for attendance violations (late arrivals, unauthorized absence, early departure).

**Why You Need It:**
- Enforce attendance policies consistently
- Automate penalty calculations
- Deduct penalties from salary
- Maintain disciplinary records

**Who Uses It:**
- Supervisors (issue penalties)
- HR (review and approve)
- Payroll (deduct from salary)

**End Goal:**
✅ **Policy enforcement** - Consistent application of rules  
✅ **Automated deductions** - Penalties auto-deducted from payroll  
✅ **Documentation** - Complete penalty history for HR records  

**Customizations from one_fm:**
- **Custom DocTypes Created:**
  - `penalty` - Master penalty types
  - `penalty_issuance` - Actual penalty records
  - `penalty_type` - Penalty categories
  - `penalty_deduction` - Payroll deduction link

- **Penalty Types:**
  - Late arrival (configurable grace period)
  - Unauthorized absence
  - Early departure
  - Uniform violation
  - Behavioral issues
  - Safety violations

- **Custom Fields:**
  - `employee` - Employee who received penalty
  - `penalty_type` - Type of violation
  - `penalty_date` - Date of violation
  - `penalty_amount` - Deduction amount
  - `issued_by` - Supervisor who issued
  - `approved_by` - HR approval
  - `status` - Pending/Approved/Cancelled
  - `warning_level` - Verbal/Written/Final
  - `deducted_from_salary` - Payroll link flag

- **Custom Logic:**
  - Auto-penalty creation from late attendance
  - Progressive discipline (warnings → deductions)
  - Approval workflow
  - Payroll integration for deductions
  - Penalty history tracking
  - Appeal mechanism

- **Location:** `one_fm/legal/doctype/penalty*/`
- **Lines of Code:** ~450 lines total

**Dependencies:**
- Attendance records
- Company penalty policy configuration
- Payroll system

**Priority:** 🟡 **MEDIUM** - Important for discipline management

**Example Scenario:**
```
Penalty Policy:
- Late arrival (30+ minutes): $10 deduction
- Unauthorized absence: 1 day salary deduction
- 3 penalties in a month: Written warning

Scenario:
- Guard Lisa late 3 times in January (45 min, 60 min, 30 min)
- System automatically:
  1. Creates 3 penalty records ($10 each)
  2. Adds $30 deduction to payroll
  3. Flags for written warning (3 penalties)
  4. Notifies supervisor and HR

Result: Fair, transparent, documented disciplinary action.
```

---

### **CATEGORY: Leave Management**

---

#### **8. Leave Types & Allocation**

**What It Does:**
Defines different leave categories (Annual, Sick, Emergency, Unpaid) and allocates leave balance to each employee based on policy.

**Why You Need It:**
- Implement company leave policy systematically
- Track leave entitlement per employee
- Prevent over-utilization of leave
- Comply with labor laws (e.g., minimum annual leave)

**Who Uses It:**
- HR team (configure leave types and allocations)
- Employees (view their leave balance)
- Managers (approve leave requests)

**End Goal:**
✅ **Policy compliance** - Meet legal leave requirements  
✅ **Fair allocation** - Everyone gets entitled leave  
✅ **Balance tracking** - Know available leave at any time  

**Customizations from one_fm:**
- **Custom DocTypes:**
  - `annual_leave_allocation_matrix` - Policy definition
  - `annual_leave_allocation_reduction` - Adjustments
  - `leave_allocation_tool` - Bulk allocation utility
  - `leave_transfer` - Carry-forward logic

- **Custom Fields in Leave Allocation:**
  - `pro_rate_based_on_joining_date` - Pro-ration logic
  - `employment_type` - Different allocation per type
  - `grade` - Grade-based allocation
  - `nationality` - Country-specific entitlements
  - `leave_balance_forward` - Carry-forward amount
  - `max_carry_forward` - Maximum carry forward limit

- **Override File:** `one_fm/overrides/leave_allocation.py`
- **Custom Logic:**
  - Pro-rated allocation based on joining date
  - Monthly accrual calculations
  - Automatic carry-forward at year-end
  - Grade-based entitlements
  - Nationality-based rules (Kuwait labor law)
  - Leave encashment eligibility

- **Lines of Code:** ~320 lines

**Dependencies:**
- Employee master data
- Employment contract (leave entitlement)
- Company policy configuration

**Priority:** ⭐ **HIGH** - Legal requirement in most countries

**Example Scenario:**
```
Company Policy:
- Annual Leave: 30 days/year (pro-rated monthly)
- Sick Leave: 15 days/year
- Emergency Leave: 5 days/year
- Unpaid Leave: Unlimited (unpaid)

Employee: Guard Mohammed (joined Jan 1, 2025)
Allocation as of October:
- Annual Leave: 25 days (30 × 10/12 months)
- Sick Leave: 12.5 days (15 × 10/12 months)
- Emergency Leave: 4 days (5 × 10/12 months)

Result: Employee knows exactly how much leave they have.
```

---

#### **9. Leave Application & Approval**

**What It Does:**
Allows employees to apply for leave, sends to manager for approval, updates leave balance upon approval, marks attendance accordingly.

**Why You Need It:**
- Formalize leave request process
- Ensure proper approval before absence
- Maintain leave records and history
- Prevent scheduling conflicts

**Who Uses It:**
- Employees (apply for leave)
- Managers (approve/reject)
- HR (monitor patterns, handle appeals)

**End Goal:**
✅ **Organized process** - No informal leave requests  
✅ **Proper coverage** - Manager plans for absence  
✅ **Leave history** - Complete audit trail  

**Customizations from one_fm:**
- **Custom Fields Added:**
  - `leave_balance_before` - Balance before application
  - `leave_balance_after` - Balance after application
  - `operations_site` - Site coverage planning
  - `operations_shift` - Shift coverage planning
  - `replacement_employee` - Covering employee
  - `emergency_contact` - Contact during leave
  - `travel_details` - If traveling during leave
  - `attachment` - Supporting documents
  - `mobile_number_while_on_leave` - Emergency contact

- **Override File:** `one_fm/overrides/leave_application.py`
- **Custom Logic:**
  - Real-time balance check before submission
  - Multi-level approval workflow
  - Site coverage validation
  - Shift coverage suggestions
  - Auto-attendance marking on approval
  - Email notifications (employee, manager, HR)
  - Integration with shift assignment
  - Block roster during approved leave
  - Leave calendar integration

- **Lines of Code:** ~510 lines

**Dependencies:**
- Leave allocation
- Approval workflow
- Attendance system (to mark leave days)

**Priority:** ⭐ **HIGH** - Essential for leave management

**Example Scenario:**
```
Leave Request Flow:
1. Guard Fatima applies for 3 days annual leave (Dec 20-22)
2. System checks: Does she have 3 days balance? ✓ Yes (8 days available)
3. Request sent to Site Supervisor
4. Supervisor checks: Will we have coverage? 
5. Supervisor approves request
6. System automatically:
   - Deducts 3 days from Fatima's balance (now 5 days left)
   - Marks attendance as "On Leave" for Dec 20-22
   - Notifies Fatima of approval
   - Blocks any shift assignment for those dates

Result: Leave approved, balance updated, attendance marked, coverage planned.
```

---

#### **10. Leave Encashment**

**What It Does:**
Converts unused leave days into cash payment, typically at year-end or upon resignation.

**Why You Need It:**
- Compensate employees who don't take full leave
- Comply with labor laws requiring leave payment
- Encourage leave utilization (by limiting encashment)

**Who Uses It:**
- HR team (process encashment)
- Payroll team (add to final settlement)
- Employees (request encashment)

**End Goal:**
✅ **Fair compensation** - Pay for unused leave  
✅ **Legal compliance** - Meet termination payment requirements  
✅ **Flexible benefit** - Employee choice to take cash vs. leave  

**Customizations from one_fm:**
- **Custom DocType:** `leave_encashment` (custom implementation)
- **Custom Fields:**
  - `employee` - Employee requesting encashment
  - `leave_type` - Type of leave to encash
  - `available_balance` - Current leave balance
  - `encashment_days` - Days to convert to cash
  - `encashment_amount` - Calculated amount
  - `encashment_date` - Processing date
  - `salary_slip` - Link to payroll
  - `approval_status` - Workflow status
  - `reason` - Encashment reason

- **Custom Logic:**
  - Policy validation (max days allowed)
  - Amount calculation (based on daily rate)
  - Leave balance deduction
  - Payroll integration (additional salary component)
  - Year-end vs. mid-year encashment
  - Termination settlement calculation
  - Tax implications handling

- **Location:** `one_fm/one_fm/doctype/leave_encashment/`
- **Lines of Code:** ~180 lines

**Dependencies:**
- Leave balance records
- Company policy (how many days can be encashed)
- Payroll system

**Priority:** 🟡 **MEDIUM** - Important for employee compensation

**Example Scenario:**
```
Year-End Encashment:
Employee: Guard Ali
Available Annual Leave: 10 days unused
Company Policy: Max 5 days encashment allowed

Process:
- Ali requests to encash 5 days leave
- HR approves (within policy limit)
- Daily salary: $40
- Encashment amount: $40 × 5 = $200
- Amount added to December salary
- Remaining 5 days carried forward to next year

Result: Ali gets cash for unused leave, encouraged to use remaining days.
```

---

### **CATEGORY: Payroll**

---

#### **11. Salary Structure & Components**

**What It Does:**
Defines how employee salary is calculated - base salary, allowances (transport, housing, food), deductions (tax, insurance), and benefits.

**Why You Need It:**
- Standardize salary calculation across organization
- Handle complex salary components (40+ components possible)
- Calculate overtime, bonuses, penalties automatically
- Generate detailed payslips

**Who Uses It:**
- HR team (design salary structures)
- Payroll team (process monthly payroll)
- Employees (view salary breakdown)

**End Goal:**
✅ **Transparent compensation** - Employees understand their salary  
✅ **Automated calculation** - No manual salary computation  
✅ **Flexible structures** - Different salary models for different roles  

**Customizations from one_fm:**
- **Custom Salary Components (40+ components):**
  - **Earnings:**
    - Basic Salary, Housing Allowance, Transport Allowance
    - Food Allowance, Site Allowance, Supervisor Allowance
    - Overtime (Normal/Weekend/Holiday), Bonus, Incentive
  - **Deductions:**
    - GOSI (Social Security - Kuwait), Income Tax
    - Health Insurance, Loan Deduction, Advance Deduction
    - Penalty Deduction, Uniform Charge, Accommodation Charge

- **Custom Fields in Salary Structure:**
  - `employment_type` - Different structures per type
  - `grade` - Grade-based structures
  - `nationality` - Country-specific components
  - `operations_site` - Site-specific allowances
  - `post_type` - Role-based pay
  - `ot_rate_normal` - Normal OT multiplier (1.5x)
  - `ot_rate_weekend` - Weekend OT multiplier (2x)
  - `ot_rate_holiday` - Holiday OT multiplier (2.5x)

- **Override Files:**
  - `one_fm/overrides/salary_structure.py` (~210 lines)
  - `one_fm/overrides/salary_component.py` (~150 lines)

- **Custom Logic:**
  - Auto-assignment based on employee attributes
  - Conditional component activation
  - Pro-rated calculations for new joiners
  - Site-based salary adjustments
  - Role-based pay scales

**Dependencies:**
- Employee contract details
- Attendance records (for deductions)
- Tax and compliance rules

**Priority:** ⭐ **HIGH** - Critical for payroll processing

**Example Scenario:**
```
Salary Structure: Security Guard - Grade A

Earnings:
- Basic Salary: $1,000
- Housing Allowance: $300
- Transport Allowance: $100
- Food Allowance: $50
- Overtime: Variable (based on attendance)
- Total Earnings: $1,450 + OT

Deductions:
- Social Security (GOSI): 10% of basic = $100
- Health Insurance: $30
- Penalty Deductions: Variable
- Total Deductions: $130 + Penalties

Net Salary = Earnings - Deductions

Result: Clear breakdown, easy to understand, automated monthly.
```

---

#### **12. Overtime Calculation**

**What It Does:**
Automatically calculates overtime pay based on hours worked beyond shift, applying different rates (1.5x normal, 2x for holidays/weekends).

**Why You Need It:**
- Comply with labor laws on overtime pay
- Fairly compensate extra work
- Encourage or discourage overtime (via rates)
- Accurate payroll cost tracking

**Who Uses It:**
- Payroll team (reviews OT calculations)
- Managers (approve OT hours)
- Employees (earn OT pay)

**End Goal:**
✅ **Legal compliance** - Proper OT compensation  
✅ **Cost control** - Track and manage OT expenses  
✅ **Fair pay** - Employees paid for extra hours  

**Customizations from one_fm:**
- **Custom OT Calculation Logic:**
  - Automatic detection from attendance
  - Different rates for different scenarios:
    - Normal day OT: 1.5× base rate
    - Day off OT: 2× base rate
    - Holiday OT: 2.5× base rate
    - Unscheduled work: Special rate
  
- **Custom Fields in Additional Salary:**
  - `ot_hours_normal` - Regular overtime hours
  - `ot_hours_weekend` - Weekend overtime hours
  - `ot_hours_holiday` - Holiday overtime hours
  - `ot_amount_normal` - Normal OT payment
  - `ot_amount_weekend` - Weekend OT payment
  - `ot_amount_holiday` - Holiday OT payment
  - `attendance_ref` - Link to attendance record
  - `auto_generated` - System-generated flag

- **Override File:** `one_fm/overrides/additional_salary.py`
- **Custom Logic:**
  - Hourly rate calculation (monthly salary ÷ 208 hours)
  - OT hours extraction from attendance
  - Rate application based on day type
  - Auto-creation from attendance records
  - Approval workflow for manual OT
  - Monthly OT summary
  - Cost center allocation

- **Scheduled Task:**
  - `calculate_monthly_overtime` - Runs on 25th of month
  - Auto-creates Additional Salary entries

- **Lines of Code:** ~380 lines

**Dependencies:**
- Attendance with checkin/checkout times
- Shift assignments (to know normal hours)
- OT policy configuration

**Priority:** ⭐ **HIGH** - Legal requirement

**Example Scenario:**
```
OT Policy:
- Normal OT (weekday): 1.5× hourly rate
- Weekend OT: 2× hourly rate
- Holiday OT: 2.5× hourly rate

Example:
Guard Hassan:
- Normal hourly rate: $10/hour ($1,600/month ÷ 160 hours)
- Worked Monday 6 AM - 4 PM (10 hours, shift is 8 hours)
- Overtime: 2 hours × $10 × 1.5 = $30
- Worked Friday (weekend) 6 AM - 2 PM (8 hours)
- Weekend OT: 8 hours × $10 × 2 = $160

Total OT for month: $30 + $160 = $190

Result: Accurate OT payment, employee compensated fairly.
```

---

#### **13. Payroll Processing & Payslips**

**What It Does:**
Monthly payroll run that calculates all employees' salaries, generates payslips, processes bank transfers, and creates accounting entries.

**Why You Need It:**
- Pay employees accurately and on time
- Generate payslips for employee records
- Create bank transfer files
- Record payroll expenses in accounts

**Who Uses It:**
- Payroll team (process monthly payroll)
- Finance team (verify and approve)
- Employees (receive payslips)
- Banks (process salary transfers)

**End Goal:**
✅ **Timely payment** - Salaries paid on schedule  
✅ **Accurate records** - Complete payroll documentation  
✅ **Accounting integration** - Expenses recorded properly  

**Customizations from one_fm:**
- **Custom Fields in Salary Slip:**
  - `operations_site` - Site allocation for costing
  - `project` - Project allocation
  - `penalty_amount` - Total penalties
  - `ot_hours` - Total overtime hours
  - `actual_working_days` - Days worked
  - `absent_days` - Absent days
  - `leave_days` - Paid leave days
  - `unpaid_leave_days` - Unpaid leave days
  - `bank_account_no` - Employee bank account
  - `iban` - IBAN for transfer
  - `payment_method` - Cash/Bank/Check

- **Custom Fields in Payroll Entry:**
  - `site_wise_payroll` - Site-based payroll
  - `project_wise_payroll` - Project-based payroll
  - `process_attendance` - Auto-fetch attendance
  - `include_penalties` - Include penalty deductions
  - `include_overtime` - Include OT payments
  - `payment_approval_status` - Finance approval
  - `bank_file_generated` - Bank file flag

- **Override Files:**
  - `one_fm/overrides/salary_slip.py` (~650 lines)
  - `one_fm/overrides/payroll_entry.py` (~520 lines)

- **Custom Logic:**
  - Attendance-based salary calculation
  - Absent day deductions (1/30th of monthly salary)
  - Penalty integration
  - OT addition
  - Site/project cost allocation
  - Bank file generation (CSV/Excel)
  - Payment voucher creation
  - Accounting entries (by site/project)
  - Email payslips automatically
  - SMS notification on salary credit

- **Custom Reports:**
  - Site-wise payroll summary
  - Project-wise labor cost
  - Department-wise payroll
  - Payroll variance analysis

- **Lines of Code:** ~1,170 lines total

**Dependencies:**
- Attendance records (full month)
- Leave records
- Salary structures
- Bank account details

**Priority:** ⭐ **HIGH** - Core business function

**Example Scenario:**
```
Monthly Payroll Process (January 2025):

Step 1: System collects data
- 150 employees
- Attendance records (Jan 1-31)
- Leave applications
- Overtime records
- Penalty records

Step 2: Calculate salaries
- Apply salary structures
- Add overtime payments
- Deduct penalties
- Deduct taxes and insurance
- Calculate net pay

Step 3: Generate outputs
- 150 payslips (PDF)
- Bank transfer file (CSV)
- Payroll summary report
- Accounting entries

Step 4: Process payments
- Upload bank file
- Salaries credited
- Payslips emailed to employees

Result: Everyone paid correctly, records maintained, accounts updated.
```

---

## 🏢 OPERATIONS FEATURES

### **CATEGORY: Site Management**

---

#### **14. Operations Sites**

**What It Does:**
Manages all client sites where your company provides services - locations, client details, service requirements, SLAs, billing information.

**Why You Need It:**
- Centralized database of all service locations
- Track site-specific requirements and contracts
- Assign employees to specific sites
- Generate site-wise reports and billing

**Who Uses It:**
- Operations Manager (configure sites)
- Site Supervisors (manage site operations)
- HR team (assign employees to sites)
- Finance team (billing and invoicing)

**End Goal:**
✅ **Organized operations** - Know all service locations  
✅ **Site-specific management** - Each site has unique requirements  
✅ **Accurate billing** - Invoice based on site contracts  

**Customizations from one_fm:**
- **Custom DocType:** `operations_site` (77 doctypes in operations module)
- **Custom Fields:**
  - `site_name` - Client site name
  - `site_code` - Unique identifier
  - `client` - Client company
  - `site_location` - Full address
  - `latitude` / `longitude` - GPS coordinates
  - `geofence_radius` - Checkin boundary (meters)
  - `contract_start_date` - Contract start
  - `contract_end_date` - Contract end
  - `contract_value` - Monthly contract amount
  - `billing_type` - Fixed/Per-head/Hourly
  - `sla_requirements` - Service level agreements
  - `minimum_staff` - Min staff requirement
  - `shift_pattern` - 24/7 or specific hours
  - `contact_person` - Client contact
  - `emergency_contact` - Emergency number
  - `site_supervisor` - Assigned supervisor
  - `equipment_required` - Equipment list
  - `reporting_frequency` - Daily/Weekly/Monthly

- **Related DocTypes:**
  - `operations_shift` - Shifts at site
  - `operations_role` - Roles/posts at site
  - `site_location` - Sub-locations within site
  - `post_type` - Position types
  - `site_service` - Services provided

- **Custom Logic:**
  - Site hierarchy (parent-child sites)
  - Geofencing for checkin validation
  - SLA tracking and alerts
  - Equipment assignment tracking
  - Site-wise reporting
  - Contract renewal alerts
  - Staff allocation validation (min/max)
  - Client portal access per site

- **Location:** `one_fm/operations/doctype/operations_site/`
- **Lines of Code:** ~420 lines

**Dependencies:**
- Client master data
- Contract details
- Location/GPS coordinates

**Priority:** ⭐ **HIGH** - Foundation for operations

**Example Scenario:**
```
Site: ABC Shopping Mall

Details:
- Client: ABC Real Estate Company
- Location: Downtown, 123 Main Street
- Contract: 24/7 Security + Cleaning
- SLA: 4 guards at all times, 2 cleaners per shift
- Billing: $10,000/month
- Start Date: Jan 1, 2025
- Contact Person: Mr. Ahmed (Manager)
- Emergency Contact: +971-xxx-xxxx

Assignments:
- Morning Shift: 4 guards, 2 cleaners
- Evening Shift: 4 guards, 2 cleaners
- Night Shift: 4 guards, 1 cleaner

Equipment:
- 2 walkie-talkies
- 1 metal detector
- Cleaning supplies

Result: Complete site information in one place, easy to manage.
```

---

#### **15. Operations Roster**

**What It Does:**
Creates detailed shift schedules for all sites, assigning specific employees to specific posts/roles at specific times.

**Why You Need It:**
- Plan workforce allocation across multiple sites
- Ensure adequate coverage at all locations
- Optimize employee utilization
- Meet SLA requirements (minimum staff per site)

**Who Uses It:**
- Operations Manager (create rosters)
- Site Supervisors (view site roster)
- Employees (check their schedule)

**End Goal:**
✅ **Optimal coverage** - Right people at right places  
✅ **Cost efficiency** - No overstaffing or understaffing  
✅ **SLA compliance** - Meet contracted service levels  

**Customizations from one_fm:**
- **Custom DocType:** `operations_roster` (complex roster management)
- **Custom Fields:**
  - `site` - Operations site
  - `roster_type` - Basic/Over-Time/Emergency
  - `from_date` / `to_date` - Roster period
  - `shift` - Default shift
  - `day_off_category` - Day off pattern (e.g., Friday)
  - `roster_employee` (Child Table):
    - `employee` - Assigned employee
    - `operations_role` - Role/post
    - `shift` - Specific shift
    - `from_date` / `to_date` - Assignment dates
    - `day_off` - Day off day
    - `roster_days` (Grand-child table) - Daily assignments

- **Related DocTypes:**
  - `roster_employee` - Employee roster line
  - `roster_day` - Individual day assignment
  - `employee_schedule` - Generated schedules
  - `shift_schedule` - Shift templates

- **Custom Logic:**
  - Auto-roster generation from templates
  - Rotation logic (morning → evening → night)
  - Day off rotation (fair distribution)
  - Coverage validation (min staff per shift)
  - Conflict detection (no double-booking)
  - Mass roster updates
  - Roster publishing (notify employees)
  - Shift pattern templates
  - Monthly roster approval workflow
  - Integration with shift assignment
  - Integration with attendance

- **Custom Features:**
  - Drag-and-drop roster builder
  - Visual calendar view
  - Bulk employee assignment
  - Roster copy function (month-to-month)
  - Employee availability check
  - Skills-based auto-assignment

- **Location:** `one_fm/operations/doctype/operations_roster/`
- **Lines of Code:** ~680 lines

**Dependencies:**
- Operations sites configured
- Employee availability
- Shift types
- Contract requirements (minimum staff)

**Priority:** ⭐ **HIGH** - Core planning function

**Example Scenario:**
```
Weekly Roster: Week of Oct 20-26, 2025

Site A (Shopping Mall):
Monday:
- Morning: Guard Ahmed, Guard Fatima, Guard Hassan, Guard Sarah
- Evening: Guard Ali, Guard John, Guard Lisa, Guard David
- Night: Guard Mohammed, Guard Maria, Guard Omar, Guard Zainab

Site B (Office Building):
Monday:
- Morning: Guard Khalid, Guard Layla
- Evening: Guard Youssef, Guard Noor

Rotation:
- Each guard works 6 days, 1 day off per week
- Rotates between morning/evening/night over 3 weeks
- Never double-booked

Result: Fair schedule, full coverage, happy employees and clients.
```

---

#### **16. Post Types & Post Management**

**What It Does:**
Defines specific job positions/posts at each site (Gate Guard, Patrol Guard, Reception, Supervisor) with role descriptions and requirements.

**Why You Need It:**
- Clearly define role responsibilities
- Assign right person to right post
- Track post-specific costs (different pay for different posts)
- Client reporting (show who did what)

**Who Uses It:**
- Operations Manager (define posts)
- Site Supervisor (assign employees to posts)
- HR team (match skills to post requirements)
- Clients (see service delivery details)

**End Goal:**
✅ **Clear responsibilities** - Everyone knows their role  
✅ **Skill matching** - Right person for each post  
✅ **Transparent billing** - Client sees what they're paying for  

**Customizations from one_fm:**
- **Custom DocTypes:**
  - `post_type` - Master post/role types
  - `post` - Actual post at site
  - `operations_role` - Role assignment

- **Custom Fields in Post Type:**
  - `post_name` - Role name (e.g., "Main Gate Guard")
  - `post_code` - Short code
  - `post_template` - Job description template
  - `skills_required` (Child Table):
    - `skill` - Required skill
    - `proficiency` - Required level
  - `pay_rate` - Hourly rate for this post
  - `billing_rate` - Client billing rate
  - `equipment_required` (Child Table):
    - `item` - Equipment needed
    - `quantity` - Number required
  - `responsibilities` - Detailed JD
  - `reports_to` - Reporting structure

- **Custom Fields in Post (Site-specific):**
  - `operations_site` - Site location
  - `post_type` - Reference to post type
  - `number_of_posts` - How many positions
  - `shift_hours` - Working hours
  - `active_status` - Active/Inactive
  - `start_date` / `end_date` - Post duration

- **Custom Logic:**
  - Post-based roster generation
  - Skills matching for assignment
  - Pay rate vs. billing rate tracking (margin analysis)
  - Equipment auto-assignment to post
  - Post coverage reports
  - Vacant post alerts
  - Post rotation schedules

- **Integration:**
  - Links to roster (assign by post)
  - Links to attendance (track by post)
  - Links to billing (invoice by post)
  - Links to payroll (cost by post)

- **Location:** `one_fm/operations/doctype/post*/`
- **Lines of Code:** ~320 lines total

**Dependencies:**
- Operations sites
- Job descriptions
- Employee skills database

**Priority:** 🟡 **MEDIUM** - Improves operations quality

**Example Scenario:**
```
Site: Corporate Office Building

Post Types:
1. Main Gate Guard
   - Requirements: 2+ years experience, English speaking
   - Responsibilities: Check IDs, visitor log, gate control
   - Pay Rate: $12/hour

2. Patrol Guard
   - Requirements: Physical fitness, driver's license
   - Responsibilities: Hourly building rounds, report incidents
   - Pay Rate: $11/hour

3. CCTV Operator
   - Requirements: Technical training, alert
   - Responsibilities: Monitor cameras, log events
   - Pay Rate: $13/hour

4. Supervisor
   - Requirements: 5+ years, leadership skills
   - Responsibilities: Oversee team, client liaison
   - Pay Rate: $15/hour

Roster:
- Main Gate: Guard Ahmed (qualified, English speaker)
- Patrol: Guard Hassan (has driver's license)
- CCTV: Guard Fatima (trained on systems)
- Supervisor: Guard Ali (senior)

Result: Skill-matched assignments, quality service delivery.
```

---

### **CATEGORY: Checkpoints & Patrols**

---

#### **17. Checkpoints & Patrol Routes**

**What It Does:**
Defines specific physical locations (checkpoints) that guards must visit during patrols, with expected visit frequency and scan requirements.

**Why You Need It:**
- Ensure guards patrol entire site
- Prove service delivery to clients
- Detect missed patrols immediately
- Create audit trail of patrol activity

**Who Uses It:**
- Operations Manager (define checkpoints)
- Guards (scan checkpoints during patrol)
- Site Supervisor (monitor patrol compliance)
- Clients (review patrol reports)

**End Goal:**
✅ **Service verification** - Proof patrols are happening  
✅ **Client confidence** - Transparent service delivery  
✅ **Quality control** - Catch security gaps  

**Customizations from one_fm:**
- **Custom DocTypes (15+ checkpoint-related):**
  - `checkpoint` - Master checkpoint definition
  - `checkpoint_route` - Patrol routes
  - `checkpoint_assignment` - Guard-route assignment
  - `checkpoint_assignment_scan` - Scan records
  - `patrol_routes` - Route templates

- **Custom Fields in Checkpoint:**
  - `checkpoint_name` - Descriptive name
  - `checkpoint_code` - Unique QR/NFC code
  - `site` - Operations site
  - `location` - Specific location at site
  - `latitude` / `longitude` - GPS coordinates
  - `scan_type` - QR/NFC/Manual
  - `visit_frequency` - How often to scan (hourly/2hrs/etc.)
  - `critical` - Critical checkpoint flag
  - `active` - Active status

- **Custom Fields in Checkpoint Scan:**
  - `employee` - Guard who scanned
  - `checkpoint` - Checkpoint scanned
  - `scan_time` - Actual scan timestamp
  - `expected_time` - Scheduled scan time
  - `late_by` - Minutes late
  - `latitude` / `longitude` - GPS at scan
  - `photo` - Photo evidence
  - `notes` - Guard notes
  - `skip_reason` - If missed, why
  - `verified_by` - Supervisor verification

- **Custom Fields in Checkpoint Route:**
  - `route_name` - Route name
  - `site` - Operations site
  - `shift` - Which shift uses this route
  - `checkpoints` (Child Table):
    - `checkpoint` - Checkpoint in route
    - `sequence` - Order of visit
    - `expected_time` - When to scan
  - `total_distance` - Route distance
  - `estimated_duration` - Time to complete

- **Custom Logic:**
  - Route assignment to guards
  - Real-time scan tracking
  - Missed checkpoint alerts
  - Supervisor notifications
  - GPS verification (within 50m of checkpoint)
  - Photo requirement enforcement
  - Route completion tracking
  - Client reporting (daily patrol reports)
  - Heatmap of patrol coverage
  - Exception reporting (missed/late scans)

- **Mobile App Integration:**
  - QR scanner
  - NFC reader
  - GPS location capture
  - Photo capture
  - Offline scan storage

- **Reports:**
  - Daily patrol compliance
  - Missed checkpoint summary
  - Guard performance by scans
  - Site coverage heatmap

- **Location:** `one_fm/operations/doctype/checkpoint*/`
- **Lines of Code:** ~890 lines total (15 doctypes)

**Dependencies:**
- Physical checkpoint markers (NFC tags, QR codes)
- Mobile app for scanning
- Operations sites

**Priority:** 🟡 **MEDIUM** - High value for security operations

**Example Scenario:**
```
Site: Industrial Warehouse

Checkpoint Route (12 checkpoints):
1. Main Gate - Every hour
2. Warehouse A Entrance - Every 2 hours
3. Warehouse B Entrance - Every 2 hours
4. Loading Dock - Every hour
5. Perimeter North - Every 3 hours
6. Perimeter East - Every 3 hours
7. Perimeter South - Every 3 hours
8. Perimeter West - Every 3 hours
9. Office Block - Every 2 hours
10. Generator Room - Every 4 hours
11. Parking Area - Every 2 hours
12. Back Exit - Every hour

Night Shift Patrol:
- Guard starts at 10 PM
- Must complete full route every 3 hours
- Scans each checkpoint via mobile app
- System logs: Time, GPS location, Guard name

Alert:
- If checkpoint missed: Immediate supervisor alert
- If route incomplete: Email to Operations Manager

Result: Complete patrol coverage, verified service delivery.
```

---

### **CATEGORY: Cleaning & Maintenance**

---

#### **18. Cleaning Schedules & Task Management**

**What It Does:**
Creates cleaning schedules with specific tasks, frequencies, assigned cleaners, and quality checklists for each site/area.

**Why You Need It:**
- Ensure consistent cleaning standards
- Track task completion
- Manage cleaning supplies/consumables
- Generate cleaning reports for clients

**Who Uses It:**
- Operations Manager (create schedules)
- Cleaning Supervisor (assign tasks)
- Cleaners (view assigned tasks)
- Clients (review cleaning reports)

**End Goal:**
✅ **Quality assurance** - Consistent cleaning standards  
✅ **Accountability** - Know who cleaned what and when  
✅ **Client satisfaction** - Transparent cleaning reports  

**Customizations from one_fm:**
- **Custom DocTypes:**
  - `cleaning_master_list` - Cleaning task catalog
  - `cleaning_shift_plan` - Shift-based cleaning plan
  - `cleaning_master_tasks` - Task definitions
  - `cleaning_consumables` - Supplies tracking
  - `cleaning_object_category` - Area categories

- **Custom Fields:**
  - `site` - Operations site
  - `shift` - Cleaning shift
  - `area` - Area to clean
  - `task_list` (Child Table):
    - `task` - Cleaning task
    - `frequency` - Daily/Weekly/Monthly
    - `time` - Scheduled time
    - `duration` - Time required (mins)
    - `cleaner` - Assigned cleaner
  - `consumables` (Child Table):
    - `item` - Cleaning supply
    - `quantity` - Amount needed
  - `checklist_template` - Quality checklist
  - `completion_status` - Pending/In Progress/Completed

- **Custom Logic:**
  - Auto-task assignment based on shift
  - Consumables consumption tracking
  - Quality checklist completion
  - Photo evidence requirement
  - Supervisor sign-off
  - Client satisfaction rating
  - Before/after photos
  - Task completion tracking via mobile

- **Location:** `one_fm/operations/doctype/cleaning*/`
- **Lines of Code:** ~450 lines

**Dependencies:**
- Operations sites
- Cleaning task library
- Employee assignments

**Priority:** 🟡 **MEDIUM** - Important for FM companies

**Example Scenario:**
```
Site: Office Building (5 floors)

Daily Cleaning Schedule:

Floor 1 (Lobby & Reception):
- Vacuum carpets - 7:00 AM (Cleaner Maria)
- Mop floors - 7:30 AM (Cleaner Maria)
- Clean glass doors - 8:00 AM (Cleaner Maria)
- Empty trash bins - 8:30 AM (Cleaner Maria)
- Sanitize washrooms - 9:00 AM (Cleaner Sarah)

Floors 2-5 (Offices):
- Each floor assigned to specific cleaner
- Vacuum, dust, trash collection - Daily
- Washroom cleaning - 3 times/day
- Deep cleaning - Weekly (Fridays)

Quality Checklist:
☐ All trash bins emptied
☐ Floors vacuumed/mopped
☐ Washrooms sanitized
☐ Glass surfaces cleaned
☐ Supplies restocked

Tracking:
- Cleaners check off tasks via mobile app
- Supervisor spot-checks quality
- Client receives daily completion report

Result: Clean facility, happy client, documented service.
```

---

## 👔 RECRUITMENT FEATURES

### **CATEGORY: Hiring & Onboarding**

---

#### **19. Job Opening & Applicant Management**

**What It Does:**
Post job openings, receive applications, track candidates through hiring stages, store resumes and interview notes.

**Why You Need It:**
- Organize recruitment process
- Track all candidates in one system
- Collaborate on candidate evaluation
- Maintain hiring history

**Who Uses It:**
- HR team (post jobs, review applications)
- Hiring managers (interview, evaluate)
- Candidates (apply for positions)

**End Goal:**
✅ **Efficient hiring** - Find right candidates faster  
✅ **Organized process** - Track each applicant's status  
✅ **Better decisions** - Complete candidate information  

**Dependencies:**
- Job descriptions
- Company careers page/portal
- Email integration

**Priority:** ⭐ **HIGH** - Essential for growing company

**Example Scenario:**
```
Job Opening: Security Guard - 10 Positions

Recruitment Flow:
1. Job posted on company website + job boards
2. 50 applications received in 2 weeks

Application Tracking:
- 50 Applications Received
  ↓ Resume screening (HR)
- 30 Shortlisted
  ↓ Phone screening
- 20 Invited for Interview
  ↓ Interview round 1
- 15 Passed to Round 2
  ↓ Skills assessment
- 12 Final Candidates
  ↓ Background check
- 10 Offers Made
  ↓ Acceptance
- 10 Hired

System Features:
- Resume storage
- Interview notes
- Scoring/rating
- Rejection emails (automated)
- Offer letters (templated)

Result: Organized hiring, quality candidates, efficient process.
```

---

#### **20. Interview Scheduling & Management**

**What It Does:**
Schedule interviews with candidates, assign interviewers, share interview scorecards, collect feedback in structured format.

**Why You Need It:**
- Coordinate multiple interviewers
- Standardize candidate evaluation
- Compare candidates objectively
- Make data-driven hiring decisions

**Who Uses It:**
- HR team (schedule interviews)
- Hiring managers (conduct interviews)
- Interview panel (provide feedback)

**End Goal:**
✅ **Fair evaluation** - Consistent criteria for all candidates  
✅ **Collaboration** - Multiple perspectives on candidates  
✅ **Faster decisions** - Organized feedback collection  

**Dependencies:**
- Candidate database
- Calendar integration
- Interview scorecard templates

**Priority:** 🟡 **MEDIUM** - Improves hiring quality

**Example Scenario:**
```
Interview Process: Security Supervisor Position

Candidate: Ahmed Hassan

Round 1: Phone Screening (30 mins)
- Interviewer: HR Manager
- Questions: Experience, availability, salary expectations
- Scorecard: 8/10 - Proceed to next round

Round 2: Technical Interview (45 mins)
- Interviewer: Operations Manager
- Questions: Security protocols, emergency handling, team management
- Scorecard:
  * Security knowledge: 9/10
  * Leadership skills: 7/10
  * Communication: 8/10
  * Overall: 8/10 - Proceed

Round 3: Final Interview (1 hour)
- Interviewers: Site Supervisor + HR
- Questions: Cultural fit, situational responses, growth plans
- Scorecard:
  * Cultural fit: 9/10
  * Problem-solving: 8/10
  * Motivation: 9/10
  * Overall: 8.7/10 - Recommend hire

Decision: Offer extended

Result: Structured evaluation, quality hire, documented decision.
```

---

#### **21. Employee Onboarding Workflows**

**What It Does:**
Guides new hires through onboarding process - document collection, training completion, equipment issuance, system access setup.

**Why You Need It:**
- Ensure nothing is missed in onboarding
- Create consistent new hire experience
- Track onboarding completion
- Faster time-to-productivity

**Who Uses It:**
- HR team (manage onboarding)
- IT team (system access)
- Operations (equipment issuance)
- New employees (complete tasks)

**End Goal:**
✅ **Complete onboarding** - No missed steps  
✅ **Great first impression** - Organized welcome  
✅ **Quick ramp-up** - Employee productive faster  

**Dependencies:**
- Employee master record
- Document templates
- Equipment inventory
- Training materials

**Priority:** 🟡 **MEDIUM** - Improves employee experience

**Example Scenario:**
```
Onboarding Checklist: New Security Guard

Pre-Joining (Before Day 1):
☐ Background check completed
☐ Medical fitness certificate received
☐ Offer letter signed
☐ Employee file created in system

Day 1:
☐ Welcome session (HR)
☐ Collect documents (passport, ID, certificates)
☐ Issue employee ID card
☐ Issue uniform (2 sets)
☐ Issue equipment (walkie-talkie, flashlight)
☐ System access created (mobile app login)
☐ Bank details collected

Week 1:
☐ Company orientation training (2 hours)
☐ Security protocols training (4 hours)
☐ Safety training (2 hours)
☐ Site familiarization tour
☐ Shadow experienced guard (3 shifts)

Week 2:
☐ First solo shift (supervised)
☐ Checkpoint scanning training
☐ Incident reporting training
☐ Meet site client contact

End of Month 1:
☐ Performance review meeting
☐ Confirm permanent employment
☐ Employee survey (feedback on onboarding)

Tracking:
- HR sees completion percentage
- Alerts for overdue tasks
- New hire sees their progress

Result: Smooth onboarding, confident employee, nothing missed.
```

---

## 🏠 ACCOMMODATION FEATURES

### **CATEGORY: Housing Management**

---

#### **22. Accommodation Unit Management**

**What It Does:**
Manages company-provided employee housing - buildings, rooms, beds, occupancy tracking, maintenance.

**Why You Need It:**
- Track housing inventory
- Assign accommodation to employees
- Monitor occupancy rates
- Manage housing costs

**Who Uses It:**
- HR team (allocate accommodation)
- Accommodation manager (manage facilities)
- Employees (view their assigned room)
- Finance (track housing costs)

**End Goal:**
✅ **Organized housing** - Know all available units  
✅ **Fair allocation** - Transparent room assignment  
✅ **Cost tracking** - Monitor housing expenses  

**Dependencies:**
- Employee records
- Property/building details
- Maintenance schedules

**Priority:** 🟡 **MEDIUM** - Critical if you provide housing

**Example Scenario:**
```
Company Housing: Labor Camp

Inventory:
- 5 Buildings
- 100 Rooms total
- 400 Beds (4 beds per room)

Current Status:
- Occupied: 350 beds (87.5%)
- Available: 50 beds
- Under Maintenance: 0 beds

Room Assignment:
Building A, Room 101:
- Bed 1: Ahmed Hassan (Guard)
- Bed 2: Mohammed Ali (Guard)
- Bed 3: Khalid Omar (Cleaner)
- Bed 4: Youssef Said (Guard)

Facilities:
- Shared kitchen per floor
- 2 bathrooms per room
- AC, WiFi included
- Laundry facility

Tracking:
- Check-in/check-out dates
- Damage reports
- Maintenance requests
- Utility consumption

Result: Organized housing, happy employees, cost control.
```

---

#### **23. Accommodation Inspection & Quality**

**What It Does:**
Regular inspection of accommodation units with quality checklists, issue tracking, and maintenance follow-up.

**Why You Need It:**
- Maintain accommodation standards
- Ensure health and safety compliance
- Track and fix issues quickly
- Employee satisfaction

**Who Uses It:**
- Accommodation manager (conduct inspections)
- Maintenance team (fix issues)
- HR (monitor living conditions)
- Employees (report issues)

**End Goal:**
✅ **Quality living** - Clean, safe accommodation  
✅ **Compliance** - Meet labor camp regulations  
✅ **Employee welfare** - Happy, healthy workforce  

**Dependencies:**
- Accommodation unit database
- Inspection checklist templates
- Maintenance workflow

**Priority:** 🔴 **LOW** - Nice to have for quality management

**Example Scenario:**
```
Monthly Inspection: Building A

Inspection Checklist:
☐ Room cleanliness
☐ Bathroom sanitation
☐ AC functioning
☐ Electrical safety
☐ Fire safety equipment
☐ Bed condition
☐ Windows/doors
☐ Pest control
☐ Water supply
☐ Ventilation

Room 101 Inspection Results:
✅ Overall Clean
❌ AC not cooling properly - Maintenance ticket created
✅ Bathroom sanitized
❌ 1 bed frame broken - Replacement ordered
✅ Fire extinguisher present and valid
✅ No pest issues

Actions Taken:
- AC repair scheduled (next day)
- New bed ordered (2-day delivery)
- Follow-up inspection in 1 week

Employee Feedback:
- Satisfaction survey sent after repairs
- 4.5/5 rating received

Result: Issues fixed quickly, quality maintained, employees happy.
```

---

## 📋 COMPLIANCE FEATURES (Kuwait-Specific)

### **CATEGORY: Government Relations**

---

#### **24. PACI Integration & Civil ID Management**

**What It Does:**
Integrates with Kuwait's Public Authority for Civil Information (PACI) to validate employee Civil IDs, track expiry, auto-update employee data.

**Why You Need It:**
- Legal requirement in Kuwait
- Verify employee identity
- Track document expiry
- Auto-update employee information

**Who Uses It:**
- HR team (manage Civil IDs)
- Employees (provide Civil ID)
- Government compliance officer

**End Goal:**
✅ **Legal compliance** - Meet PACI requirements  
✅ **Identity verification** - Confirm employee identity  
✅ **Document tracking** - Never miss Civil ID renewal  

**Dependencies:**
- PACI API access
- Employee Civil ID numbers
- Government compliance license

**Priority:** ⭐ **HIGH** (if operating in Kuwait) / 🔴 **LOW** (other regions)

**Example Scenario:**
```
Employee: Ahmed Hassan
Civil ID: 12345678901234

PACI Integration:
1. HR enters Civil ID in system
2. System connects to PACI database
3. Retrieves employee data:
   - Full Name: Ahmed Hassan Mohammed
   - Date of Birth: 15-Jan-1990
   - Nationality: Egyptian
   - Expiry Date: 30-Dec-2025
4. Auto-populates employee record
5. Sets reminder: 30 days before expiry

Expiry Alert (Dec 1, 2025):
- Email to HR: "Ahmed's Civil ID expires in 30 days"
- Email to Ahmed: "Please renew your Civil ID"
- Workflow initiated: Document renewal process

Result: Compliant operations, no expired documents, automated tracking.
```

**⚠️ Regional Note:** Only needed for Kuwait operations. Skip for other regions.

---

## 🚗 FLEET FEATURES

### **CATEGORY: Vehicle Management**

---

#### **25. Vehicle Fleet Management**

**What It Does:**
Manages company vehicles - registration, insurance, maintenance schedules, fuel tracking, driver assignments.

**Why You Need It:**
- Track all company vehicles
- Schedule preventive maintenance
- Monitor fuel consumption
- Ensure insurance and registration validity

**Who Uses It:**
- Fleet manager (manage vehicles)
- Drivers (assigned vehicles)
- Finance team (track costs)
- Maintenance team (service vehicles)

**End Goal:**
✅ **Asset protection** - Well-maintained vehicles  
✅ **Cost control** - Monitor fuel and maintenance costs  
✅ **Compliance** - Valid registration and insurance  

**Dependencies:**
- Vehicle purchase/lease records
- Driver database
- Maintenance service providers

**Priority:** 🟡 **MEDIUM** - Important if you have fleet

**Example Scenario:**
```
Company Fleet: 20 Vehicles

Vehicle: Toyota Hilux (Plate: ABC-1234)
- Type: Pickup Truck
- Year: 2023
- Use: Site supervision, equipment transport
- Assigned Driver: Mohammed Ali

Tracking:
- Registration Expiry: 15-Mar-2026
- Insurance Expiry: 30-Jun-2025
- Last Service: 15-Oct-2025 (18,500 km)
- Next Service: 15-Jan-2026 (20,000 km or 3 months)

Fuel Consumption:
- Oct 2025: 450 liters ($315)
- Average: 12 km/liter
- Monthly cost: $315

Maintenance History:
- Oil change: 15-Oct-2025 - $80
- Tire rotation: 15-Jul-2025 - $40
- Brake pads: 10-Apr-2025 - $150

Alerts:
- Insurance expires in 60 days (alert sent)
- Service due in 3 months (reminder set)

Result: Well-maintained fleet, controlled costs, no expired documents.
```

---

## 📦 PROCUREMENT FEATURES

### **CATEGORY: Purchase Management**

---

#### **26. Purchase Request & Approval Workflow**

**What It Does:**
Formalize purchase requests from departments, route through approval workflow, convert to purchase orders after approval.

**Why You Need It:**
- Control spending through approvals
- Budget compliance
- Track who requested what
- Prevent unauthorized purchases

**Who Uses It:**
- Department managers (request purchases)
- Approvers (review and approve)
- Procurement team (process orders)
- Finance team (budget monitoring)

**End Goal:**
✅ **Spending control** - Only approved purchases  
✅ **Budget management** - Stay within budgets  
✅ **Audit trail** - Complete purchase history  

**Dependencies:**
- Budget allocation
- Approval hierarchy
- Item master database

**Priority:** 🟡 **MEDIUM** - Important for cost control

**Example Scenario:**
```
Purchase Request Flow:

Requestor: Site Supervisor
Need: 10 walkie-talkies for new site
Estimated Cost: $1,500

Step 1: Request Created
- Items: 10× Motorola Walkie-Talkies
- Unit Price: $150
- Total: $1,500
- Justification: "New site opening, need communication equipment"
- Urgency: Normal

Step 2: Department Approval
- Operations Manager reviews
- Checks: Do we really need 10?
- Approves: Yes, new site requires this

Step 3: Budget Approval
- Finance Manager checks budget
- Security Equipment Budget: $5,000 remaining
- Approves: Within budget

Step 4: Procurement
- Procurement team receives approved request
- Creates RFQ (Request for Quotation)
- Gets quotes from 3 suppliers
- Selects best price + quality

Step 5: Purchase Order
- PO created for $1,400 (negotiated price)
- Sent to supplier
- Delivery: 5 days

Step 6: Receipt
- Items received at warehouse
- Quality checked
- Issued to site

Result: Controlled spending, proper approvals, audit trail maintained.
```

---

## 🎯 FEATURE PRIORITY SUMMARY

### **Must-Have (Phase 1) - HIGH Priority:**
1. ⭐ Shift Types & Shift Assignment
2. ⭐ Employee Checkin/Checkout
3. ⭐ Attendance Tracking
4. ⭐ Leave Management (Basic)
5. ⭐ Operations Sites
6. ⭐ Basic Roster

### **Should-Have (Phase 2) - MEDIUM Priority:**
7. 🟡 Shift Requests
8. 🟡 Penalty Management
9. 🟡 Operations Roster (Advanced)
10. 🟡 Post Management
11. 🟡 Checkpoints & Patrols
12. 🟡 Job Openings & Hiring
13. 🟡 Onboarding Workflows

### **Nice-to-Have (Phase 3+) - LOW Priority:**
14. 🔴 Leave Encashment
15. 🔴 Accommodation Management
16. 🔴 Fleet Management
17. 🔴 Cleaning Schedules
18. 🔴 Interview Management
19. 🔴 Accommodation Inspection
20. 🔴 PACI Integration (Kuwait only)

---

## 💡 How to Use This Guide for Migration

### **Decision Framework:**

For each feature, ask:
1. **Do we need this?** (Based on your business model)
2. **When do we need it?** (Phase 1, 2, 3, or skip)
3. **What's the effort?** (Check implementation time)
4. **What's the value?** (Check end goal and business impact)

### **Example Decision Process:**

**Feature: Checkpoint Scanning**

1. ✅ **Need it?** Yes - We provide security services
2. 📅 **When?** Phase 2 - Not critical for MVP, but important for service quality
3. ⏱️ **Effort?** Medium - Need mobile app, checkpoint markers, backend
4. 💰 **Value?** High - Proves service delivery, increases client confidence

**Decision:** Include in Phase 2 (Weeks 7-16)

---

## 📞 Questions to Guide Your Selection

### **For HR Features:**
- Do you have shift-based operations? → Need shift management
- Do you pay overtime? → Need OT calculation
- Do you have leave policies? → Need leave management
- Complex salary structures? → Need payroll module

### **For Operations Features:**
- Multiple service locations? → Need site management
- Need to prove service delivery? → Need checkpoints
- Complex scheduling? → Need advanced roster
- Cleaning services? → Need cleaning module

### **For Other Features:**
- Provide employee housing? → Need accommodation module
- Company vehicles? → Need fleet management
- Growing fast? → Need recruitment module
- Operating in Kuwait? → Need GRD/PACI modules

---

*This guide helps you understand not just WHAT each feature does, but WHY you need it and WHEN to implement it during migration.*

**Next Step:** Review this guide and mark which features are must-have for your business! 🎯
