# one_fm Complete Feature Inventory & Categorization

**Date:** October 20, 2025  
**Source:** one_fm Facility Management System  
**Target:** frappe_ticktix (Fresh Implementation - Option 1)  
**Total Modules:** 36 modules  
**Total Doctypes:** ~468 doctypes

---

## 📊 Executive Summary

one_fm is a **comprehensive facility management system** with features covering:
- Human Resources & Payroll
- Operations & Site Management
- Accommodation Management
- Fleet Management
- Hiring & Recruitment
- Legal & Compliance
- Purchase & Procurement
- Government Relations (Kuwait-specific)
- Asset Management

---

## 🏗️ Module Overview by Size

| Module | Doctypes | Python Files | Category | Priority |
|--------|----------|--------------|----------|----------|
| **one_fm (Core)** | 192 | 10 | HR/Core | HIGH |
| **operations** | 77 | 1 | Operations | HIGH |
| **grd** | 45 | 2 | Government/Legal | MEDIUM |
| **purchase** | 38 | 3 | Procurement | MEDIUM |
| **accommodation** | 31 | 2 | Accommodation | HIGH |
| **hiring** | 23 | 2 | Recruitment | HIGH |
| **legal** | 19 | 1 | Legal | LOW |
| **developer** | 12 | 1 | Internal Tools | LOW |
| **fleet_management** | 6 | 2 | Fleet | MEDIUM |
| **uniform_management** | 5 | 1 | Operations | LOW |
| **subcontract** | 5 | 1 | Procurement | LOW |
| **one_fm_assets** | 4 | 1 | Assets | LOW |
| **paci** | 3 | 1 | Government | LOW |
| **overrides** | 0 | 48 | Customizations | HIGH |

---

## 📂 CATEGORY 1: HUMAN RESOURCES & PAYROLL

### **Priority: HIGH** | **Estimated Effort: 8-12 weeks**

#### Core HR Features (one_fm/one_fm/)
**Selected Doctypes (192 total):**

**Employee Management:**
- employee (customizations)
- employee_checkin (attendance tracking)
- employee_grade
- employee_skill_details
- employee_schedule

**Attendance & Shifts:**
- shift_type
- shift_request
- shift_assignment
- additional_shift_assignment
- penalty
- penalty_issuance
- penalty_type

**Leave Management:**
- annual_leave_allocation_matrix
- annual_leave_allocation_reduction
- leave_allocation_tool
- leave_transfer

**Payroll:**
- payroll_entry (customized)
- salary_component (customized)
- salary_slip (customized)
- salary_structure (customized)
- additional_salary
- payroll_additional_settings

**Performance & Appraisal:**
- appraisal_template
- goal_card
- performance_goal
- kpi
- kpi_target

**Training:**
- training_event
- training_program
- training_feedback

#### HR Overrides (overrides/)
**48 Python files customizing standard ERPNext:**
- salary_slip.py
- payroll_entry.py
- attendance.py
- leave_application.py
- employee.py
- shift_type.py
- employee_checkin.py
- additional_salary.py
... (40 more override files)

**Migration Strategy for HR:**
```
frappe_ticktix/plugins/hr/
├── employee/           # Employee management
├── attendance/         # Attendance & checkin
├── shifts/            # Shift management
├── leave/             # Leave management
├── payroll/           # Salary & payroll
├── performance/       # Appraisals & KPI
└── training/          # Training programs
```

---

## 📂 CATEGORY 2: OPERATIONS & SITE MANAGEMENT

### **Priority: HIGH** | **Estimated Effort: 10-14 weeks**

#### Operations Module (operations/)
**77 Doctypes - Core Facility Management:**

**Site Operations:**
- operations_site
- operations_shift
- operations_role
- post_type
- post
- site_location

**Roster & Scheduling:**
- operations_roster
- roster_employee
- roster_day
- shift_schedule
- holiday_list_dates

**Checkpoints & Patrols:**
- checkpoints (15 related doctypes)
- checkpoint_assignment_scan
- checkpoint_routes
- checkpoint_assignment
- patrol_routes

