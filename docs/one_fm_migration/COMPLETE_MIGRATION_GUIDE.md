# Complete Migration Guide: one_fm → frappe_ticktix

**Version:** 1.0  
**Date:** October 20, 2025  
**Status:** Planning Phase  
**Approach:** Build Fresh (Option 1)

---

## 📋 Table of Contents

1. [Executive Summary](#executive-summary)
2. [Project Context](#project-context)
3. [Why Not Install one_fm Directly?](#why-not-install-onefm-directly)
4. [Complete Feature Inventory](#complete-feature-inventory)
5. [Migration Architecture](#migration-architecture)
6. [Implementation Strategy](#implementation-strategy)
7. [Phase-by-Phase Plan](#phase-by-phase-plan)
8. [Detailed Implementation Guide](#detailed-implementation-guide)
9. [Testing Strategy](#testing-strategy)
10. [Timeline & Resources](#timeline--resources)

---

## 🎯 Executive Summary

### **Mission**
Migrate facility management features from **one_fm** (500+ doctypes) to **frappe_ticktix** using a clean plugin architecture, ensuring maintainability and scalability.

### **Current State**
- ✅ **frappe_ticktix:** Authentication + Branding plugins operational
- 📦 **one_fm:** 36 modules, 468 doctypes, cannot install due to compatibility issues
- 🎯 **Goal:** Incremental feature migration maintaining plugin architecture

### **Chosen Approach**
**Option 1: Build Fresh in frappe_ticktix**
- Extract features from one_fm
- Rebuild with plugin architecture
- Test incrementally
- No compatibility issues

### **Timeline**
- **MVP:** 3 months (HR Core + Operations Core)
- **Core System:** 6 months (Full operations capability)
- **Complete System:** 9-12 months (All features)

---

## 🏢 Project Context

### **frappe_ticktix Overview**
**Purpose:** Comprehensive Facility Management System  
**Framework:** Frappe v15 / ERPNext  
**Architecture:** Plugin-based modular system

**Existing Plugins:**
- ✅ `plugins/authentication/` - TickTix OAuth/JWT integration
- ✅ `plugins/branding/` - Dynamic logo management
- 🔄 `plugins/hr/` - (To be built)
- 🔄 `plugins/operations/` - (To be built)
- 🔄 `plugins/accommodation/` - (To be built)

### **one_fm Overview**
**Purpose:** Comprehensive Facility Management System (Kuwait-focused)  
**Size:** 36 modules, ~468 doctypes  
**Issue:** Cannot install due to lending app compatibility

**Key Modules:**
1. **one_fm (Core)** - 192 doctypes (HR, shifts, payroll)
2. **operations** - 77 doctypes (sites, roster, checkpoints)
3. **grd** - 45 doctypes (government relations - Kuwait)
4. **accommodation** - 31 doctypes (housing management)
5. **hiring** - 23 doctypes (recruitment)
6. **purchase** - 38 doctypes (procurement)
7. **overrides** - 48 files (ERPNext customizations)

---

## 🚫 Why Not Install one_fm Directly?

### **Technical Issues**

#### 1. **Compatibility Problems**
```bash
Error: ImportError: cannot import name 'get_outstanding_invoices' 
from 'lending.loan_management.doctype.loan_repayment.loan_repayment'
```
- Requires different lending app version
- Incompatible with current frappe_ticktix dependencies

#### 2. **Architecture Conflict**
- **one_fm:** Monolithic structure with tight coupling
- **frappe_ticktix:** Plugin-based modular architecture
- Direct installation would break existing plugin system

#### 3. **Code Quality & Maintenance**
- one_fm has 500+ doctypes (many Kuwait-specific)
- Contains features we don't need
- Would inherit technical debt
- Difficult to maintain long-term

### **Strategic Decision**

✅ **Build Fresh Approach:**
- Clean plugin architecture
- Only migrate needed features
- Improve code during migration
- Better long-term maintainability
- Full control over codebase

---

## 📊 Complete Feature Inventory

### **Category 1: HR & Payroll** 
**Priority: HIGH** | **Effort: 8-12 weeks**

#### **Module:** one_fm/one_fm/ (192 doctypes)

**Employee Management:**
- Employee master data & profiles
- Employee grades & skills
- Employee schedules & assignments

**Attendance & Shifts:**
- Shift types & templates
- Shift requests & assignments
- Additional shift assignments
- Employee checkin/checkout
- Attendance tracking
- Penalty management

**Leave Management:**
- Annual leave allocation
- Leave allocation matrix
- Leave reduction tracking
- Leave transfer functionality

**Payroll:**
- Salary components
- Salary structures
- Salary slips (customized)
- Payroll entry processing
- Additional salary management
- Payroll settings

**Performance:**
- Appraisal templates
- Goal cards & KPIs
- Performance goals
- KPI targets

**Training:**
- Training events
- Training programs
- Training feedback

**Override Files (overrides/):**
- 48 Python files customizing ERPNext HR
- salary_slip.py, payroll_entry.py, attendance.py, etc.

**Target Plugin Structure:**
```
frappe_ticktix/plugins/hr/
├── __init__.py
├── employee/          # Employee management
├── attendance/        # Attendance & checkin
├── shifts/           # Shift management
├── leave/            # Leave management
├── payroll/          # Salary & payroll
├── performance/      # Appraisals & KPI
└── training/         # Training programs
```

---

### **Category 2: Operations & Site Management**
**Priority: HIGH** | **Effort: 10-14 weeks**

#### **Module:** one_fm/operations/ (77 doctypes)

**Site Operations:**
- Operations sites
- Operations shifts
- Operations roles
- Post types & posts
- Site locations

**Roster & Scheduling:**
- Operations roster
- Roster employees
- Roster days
- Shift schedules
- Holiday lists

**Checkpoints & Patrols:**
- Checkpoints (15+ related doctypes)
- Checkpoint assignments
- Checkpoint routes
- Patrol routes
- Checkpoint scanning

**Cleaning & Maintenance:**
- Cleaning master tasks
- Cleaning consumables
- Cleaning master lists
- Cleaning object categories
- Cleaning shift plans

**Site Services:**
- Site services
- Service areas
- Service categories
- Maintenance schedules
- Work orders

**Contracts & SLA:**
- Contracts management
- Contract payment schedules
- Contract SLAs
- Service level agreements

**Deployment:**
- Additional deployment
- Change requests (transfers)

**Target Plugin Structure:**
```
frappe_ticktix/plugins/operations/
├── __init__.py
├── sites/            # Site management
├── roster/           # Roster & scheduling
├── checkpoints/      # Patrol & checkpoints
├── cleaning/         # Cleaning operations
├── maintenance/      # Maintenance tasks
├── contracts/        # Contract management
└── deployment/       # Staff deployment
```

---

### **Category 3: Recruitment & Hiring**
**Priority: HIGH** | **Effort: 4-6 weeks**

#### **Module:** one_fm/hiring/ (23 doctypes)

**Recruitment:**
- Job opening advertisements
- Applicant leads
- Head hunting
- Job applicant (customized)

**Interview Process:**
- Interview rounds
- Candidate orientation
- Check list templates

**Onboarding:**
- Onboard employee
- Onboard employee templates
- Onboard employee activities
- Duty commencement

**Offer Management:**
- Job offer templates
- Offer terms templates
- Electronic signature declarations

**Configuration:**
- Hiring settings
- ERF (Employee Requisition Form)

**Target Plugin Structure:**
```
frappe_ticktix/plugins/hr/recruitment/
├── __init__.py
├── job_openings/     # Job postings
├── candidates/       # Applicant management
├── interviews/       # Interview process
├── onboarding/       # New hire onboarding
└── offers/           # Offer management
```

---

### **Category 4: Accommodation Management**
**Priority: HIGH** | **Effort: 4-6 weeks**

#### **Module:** one_fm/accommodation/ (31 doctypes)

**Accommodation Setup:**
- Accommodation master
- Accommodation spaces
- Accommodation units
- Accommodation floors
- Accommodation buildings

**Asset Management:**
- Accommodation assets
- Asset & consumable tracking
- Asset distribution
- Consumable distribution

**Check-in/Check-out:**
- Accommodation checkin/checkout
- Bed assignments
- Bed assignment records

**Inspection & Maintenance:**
- Accommodation inspections
- Inspection templates
- Inspection parameters
- Building condition tracking

**Meters & Utilities:**
- Accommodation meters
- Meter readings
- Meter reading records

**Objects & Categories:**
- Accommodation objects
- Object categories

**Target Plugin Structure:**
```
frappe_ticktix/plugins/accommodation/
├── __init__.py
├── units/            # Accommodation units
├── checkin/          # Check-in/out process
├── assets/           # Asset management
├── inspection/       # Quality inspection
└── utilities/        # Meter readings
```

---

### **Category 5: Government Relations & Compliance**
**Priority: MEDIUM** | **Effort: 6-8 weeks**

#### **Module:** one_fm/grd/ (45 doctypes - Kuwait-specific)

**PACI (Public Authority for Civil Information):**
- PACI transactions
- MOI residency (Jawazat)
- Civil ID applications

**Labor & Immigration:**
- Work permits
- Residency visas
- Visa applications
- Visa extensions

**Business Licenses:**
- MOCI licenses (Ministry of Commerce)
- Articles of association
- Commercial licenses

**Insurance & Medical:**
- Medical insurance
- Health insurance providers
- Insurance items

**Payroll Compliance:**
- PAM salary certificates
- PIFSS monthly deductions
- Form 55 employees

**Fingerprinting:**
- Fingerprint appointments
- Appointment settings

**Target Plugin Structure:**
```
frappe_ticktix/plugins/compliance/
├── __init__.py
├── paci/             # PACI integration
├── visas/            # Visa management
├── licenses/         # Business licenses
├── insurance/        # Medical insurance
└── labor/            # Labor compliance
```

**⚠️ Note:** This module is Kuwait-specific. Evaluate if needed for your region.

---

### **Category 6: Fleet Management**
**Priority: MEDIUM** | **Effort: 2-3 weeks**

#### **Module:** one_fm/fleet_management/ (6 doctypes)

**Vehicle Management:**
- Vehicles
- Vehicle logs
- Vehicle services

**Driver Management:**
- Drivers
- Driver assignments
- Driver logs

**Target Plugin Structure:**
```
frappe_ticktix/plugins/fleet/
├── __init__.py
├── vehicles/         # Vehicle management
├── drivers/          # Driver management
└── maintenance/      # Service & maintenance
```

---

### **Category 7: Procurement & Purchase**
**Priority: MEDIUM** | **Effort: 4-5 weeks**

#### **Module:** one_fm/purchase/ (38 doctypes)

**Procurement Process:**
- Purchase requests
- Purchase orders (customized)
- Supplier quotations
- Request for quotations

**Supplier Management:**
- Suppliers (customized)
- Supplier evaluations
- Supplier scorecards

**Stock & Inventory:**
- Stock entries (customized)
- Material requests (customized)
- Delivery notes (customized)

**Subcontracting:**
- Subcontract orders
- Subcontract receipts
- Subcontract services

**Target Plugin Structure:**
```
frappe_ticktix/plugins/procurement/
├── __init__.py
├── requests/         # Purchase requests
├── orders/           # Purchase orders
├── suppliers/        # Supplier management
└── stock/            # Inventory management
```

---

### **Category 8-11: Lower Priority Modules**

**Legal & Compliance** (19 doctypes) - 2-3 weeks  
**Assets Management** (4 doctypes) - 2-3 weeks  
**Uniform Management** (5 doctypes) - 1-2 weeks  
**Support Modules** (API, Config, Developer tools)

---

## 🏗️ Migration Architecture

### **Plugin Structure Design**

```
frappe_ticktix/
├── __init__.py
├── hooks.py                    # Central hook registration
├── plugins/
│   ├── __init__.py
│   ├── authentication/         # ✅ Existing
│   │   ├── oauth_provider.py
│   │   ├── jwt_middleware.py
│   │   └── login_callback.py
│   ├── branding/              # ✅ Existing
│   │   └── logo_manager.py
│   ├── hr/                    # 🔄 To Build - Phase 1
│   │   ├── __init__.py
│   │   ├── employee/
│   │   ├── attendance/
│   │   ├── shifts/
│   │   ├── leave/
│   │   ├── payroll/
│   │   ├── performance/
│   │   ├── training/
│   │   └── recruitment/
│   ├── operations/            # 🔄 To Build - Phase 2
│   │   ├── __init__.py
│   │   ├── sites/
│   │   ├── roster/
│   │   ├── checkpoints/
│   │   ├── cleaning/
│   │   ├── maintenance/
│   │   ├── contracts/
│   │   └── deployment/
│   ├── accommodation/         # 🔄 To Build - Phase 2
│   │   ├── __init__.py
│   │   ├── units/
│   │   ├── checkin/
│   │   ├── assets/
│   │   ├── inspection/
│   │   └── utilities/
│   ├── fleet/                 # 🔄 To Build - Phase 3
│   │   ├── __init__.py
│   │   ├── vehicles/
│   │   ├── drivers/
│   │   └── maintenance/
│   ├── procurement/           # 🔄 To Build - Phase 3
│   │   ├── __init__.py
│   │   ├── requests/
│   │   ├── orders/
│   │   ├── suppliers/
│   │   └── stock/
│   └── compliance/            # 🔄 To Build - Phase 4
│       ├── __init__.py
│       ├── paci/
│       ├── visas/
│       ├── licenses/
│       └── insurance/
├── utils/
│   ├── verify_setup.py
│   └── verify_cli.py
└── public/
    └── images/
```

### **hooks.py Registration Pattern**

```python
# frappe_ticktix/hooks.py

# Existing plugins
override_whitelisted_methods = {
    # Authentication
    "frappe_ticktix.plugins.authentication.oauth_provider.get_user_info":
        "frappe_ticktix.plugins.authentication.oauth_provider.get_user_info",
    
    # Branding
    "frappe_ticktix.plugins.branding.logo_manager.get_logo":
        "frappe_ticktix.plugins.branding.logo_manager.get_logo",
}

# New HR plugin methods (Phase 1)
override_whitelisted_methods.update({
    # Employee Management
    "frappe_ticktix.plugins.hr.employee.get_employee_details":
        "frappe_ticktix.plugins.hr.employee.get_employee_details",
    
    # Attendance
    "frappe_ticktix.plugins.hr.attendance.mark_attendance":
        "frappe_ticktix.plugins.hr.attendance.mark_attendance",
    
    # Shifts
    "frappe_ticktix.plugins.hr.shifts.get_shift_schedule":
        "frappe_ticktix.plugins.hr.shifts.get_shift_schedule",
})

# Document events
doc_events = {
    "Employee": {
        "validate": "frappe_ticktix.plugins.hr.employee.validate_employee",
        "on_update": "frappe_ticktix.plugins.hr.employee.on_employee_update",
    },
    "Attendance": {
        "validate": "frappe_ticktix.plugins.hr.attendance.validate_attendance",
        "on_submit": "frappe_ticktix.plugins.hr.attendance.on_attendance_submit",
    },
    "Shift Assignment": {
        "validate": "frappe_ticktix.plugins.hr.shifts.validate_shift_assignment",
    }
}

# Scheduled tasks
scheduler_events = {
    "daily": [
        "frappe_ticktix.plugins.hr.attendance.auto_mark_attendance",
        "frappe_ticktix.plugins.hr.shifts.process_shift_schedules",
    ],
    "hourly": [
        "frappe_ticktix.plugins.operations.checkpoints.process_checkpoint_alerts",
    ]
}
```

---

## 🚀 Implementation Strategy

### **Core Principles**

1. **Incremental Migration**
   - One feature at a time
   - Test thoroughly before moving to next
   - Don't break existing functionality

2. **Plugin Architecture**
   - Each category as separate plugin
   - Clear module boundaries
   - Minimal cross-plugin dependencies

3. **Code Quality**
   - Improve code during migration
   - Add proper documentation
   - Follow Frappe best practices

4. **Testing First**
   - Write tests before migration
   - Test each feature independently
   - Integration tests for plugin interactions

### **Migration Process per Feature**

#### **Step 1: Analysis**
```bash
# Identify feature in one_fm
cd /home/sagivasan/ticktix/apps/one_fm
find . -name "*feature_name*" -type f

# Study the implementation
# - Doctypes (.json files)
# - Controllers (.py files)
# - Client scripts (.js files)
# - Hooks (hooks.py)
# - Dependencies
```

#### **Step 2: Design**
- Create plugin structure
- Design database schema (doctypes)
- Plan API endpoints
- Define hooks and events
- Document dependencies

#### **Step 3: Implementation**
```python
# Example: Shift Management

# 1. Create plugin directory
mkdir -p frappe_ticktix/plugins/hr/shifts

# 2. Create __init__.py
touch frappe_ticktix/plugins/hr/shifts/__init__.py

# 3. Create main controller
# frappe_ticktix/plugins/hr/shifts/shift_manager.py

import frappe
from frappe import _
from frappe.utils import getdate, add_days

class ShiftManager:
    """
    Shift Management Controller
    Migrated from: one_fm.one_fm.doctype.shift_assignment
    """
    
    @staticmethod
    @frappe.whitelist()
    def get_shift_schedule(employee, from_date, to_date):
        """
        Get shift schedule for employee within date range
        
        Args:
            employee: Employee ID
            from_date: Start date
            to_date: End date
            
        Returns:
            List of shift assignments
        """
        return frappe.get_all(
            "Shift Assignment",
            filters={
                "employee": employee,
                "from_date": ["<=", to_date],
                "to_date": [">=", from_date],
                "docstatus": 1
            },
            fields=["name", "shift_type", "from_date", "to_date"]
        )
    
    @staticmethod
    @frappe.whitelist()
    def create_shift_assignment(employee, shift_type, from_date, to_date):
        """Create shift assignment for employee"""
        doc = frappe.get_doc({
            "doctype": "Shift Assignment",
            "employee": employee,
            "shift_type": shift_type,
            "from_date": from_date,
            "to_date": to_date
        })
        doc.insert()
        doc.submit()
        return doc.name
    
    @staticmethod
    def validate_shift_assignment(doc, method):
        """Validate shift assignment before save"""
        # Check for overlapping shifts
        overlapping = frappe.get_all(
            "Shift Assignment",
            filters={
                "employee": doc.employee,
                "name": ["!=", doc.name],
                "docstatus": ["!=", 2],
                "from_date": ["<=", doc.to_date],
                "to_date": [">=", doc.from_date]
            }
        )
        
        if overlapping:
            frappe.throw(_("Overlapping shift assignments found"))

# 4. Register in hooks.py
# See hooks.py pattern above

# 5. Add doctypes if needed
# bench new-doctype "Shift Assignment Custom"
```

#### **Step 4: Testing**
```python
# frappe_ticktix/plugins/hr/shifts/test_shift_manager.py

import frappe
import unittest
from datetime import datetime, timedelta
from frappe_ticktix.plugins.hr.shifts.shift_manager import ShiftManager

class TestShiftManager(unittest.TestCase):
    
    def setUp(self):
        """Create test data"""
        self.employee = frappe.get_doc({
            "doctype": "Employee",
            "first_name": "Test",
            "last_name": "Employee"
        }).insert()
        
        self.shift_type = frappe.get_doc({
            "doctype": "Shift Type",
            "name": "Morning Shift",
            "start_time": "08:00:00",
            "end_time": "16:00:00"
        }).insert()
    
    def test_create_shift_assignment(self):
        """Test creating shift assignment"""
        from_date = datetime.today()
        to_date = from_date + timedelta(days=7)
        
        assignment = ShiftManager.create_shift_assignment(
            employee=self.employee.name,
            shift_type=self.shift_type.name,
            from_date=from_date,
            to_date=to_date
        )
        
        self.assertIsNotNone(assignment)
    
    def test_overlapping_shifts(self):
        """Test overlapping shift validation"""
        # Test implementation
        pass
    
    def tearDown(self):
        """Clean up test data"""
        frappe.delete_doc("Employee", self.employee.name)
        frappe.delete_doc("Shift Type", self.shift_type.name)
```

#### **Step 5: Documentation**
```markdown
# frappe_ticktix/plugins/hr/shifts/README.md

# Shift Management Plugin

## Overview
Manages employee shift assignments and scheduling.

## Features
- Create shift assignments
- Get shift schedules
- Validate overlapping shifts
- Auto-assignment based on roster

## API Endpoints

### `get_shift_schedule`
**Method:** POST  
**URL:** `/api/method/frappe_ticktix.plugins.hr.shifts.shift_manager.get_shift_schedule`

**Parameters:**
- `employee` (required): Employee ID
- `from_date` (required): Start date (YYYY-MM-DD)
- `to_date` (required): End date (YYYY-MM-DD)

**Response:**
```json
{
  "message": [
    {
      "name": "SHFT-00001",
      "shift_type": "Morning Shift",
      "from_date": "2025-10-20",
      "to_date": "2025-10-26"
    }
  ]
}
```

## Usage Example
```python
import frappe

# Get employee shift schedule
shifts = frappe.call(
    "frappe_ticktix.plugins.hr.shifts.shift_manager.get_shift_schedule",
    employee="EMP-00001",
    from_date="2025-10-20",
    to_date="2025-10-26"
)
```

## Dependencies
- Employee doctype
- Shift Type doctype
- Shift Assignment doctype

## Migration Notes
- Migrated from: `one_fm.one_fm.doctype.shift_assignment`
- Changes: Improved validation, added API endpoints
- Compatible with: Frappe v15+
```

#### **Step 6: Integration**
- Test with existing plugins (authentication, branding)
- Verify hooks registration
- Test API endpoints
- Perform user acceptance testing

---

## 📅 Phase-by-Phase Plan

### **PHASE 1: Foundation (Weeks 1-6) - MUST HAVE**

**Goal:** Basic employee management & operations capability

#### **Week 1-2: HR Core - Employee Management**
- [ ] Create `plugins/hr/employee/` structure
- [ ] Migrate employee master data management
- [ ] Employee profile & skills tracking
- [ ] Employee grade system
- [ ] API endpoints for employee CRUD
- [ ] Write tests
- [ ] Document APIs

**Deliverables:**
- ✅ Employee management plugin
- ✅ API documentation
- ✅ Test coverage > 80%

#### **Week 3-4: HR Core - Attendance & Shifts**
- [ ] Create `plugins/hr/attendance/` structure
- [ ] Create `plugins/hr/shifts/` structure
- [ ] Migrate shift types & templates
- [ ] Shift assignment functionality
- [ ] Employee checkin/checkout
- [ ] Attendance tracking
- [ ] Auto-attendance marking
- [ ] Write tests
- [ ] Document APIs

**Deliverables:**
- ✅ Attendance tracking plugin
- ✅ Shift management plugin
- ✅ Scheduled jobs for auto-attendance
- ✅ API documentation

#### **Week 5-6: Operations Core - Sites & Basic Roster**
- [ ] Create `plugins/operations/sites/` structure
- [ ] Create `plugins/operations/roster/` structure
- [ ] Migrate operations sites
- [ ] Operations roles & posts
- [ ] Basic roster functionality
- [ ] Site location tracking
- [ ] Write tests
- [ ] Document APIs

**Deliverables:**
- ✅ Site management plugin
- ✅ Basic roster plugin
- ✅ MVP system operational

**Phase 1 Success Criteria:**
- Employees can be managed
- Attendance can be tracked
- Shifts can be assigned
- Sites can be configured
- Basic roster can be created

---

### **PHASE 2: Core Operations (Weeks 7-16) - SHOULD HAVE**

**Goal:** Full operational capability for facility management

#### **Week 7-10: Advanced Operations**
- [ ] Checkpoint & patrol system
- [ ] Cleaning schedules & management
- [ ] Maintenance tasks
- [ ] Contract management
- [ ] Work order system
- [ ] Service level agreements

**Deliverables:**
- ✅ Full operations plugin suite
- ✅ Checkpoint tracking operational
- ✅ Cleaning & maintenance systems

#### **Week 11-13: Recruitment & Hiring**
- [ ] Create `plugins/hr/recruitment/` structure
- [ ] Job opening management
- [ ] Candidate tracking
- [ ] Interview process
- [ ] Onboarding workflows
- [ ] Offer management

**Deliverables:**
- ✅ Complete recruitment system
- ✅ Onboarding workflows

#### **Week 14-16: Accommodation Management**
- [ ] Create `plugins/accommodation/` structure
- [ ] Accommodation unit management
- [ ] Check-in/check-out system
- [ ] Asset tracking
- [ ] Inspection management
- [ ] Utility meter readings

**Deliverables:**
- ✅ Full accommodation management
- ✅ Asset tracking operational

**Phase 2 Success Criteria:**
- Complete operations management
- Full recruitment capability
- Accommodation tracking functional
- All core features operational

---

### **PHASE 3: Business Operations (Weeks 17-26) - NICE TO HAVE**

**Goal:** Complete business process automation

#### **Week 17-20: Payroll System**
- [ ] Create `plugins/hr/payroll/` structure
- [ ] Migrate salary components
- [ ] Salary structure management
- [ ] Salary slip generation
- [ ] Payroll entry processing
- [ ] Payroll reports
- [ ] Integration with attendance/leave

**Deliverables:**
- ✅ Complete payroll system
- ✅ Payroll reports
- ✅ Salary processing automation

#### **Week 21-23: Procurement**
- [ ] Create `plugins/procurement/` structure
- [ ] Purchase request workflow
- [ ] Purchase order management
- [ ] Supplier management
- [ ] Supplier evaluation
- [ ] Stock integration

**Deliverables:**
- ✅ Procurement workflow
- ✅ Supplier management

#### **Week 24-26: Fleet Management**
- [ ] Create `plugins/fleet/` structure
- [ ] Vehicle management
- [ ] Driver management
- [ ] Vehicle service tracking
- [ ] Vehicle logs

**Deliverables:**
- ✅ Complete fleet management
- ✅ Vehicle tracking system

**Phase 3 Success Criteria:**
- Payroll fully automated
- Procurement workflow complete
- Fleet tracking operational

---

### **PHASE 4: Compliance & Extras (Weeks 27-36) - OPTIONAL**

**Goal:** Full-featured enterprise system

#### **Week 27-30: Government Relations (if Kuwait)**
- [ ] Create `plugins/compliance/` structure
- [ ] PACI integration
- [ ] Visa management
- [ ] License tracking
- [ ] Insurance management

#### **Week 31-32: Legal & Compliance**
- [ ] Legal case management
- [ ] Investigation tracking
- [ ] Legal document management

#### **Week 33-36: Assets & Final Features**
- [ ] Asset tracking system
- [ ] Uniform management
- [ ] Final integrations
- [ ] Performance optimization
- [ ] Complete documentation

**Deliverables:**
- ✅ Complete system
- ✅ All features operational
- ✅ Full documentation

---

## 📖 Detailed Implementation Guide

### **Getting Started: First Feature Migration**

#### **Recommended First Feature: Shift Management**

**Why?**
- Core to facility management
- Self-contained functionality
- Medium complexity
- Foundation for attendance

#### **Step-by-Step Implementation**

##### **1. Analyze one_fm Shift Implementation**

```bash
# Navigate to one_fm
cd /home/sagivasan/ticktix/apps/one_fm

# Find all shift-related files
find . -name "*shift*" -type f | grep -v __pycache__ | grep -v .pyc

# Expected output:
# ./one_fm/one_fm/doctype/shift_type/
# ./one_fm/one_fm/doctype/shift_assignment/
# ./one_fm/one_fm/doctype/shift_request/
# ./one_fm/operations/doctype/operations_shift/

# Study the JSON doctype definitions
cat ./one_fm/one_fm/doctype/shift_assignment/shift_assignment.json

# Study the Python controllers
cat ./one_fm/one_fm/doctype/shift_assignment/shift_assignment.py

# Check for hooks
grep -r "shift" ./one_fm/one_fm/hooks.py
```

##### **2. Create Plugin Structure**

```bash
# Navigate to frappe_ticktix
cd /home/sagivasan/ticktix/apps/frappe_ticktix

# Create HR plugin structure
mkdir -p frappe_ticktix/plugins/hr
mkdir -p frappe_ticktix/plugins/hr/shifts
mkdir -p frappe_ticktix/plugins/hr/shifts/doctype

# Create __init__.py files
touch frappe_ticktix/plugins/hr/__init__.py
touch frappe_ticktix/plugins/hr/shifts/__init__.py
```

##### **3. Create Shift Manager**

Create file: `frappe_ticktix/plugins/hr/shifts/shift_manager.py`

```python
"""
Shift Management Plugin for frappe_ticktix
Migrated from: one_fm.one_fm.doctype.shift_assignment

Handles:
- Shift type management
- Shift assignments
- Shift requests
- Shift validation
"""

import frappe
from frappe import _
from frappe.utils import getdate, add_days, now_datetime
from datetime import datetime, timedelta

class ShiftManager:
    """Main controller for shift management"""
    
    @staticmethod
    @frappe.whitelist()
    def get_shift_schedule(employee, from_date, to_date):
        """
        Get shift schedule for employee
        
        Args:
            employee (str): Employee ID
            from_date (str): Start date (YYYY-MM-DD)
            to_date (str): End date (YYYY-MM-DD)
            
        Returns:
            list: List of shift assignments
        """
        frappe.has_permission("Shift Assignment", "read", throw=True)
        
        shifts = frappe.get_all(
            "Shift Assignment",
            filters={
                "employee": employee,
                "from_date": ["<=", to_date],
                "to_date": [">=", from_date],
                "docstatus": ["!=", 2]  # Exclude cancelled
            },
            fields=[
                "name", 
                "shift_type", 
                "from_date", 
                "to_date",
                "status"
            ],
            order_by="from_date"
        )
        
        # Enrich with shift type details
        for shift in shifts:
            shift_type = frappe.get_cached_doc("Shift Type", shift.shift_type)
            shift.update({
                "start_time": shift_type.start_time,
                "end_time": shift_type.end_time,
                "shift_name": shift_type.shift_name
            })
        
        return shifts
    
    @staticmethod
    @frappe.whitelist()
    def create_shift_assignment(employee, shift_type, from_date, to_date, 
                                company=None):
        """
        Create new shift assignment
        
        Args:
            employee: Employee ID
            shift_type: Shift Type name
            from_date: Assignment start date
            to_date: Assignment end date
            company: Company (optional)
            
        Returns:
            str: Name of created shift assignment
        """
        frappe.has_permission("Shift Assignment", "create", throw=True)
        
        # Get employee company if not provided
        if not company:
            employee_doc = frappe.get_doc("Employee", employee)
            company = employee_doc.company
        
        # Create shift assignment
        doc = frappe.get_doc({
            "doctype": "Shift Assignment",
            "employee": employee,
            "shift_type": shift_type,
            "from_date": from_date,
            "to_date": to_date,
            "company": company,
            "status": "Active"
        })
        
        doc.insert()
        doc.submit()
        
        frappe.msgprint(_("Shift assignment created successfully"))
        
        return doc.name
    
    @staticmethod
    @frappe.whitelist()
    def request_shift_change(employee, current_shift, requested_shift, 
                            date, reason):
        """
        Create shift change request
        
        Args:
            employee: Employee ID
            current_shift: Current shift type
            requested_shift: Requested shift type
            date: Date of shift change
            reason: Reason for change
            
        Returns:
            str: Name of shift request
        """
        doc = frappe.get_doc({
            "doctype": "Shift Request",
            "employee": employee,
            "from_shift": current_shift,
            "to_shift": requested_shift,
            "date": date,
            "reason": reason,
            "status": "Pending"
        })
        
        doc.insert()
        
        return doc.name
    
    @staticmethod
    def validate_shift_assignment(doc, method):
        """
        Validate shift assignment before save
        Called via hooks on Shift Assignment doctype
        """
        ShiftManager._check_overlapping_shifts(doc)
        ShiftManager._validate_shift_dates(doc)
        ShiftManager._validate_employee_active(doc)
    
    @staticmethod
    def _check_overlapping_shifts(doc):
        """Check for overlapping shift assignments"""
        overlapping = frappe.get_all(
            "Shift Assignment",
            filters={
                "employee": doc.employee,
                "name": ["!=", doc.name],
                "docstatus": ["!=", 2],
                "from_date": ["<=", doc.to_date],
                "to_date": [">=", doc.from_date]
            },
            fields=["name", "shift_type", "from_date", "to_date"]
        )
        
        if overlapping:
            frappe.throw(_(
                "Overlapping shift assignment found: {0} ({1} to {2})"
            ).format(
                overlapping[0].name,
                overlapping[0].from_date,
                overlapping[0].to_date
            ))
    
    @staticmethod
    def _validate_shift_dates(doc):
        """Validate from_date and to_date"""
        if getdate(doc.from_date) > getdate(doc.to_date):
            frappe.throw(_("From date cannot be after To date"))
    
    @staticmethod
    def _validate_employee_active(doc):
        """Validate employee is active"""
        employee = frappe.get_cached_doc("Employee", doc.employee)
        if employee.status != "Active":
            frappe.throw(_("Cannot assign shift to inactive employee"))
    
    @staticmethod
    def on_shift_assignment_submit(doc, method):
        """Actions after shift assignment is submitted"""
        # Mark any pending shift requests as processed
        shift_requests = frappe.get_all(
            "Shift Request",
            filters={
                "employee": doc.employee,
                "date": ["between", [doc.from_date, doc.to_date]],
                "status": "Pending"
            }
        )
        
        for req in shift_requests:
            req_doc = frappe.get_doc("Shift Request", req.name)
            req_doc.status = "Approved"
            req_doc.save()
    
    @staticmethod
    @frappe.whitelist()
    def get_employee_current_shift(employee, date=None):
        """
        Get employee's current shift for a specific date
        
        Args:
            employee: Employee ID
            date: Date (default: today)
            
        Returns:
            dict: Shift details or None
        """
        if not date:
            date = getdate()
        
        shift = frappe.get_all(
            "Shift Assignment",
            filters={
                "employee": employee,
                "from_date": ["<=", date],
                "to_date": [">=", date],
                "docstatus": 1,
                "status": "Active"
            },
            fields=["name", "shift_type"],
            limit=1
        )
        
        if shift:
            shift_type = frappe.get_cached_doc("Shift Type", shift[0].shift_type)
            return {
                "assignment": shift[0].name,
                "shift_type": shift_type.name,
                "shift_name": shift_type.shift_name,
                "start_time": shift_type.start_time,
                "end_time": shift_type.end_time
            }
        
        return None


# Scheduled tasks
def auto_process_shift_schedules():
    """
    Process shift schedules daily
    Registered in hooks.py as scheduled task
    """
    # Auto-approve shift requests
    # Generate attendance records based on shifts
    # Send shift reminders
    pass
```

##### **4. Register in hooks.py**

Edit: `frappe_ticktix/hooks.py`

```python
# Add to existing override_whitelisted_methods
override_whitelisted_methods.update({
    # Shift Management
    "frappe_ticktix.plugins.hr.shifts.shift_manager.get_shift_schedule":
        "frappe_ticktix.plugins.hr.shifts.shift_manager.get_shift_schedule",
    "frappe_ticktix.plugins.hr.shifts.shift_manager.create_shift_assignment":
        "frappe_ticktix.plugins.hr.shifts.shift_manager.create_shift_assignment",
    "frappe_ticktix.plugins.hr.shifts.shift_manager.request_shift_change":
        "frappe_ticktix.plugins.hr.shifts.shift_manager.request_shift_change",
    "frappe_ticktix.plugins.hr.shifts.shift_manager.get_employee_current_shift":
        "frappe_ticktix.plugins.hr.shifts.shift_manager.get_employee_current_shift",
})

# Add document events
doc_events.update({
    "Shift Assignment": {
        "validate": "frappe_ticktix.plugins.hr.shifts.shift_manager.validate_shift_assignment",
        "on_submit": "frappe_ticktix.plugins.hr.shifts.shift_manager.on_shift_assignment_submit",
    }
})

# Add scheduled tasks
scheduler_events = {
    "daily": [
        "frappe_ticktix.plugins.hr.shifts.shift_manager.auto_process_shift_schedules"
    ]
}
```

##### **5. Create Tests**

Create file: `frappe_ticktix/plugins/hr/shifts/test_shift_manager.py`

```python
import frappe
import unittest
from datetime import datetime, timedelta
from frappe.utils import getdate, add_days
from frappe_ticktix.plugins.hr.shifts.shift_manager import ShiftManager

class TestShiftManager(unittest.TestCase):
    
    def setUp(self):
        """Create test data"""
        # Create test employee
        if not frappe.db.exists("Employee", "TEST-EMP-001"):
            self.employee = frappe.get_doc({
                "doctype": "Employee",
                "employee": "TEST-EMP-001",
                "first_name": "Test",
                "last_name": "Employee",
                "company": frappe.defaults.get_defaults().company,
                "status": "Active"
            }).insert(ignore_permissions=True)
        else:
            self.employee = frappe.get_doc("Employee", "TEST-EMP-001")
        
        # Create test shift type
        if not frappe.db.exists("Shift Type", "Test Morning Shift"):
            self.shift_type = frappe.get_doc({
                "doctype": "Shift Type",
                "name": "Test Morning Shift",
                "shift_name": "Morning Shift",
                "start_time": "08:00:00",
                "end_time": "16:00:00"
            }).insert(ignore_permissions=True)
        else:
            self.shift_type = frappe.get_doc("Shift Type", "Test Morning Shift")
    
    def test_create_shift_assignment(self):
        """Test creating a shift assignment"""
        from_date = getdate()
        to_date = add_days(from_date, 7)
        
        assignment = ShiftManager.create_shift_assignment(
            employee=self.employee.name,
            shift_type=self.shift_type.name,
            from_date=from_date,
            to_date=to_date
        )
        
        self.assertIsNotNone(assignment)
        
        # Verify assignment was created
        doc = frappe.get_doc("Shift Assignment", assignment)
        self.assertEqual(doc.employee, self.employee.name)
        self.assertEqual(doc.shift_type, self.shift_type.name)
        
        # Cleanup
        frappe.delete_doc("Shift Assignment", assignment, force=True)
    
    def test_get_shift_schedule(self):
        """Test retrieving shift schedule"""
        # Create assignment
        from_date = getdate()
        to_date = add_days(from_date, 7)
        
        assignment = ShiftManager.create_shift_assignment(
            employee=self.employee.name,
            shift_type=self.shift_type.name,
            from_date=from_date,
            to_date=to_date
        )
        
        # Get schedule
        schedule = ShiftManager.get_shift_schedule(
            employee=self.employee.name,
            from_date=from_date,
            to_date=to_date
        )
        
        self.assertIsNotNone(schedule)
        self.assertTrue(len(schedule) > 0)
        self.assertEqual(schedule[0]["shift_type"], self.shift_type.name)
        
        # Cleanup
        frappe.delete_doc("Shift Assignment", assignment, force=True)
    
    def test_overlapping_shifts(self):
        """Test overlapping shift validation"""
        from_date = getdate()
        to_date = add_days(from_date, 7)
        
        # Create first assignment
        assignment1 = ShiftManager.create_shift_assignment(
            employee=self.employee.name,
            shift_type=self.shift_type.name,
            from_date=from_date,
            to_date=to_date
        )
        
        # Try to create overlapping assignment
        overlap_from = add_days(from_date, 3)
        overlap_to = add_days(from_date, 10)
        
        with self.assertRaises(frappe.ValidationError):
            ShiftManager.create_shift_assignment(
                employee=self.employee.name,
                shift_type=self.shift_type.name,
                from_date=overlap_from,
                to_date=overlap_to
            )
        
        # Cleanup
        frappe.delete_doc("Shift Assignment", assignment1, force=True)
    
    def test_get_current_shift(self):
        """Test getting employee's current shift"""
        from_date = getdate()
        to_date = add_days(from_date, 7)
        
        # Create assignment
        assignment = ShiftManager.create_shift_assignment(
            employee=self.employee.name,
            shift_type=self.shift_type.name,
            from_date=from_date,
            to_date=to_date
        )
        
        # Get current shift
        current_shift = ShiftManager.get_employee_current_shift(
            employee=self.employee.name,
            date=getdate()
        )
        
        self.assertIsNotNone(current_shift)
        self.assertEqual(current_shift["shift_type"], self.shift_type.name)
        
        # Cleanup
        frappe.delete_doc("Shift Assignment", assignment, force=True)
    
    def tearDown(self):
        """Cleanup test data"""
        frappe.db.rollback()
```

##### **6. Create Documentation**

Create file: `frappe_ticktix/plugins/hr/shifts/README.md`

(See documentation example in previous section)

##### **7. Test the Implementation**

```bash
# Navigate to bench directory
cd /home/sagivasan/ticktix

# Run tests
bench --site ticktix.local run-tests --app frappe_ticktix --module plugins.hr.shifts

# Clear cache
bench --site ticktix.local clear-cache

# Restart bench
bench restart

# Test API endpoint manually
curl -X POST http://ticktix.local:8000/api/method/frappe_ticktix.plugins.hr.shifts.shift_manager.get_shift_schedule \
  -H "Content-Type: application/json" \
  -d '{
    "employee": "EMP-00001",
    "from_date": "2025-10-20",
    "to_date": "2025-10-27"
  }'
```

---

## ✅ Testing Strategy

### **1. Unit Tests**
- Test each function independently
- Mock external dependencies
- Achieve 80%+ code coverage

### **2. Integration Tests**
- Test plugin interactions
- Test with real doctypes
- Verify hooks execution

### **3. API Tests**
- Test all whitelisted methods
- Verify permissions
- Test error handling

### **4. User Acceptance Tests**
- Real-world scenarios
- Complete workflows
- Performance testing

### **5. Regression Tests**
- Ensure existing plugins still work
- No breaking changes
- Backward compatibility

---

## 📊 Timeline & Resources

### **Resource Requirements**

#### **Team Composition**

**Option A: 1 Developer**
- **Timeline:** 18 months
- **Role:** Full-stack developer
- **Skills:** Python, Frappe/ERPNext, JavaScript
- **Workload:** 100% dedicated

**Option B: 2 Developers**
- **Timeline:** 9-12 months
- **Roles:**
  - Lead Developer: Architecture, HR, Operations
  - Developer: Accommodation, Fleet, Procurement
- **Skills:** Python, Frappe/ERPNext, JavaScript
- **Workload:** 100% dedicated each

**Option C: 3 Developers** (Recommended)
- **Timeline:** 6-9 months
- **Roles:**
  - Senior Developer: Architecture, HR Core
  - Developer 1: Operations, Accommodation
  - Developer 2: Recruitment, Fleet, Procurement
- **Skills:** Python, Frappe/ERPNext, JavaScript
- **Workload:** 100% dedicated each

### **Timeline by Approach**

#### **MVP Approach (3 months)**
- **Phase 1 Only:** HR Core + Operations Core
- **Features:** 40% of total features
- **Effort:** ~520 hours
- **Team:** 2-3 developers
- **Best For:** Quick start, validate concept

#### **Core System Approach (6 months)** ⭐ **RECOMMENDED**
- **Phase 1 + Phase 2:** Foundation + Core Operations
- **Features:** 70% of total features
- **Effort:** ~1,040 hours
- **Team:** 2-3 developers
- **Best For:** Full operational capability

#### **Complete System Approach (9-12 months)**
- **All 4 Phases:** Everything from one_fm
- **Features:** 100% of total features
- **Effort:** ~1,560 hours
- **Team:** 2-3 developers
- **Best For:** Complete replacement

### **Effort Breakdown**

| Phase | Features | Hours | With 1 Dev | With 2 Devs | With 3 Devs |
|-------|----------|-------|------------|-------------|-------------|
| **Phase 1** | Foundation | 400h | 10 weeks | 5 weeks | 3 weeks |
| **Phase 2** | Core Ops | 640h | 16 weeks | 8 weeks | 5 weeks |
| **Phase 3** | Business | 320h | 8 weeks | 4 weeks | 3 weeks |
| **Phase 4** | Compliance | 200h | 5 weeks | 3 weeks | 2 weeks |
| **Total** | All | 1,560h | 39 weeks | 20 weeks | 13 weeks |

*Note: Assumes 40-hour work weeks, includes testing & documentation*

---

## 🎯 Success Metrics

### **Phase 1 Success:**
- [ ] Employees can be created and managed
- [ ] Attendance tracking works
- [ ] Shifts can be assigned and managed
- [ ] Sites can be configured
- [ ] Basic roster functionality
- [ ] All tests passing
- [ ] API documentation complete

### **Phase 2 Success:**
- [ ] Full operations management
- [ ] Checkpoint system operational
- [ ] Recruitment workflow complete
- [ ] Accommodation tracking functional
- [ ] All integrations working

### **Phase 3 Success:**
- [ ] Payroll processing automated
- [ ] Procurement workflow complete
- [ ] Fleet management operational
- [ ] Business processes automated

### **Phase 4 Success:**
- [ ] Compliance features operational
- [ ] All features from one_fm migrated
- [ ] System production-ready
- [ ] Complete documentation

---

## 📝 Next Steps

### **Immediate Actions:**

1. **Choose Approach:**
   - [ ] MVP (3 months)
   - [ ] Core System (6 months) ⭐ **RECOMMENDED**
   - [ ] Complete System (9-12 months)

2. **Confirm Resources:**
   - [ ] Number of developers available
   - [ ] Timeline constraints
   - [ ] Budget approval

3. **Start Phase 1:**
   - [ ] Create plugin structure
   - [ ] Begin shift management migration
   - [ ] Set up testing framework

### **Questions to Answer:**

1. **Which approach do you want to take?**
   - MVP / Core System / Complete System?

2. **What's your team size?**
   - 1, 2, or 3 developers?

3. **What's your timeline?**
   - Urgent (3 months) / Normal (6 months) / Flexible (9-12 months)?

4. **Which feature should we start with?**
   - Shift Management (recommended)
   - Attendance Tracking
   - Employee Management
   - Other?

---

## 📞 Support & Resources

### **Documentation**
- This guide: Complete migration documentation
- Feature Inventory: `ONE_FM_FEATURE_INVENTORY.md`
- HR Plan: `HR_MIGRATION_PLAN.md`
- HR Strategy: `HR_MIGRATION_STRATEGY.md`

### **Source Code**
- **frappe_ticktix:** `/home/sagivasan/ticktix/apps/frappe_ticktix`
- **one_fm:** `/home/sagivasan/ticktix/apps/one_fm`

### **Key Files**
- **hooks.py:** `/home/sagivasan/ticktix/apps/frappe_ticktix/frappe_ticktix/hooks.py`
- **Plugin structure:** `/home/sagivasan/ticktix/apps/frappe_ticktix/frappe_ticktix/plugins/`

---

## 🎉 Ready to Start!

This guide provides everything needed to migrate from one_fm to frappe_ticktix. Choose your approach, gather your team, and let's start building!

**Recommended First Step:**  
Start with **Shift Management** plugin using the detailed implementation guide in Section 9.

---

*Complete Migration Guide - Version 1.0*  
*Last Updated: October 20, 2025*  
*Ready for implementation!* 🚀