**Cleaning & Maintenance:**
- cleaning_master_tasks
- cleaning_consumables
- cleaning_master_list
- cleaning_object_category
- cleaning_shift_plan

**Site Services:**
- site_service
- service_area
- service_category
- maintenance_schedule
- work_order

**Contracts & SLA:**
- contracts
- contract_payment_schedule
- contract_sla
- service_level_agreement

**Deployment:**
- additional_deployment
- change_request (employee transfers)

**Migration Strategy for Operations:**
```
frappe_ticktix/plugins/operations/
├── sites/             # Site management
├── roster/            # Roster & scheduling
├── checkpoints/       # Patrol & checkpoints
├── cleaning/          # Cleaning operations
├── maintenance/       # Maintenance tasks
├── contracts/         # Contract management
└── deployment/        # Staff deployment
```

---

## 📂 CATEGORY 3: HIRING & RECRUITMENT

### **Priority: HIGH** | **Estimated Effort: 4-6 weeks**

#### Hiring Module (hiring/)
**23 Doctypes:**

**Recruitment:**
- job_opening_add
- applicant_lead
- head_hunt
- job_applicant (customized)

**Interview Process:**
- job_applicant_interview_round
- candidate_orientation
- check_list_template

**Onboarding:**
- onboard_employee
- onboard_employee_template
- onboard_employee_activity
- duty_commencement

**Offer Management:**
- job_offer_templates
- offer_terms_table_template
- electronic_signature_declaration

**Configuration:**
- hiring_settings
- erf_employee (Employee Requisition Form)

**Migration Strategy for Hiring:**
```
frappe_ticktix/plugins/hr/recruitment/
├── job_openings/      # Job postings
├── candidates/        # Applicant management
├── interviews/        # Interview process
├── onboarding/        # New hire onboarding
└── offers/            # Offer management
```

---

## 📂 CATEGORY 4: ACCOMMODATION MANAGEMENT

### **Priority: HIGH** | **Estimated Effort: 4-6 weeks**

#### Accommodation Module (accommodation/)
**31 Doctypes:**

**Accommodation Setup:**
- accommodation
- accommodation_space
- accommodation_unit
- accommodation_floor
- accommodation_building

**Asset Management:**
- accommodation_asset
- accommodation_asset_and_consumable
- accommodation_distribution_asset
- accommodation_distribution_consumable

**Check-in/Check-out:**
- accommodation_checkin_checkout
- bed_assignment
- bed_assignment_record

**Inspection & Maintenance:**
- accommodation_inspection
- accommodation_inspection_template
- accommodation_inspection_parameter
- accommodation_building_condition

**Meters & Utilities:**
- accommodation_meter
- accommodation_meter_reading
- accommodation_meter_reading_record

**Objects & Categories:**
- accommodation_object
- accommodation_object_category

**Migration Strategy for Accommodation:**
```
frappe_ticktix/plugins/accommodation/
├── units/             # Accommodation units
├── checkin/           # Check-in/out process
├── assets/            # Asset management
├── inspection/        # Quality inspection
└── utilities/         # Meter readings
```

---

## 📂 CATEGORY 5: GOVERNMENT RELATIONS & COMPLIANCE (Kuwait)

### **Priority: MEDIUM** | **Estimated Effort: 6-8 weeks**

#### GRD Module (grd/) - Government Relations
**45 Doctypes - Kuwait-specific:**

**PACI (Public Authority for Civil Information):**
- paci_transaction
- moi_residency_jawazat
- civil_id_application

**Labor & Immigration:**
- work_permit
- residency_visa
- visa_application
- visa_extension

**Business Licenses:**
- moci_license (Ministry of Commerce)
- article_of_association
- commercial_license

**Insurance & Medical:**
- medical_insurance
- health_insurance_provider_detail
- medical_insurance_item

**Payroll Compliance:**
- pam_salary_certificate
- pifss_monthly_deduction
- form_55_employees

**Fingerprinting:**
- fingerprint_appointment
- fingerprint_appointment_settings

**Migration Strategy for GRD:**
```
frappe_ticktix/plugins/compliance/
├── paci/              # PACI integration
├── visas/             # Visa management
├── licenses/          # Business licenses
├── insurance/         # Medical insurance
└── labor/             # Labor compliance
```

**Note:** This module is Kuwait-specific. May not be needed if targeting different region.

---

## 📂 CATEGORY 6: FLEET MANAGEMENT

### **Priority: MEDIUM** | **Estimated Effort: 2-3 weeks**

#### Fleet Management Module (fleet_management/)
**6 Doctypes:**

**Vehicle Management:**
- vehicle
- vehicle_log
- vehicle_service

**Driver Management:**
- driver
- driver_assignment
- driver_log

**Migration Strategy for Fleet:**
```
frappe_ticktix/plugins/fleet/
├── vehicles/          # Vehicle management
├── drivers/           # Driver management
└── maintenance/       # Service & maintenance
```

---

## 📂 CATEGORY 7: PURCHASE & PROCUREMENT

### **Priority: MEDIUM** | **Estimated Effort: 4-5 weeks**

#### Purchase Module (purchase/)
**38 Doctypes:**

**Procurement Process:**
- purchase_request
- purchase_order (customized)
- supplier_quotation
- request_for_quotation

**Supplier Management:**
- supplier (customized)
- supplier_evaluation
- supplier_scorecard

**Stock & Inventory:**
- stock_entry (customized)
- material_request (customized)
- delivery_note (customized)

**Subcontracting:**
- subcontract_order
- subcontract_receipt
- subcontract_service

**Migration Strategy for Purchase:**
```
frappe_ticktix/plugins/procurement/
├── requests/          # Purchase requests
├── orders/            # Purchase orders
├── suppliers/         # Supplier management
└── stock/             # Inventory management
```

---

## 📂 CATEGORY 8: LEGAL & COMPLIANCE

### **Priority: LOW** | **Estimated Effort: 2-3 weeks**

#### Legal Module (legal/)
**19 Doctypes:**

**Legal Cases:**
- legal_case
- legal_case_type
- legal_case_status

**Investigations:**
- investigation
- investigation_type
- investigation_findings

**Documentation:**
- legal_document
- legal_agreement
- legal_notice

**Migration Strategy for Legal:**
```
frappe_ticktix/plugins/legal/
├── cases/             # Legal cases
├── investigations/    # Investigations
└── documents/         # Legal documents
```

---

## 📂 CATEGORY 9: ASSETS & INVENTORY

### **Priority: LOW** | **Estimated Effort: 2-3 weeks**

#### Assets Module (one_fm_assets/)
**4 Doctypes:**

**Asset Management:**
- asset (customized)
- asset_category
- asset_maintenance
- asset_movement

**Migration Strategy for Assets:**
```
frappe_ticktix/plugins/assets/
├── tracking/          # Asset tracking
├── maintenance/       # Asset maintenance
└── movement/          # Asset transfers
```

---

## 📂 CATEGORY 10: UNIFORM MANAGEMENT

### **Priority: LOW** | **Estimated Effort: 1-2 weeks**

#### Uniform Module (uniform_management/)
**5 Doctypes:**

**Uniform Distribution:**
- uniform_request
- uniform_issue
- uniform_return
- uniform_item
- uniform_type

**Migration Strategy for Uniforms:**
```
frappe_ticktix/plugins/operations/uniforms/
├── requests/          # Uniform requests
├── distribution/      # Issue & return
└── inventory/         # Uniform stock
```

---

## 📂 CATEGORY 11: SUPPORT MODULES

### **Priority: VARIES**

#### API & Integration (api/)
**9 Python files:**
- API endpoints
- Mobile app integration
- Third-party integrations
- Webhook handlers

#### Configuration (config/)
**14 Python files:**
- Desktop configurations
- Module settings
- Workspace definitions
- Permission setups

#### Developer Tools (developer/)
**12 Doctypes:**
- Bug tracking
- Feature requests
- Development tasks
- Testing tools

---

## 📈 MIGRATION PRIORITY MATRIX

### **PHASE 1: FOUNDATION (Weeks 1-6) - CRITICAL**
Priority: **MUST HAVE**

1. **HR Core** (4 weeks)
   - Employee management
   - Basic attendance
   - Shift management
   - Leave basics

2. **Operations Core** (2 weeks)
   - Site management
   - Basic roster
   - Post/Role setup

**Deliverable:** Basic employee management & operations

---

### **PHASE 2: CORE OPERATIONS (Weeks 7-16) - HIGH**
Priority: **SHOULD HAVE**

3. **Advanced Operations** (4 weeks)
   - Checkpoints & patrols
   - Cleaning schedules
   - Maintenance

4. **Recruitment** (3 weeks)
   - Job openings
   - Candidate management
   - Onboarding

5. **Accommodation** (3 weeks)
   - Unit management
   - Check-in/out
   - Asset tracking

**Deliverable:** Full operational capability

---

### **PHASE 3: BUSINESS OPERATIONS (Weeks 17-26) - MEDIUM**
Priority: **NICE TO HAVE**

6. **Payroll** (4 weeks)
   - Salary processing
   - Payroll reports
   - Deductions

7. **Procurement** (3 weeks)
   - Purchase requests
   - PO processing
   - Supplier management

8. **Fleet** (2 weeks)
   - Vehicle tracking
   - Driver management

**Deliverable:** Complete business operations

---

### **PHASE 4: COMPLIANCE & EXTRAS (Weeks 27-36) - LOW**
Priority: **OPTIONAL**

9. **Government Relations** (4 weeks)
   - PACI integration (if Kuwait)
   - Visa management
   - Licenses

10. **Legal & Compliance** (2 weeks)
    - Case management
    - Investigations

11. **Assets & Uniforms** (3 weeks)
    - Asset tracking
    - Uniform distribution

**Deliverable:** Full featured system

---

## 📊 TOTAL EFFORT ESTIMATION

| Phase | Duration | Features | Complexity | Team Size |
|-------|----------|----------|------------|-----------|
| Phase 1 | 6 weeks | 2 modules | High | 2-3 devs |
| Phase 2 | 10 weeks | 3 modules | Medium-High | 2-3 devs |
| Phase 3 | 10 weeks | 3 modules | Medium | 2 devs |
| Phase 4 | 10 weeks | 3 modules | Medium | 1-2 devs |
| **TOTAL** | **36 weeks** | **11 modules** | - | **~9 months** |

**With 1 developer:** ~18 months  
**With 2 developers:** ~9-12 months  
**With 3 developers:** ~6-9 months

---

## 🎯 RECOMMENDED APPROACH

### **Option A: Minimal Viable Product (MVP)**
**Timeline:** 3 months  
**Features:** Phase 1 + Selected Phase 2  
- HR Core (Employee, Attendance, Shifts, Leave)
- Operations Core (Sites, Roster, Basic scheduling)
- Basic Recruitment

**Best for:** Quick start, prove concept

### **Option B: Core System**
**Timeline:** 6 months  
**Features:** Phase 1 + Phase 2  
- Complete HR & Operations
- Recruitment & Onboarding
- Accommodation Management

**Best for:** Full operational capability

### **Option C: Complete System**
**Timeline:** 9-12 months  
**Features:** All 4 Phases  
- Everything from one_fm
- Fully featured facility management

**Best for:** Complete replacement

---

## 📝 NEXT STEPS

1. ✅ **Choose Approach:** MVP / Core / Complete?
2. ✅ **Select First Module:** Which Phase 1 feature to start?
3. ✅ **Review Architecture:** Confirm plugin structure
4. ✅ **Start Implementation:** Build first feature

**Created:**
- ✅ This feature inventory document
- 🔄 Next: Detailed migration plan
- 🔄 Next: Implementation strategy

---

*Complete feature analysis - Ready for migration planning*
