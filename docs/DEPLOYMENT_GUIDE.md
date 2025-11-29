# Frappe TickTix - Deployment Guide

## Overview

This guide covers deploying frappe_ticktix app updates to existing production sites. The app uses Frappe's standard migration hooks, so deployment follows the same pattern as ERPNext/HRMS.

## Standard Deployment Process

### For Existing Sites

```bash
# 1. Pull latest code
cd /path/to/bench
git pull

# 2. Update bench (if needed)
bench update --patch

# 3. Migrate site(s)
bench --site [site-name] migrate

# 4. Restart services
bench restart
```

**That's it!** The `after_migrate` hook will automatically:
- ✅ Create/update custom fields
- ✅ Update status options
- ✅ Install client scripts
- ✅ Apply all HR customizations

### For Fresh Installations

```bash
# 1. Install app
bench get-app frappe_ticktix [git-url]
bench --site [site-name] install-app frappe_ticktix

# 2. That's it!
# after_install hook runs setup automatically
```

## What Happens During Migration

The `after_migrate` hook in `hooks.py` triggers:

```python
after_migrate = "frappe_ticktix.install.after_migrate"
```

This runs `install.after_migrate()` which calls `setup_hr_customizations()`:

1. **Custom Fields Creation** (`create_attendance_custom_fields()`)
   - 21 custom fields for Attendance doctype
   - Idempotent (safe to run multiple times)
   - Uses `update=True` to update existing fields

2. **Status Options Update** (`customize_attendance_status()`)
   - Adds 9 status options (vs default 5)
   - Present, Absent, On Leave, Half Day, Work From Home
   - Weekly Off, Client Day Off, Holiday, On Hold

3. **Client Scripts Installation** (`install_attendance_client_scripts()`)
   - Attendance Status Override - Mark Attendance Dialog
   - Attendance Status Override - Employee Attendance Tool

## Attendance Module Features

### Custom Fields (21 fields)

**Operations Section:**
- `operations_shift` (Data) - Operations shift reference
- `site` (Data) - Work site/location
- `project` (Link to Project) - Project for billing
- `operations_role` (Data) - Employee role at site

**Roster & Overtime:**
- `roster_type` (Select) - Basic or Over-Time
- `day_off_ot` (Check) - Worked on day off flag
- `post_abbrv` (Data) - Role abbreviation
- `sale_item` (Data) - Sales item for billing

**Integration:**
- `timesheet` (Link to Timesheet)
- `reference_doctype` (Link)
- `reference_name` (Dynamic Link)

**Tracking:**
- `employee_type` (Link to Employment Type)
- `is_unscheduled` (Check) - Employee without shift

**Comments:**
- `attendance_comments` (Small Text)

Plus 7 section/column breaks for layout.

### Extended Status Options

| Status | Description | Use Case |
|--------|-------------|----------|
| Present | Employee worked | Standard attendance |
| Absent | Employee didn't show | No checkin |
| On Leave | Approved leave | Leave management |
| Half Day | Worked partial day | Half-day attendance |
| Work From Home | Remote work | WFH policy |
| **Weekly Off** | Scheduled day off | Not worked |
| **Client Day Off** | Client-requested off | Operations |
| **Holiday** | Public/company holiday | Not worked |
| **On Hold** | Temporary suspension | Operations |

*Bold = New additions*

### Scheduler Tasks

**Daily Tasks** (configured in `scheduler_events`):
- `mark_absent_for_missing_checkins` - Mark absent for no-shows
- `mark_attendance_for_unscheduled_employees` - Handle employees without shifts
- `remark_for_active_employees` - Fix incorrect Absent records

### API Endpoints

**Attendance Management:**
- `mark_attendance` - Manual attendance marking
- `mark_bulk_attendance` - Date range processing
- `get_attendance_summary` - Summary statistics
- `get_status_options_for_client` - Available status options

## Validation & Business Logic

### Enhanced Validations

1. **Overlapping Shift Prevention**
   - Prevents multiple attendance records for same employee+date+shift combination
   - Checks timing overlaps for different shifts on same day
   - Validates roster_type (Basic vs Over-Time)

2. **Status-Specific Working Hours**
   - Present/Work From Home: Requires working_hours
   - Weekly Off/Holiday/Day Off: Can have 0 hours
   - Flexible validation based on status

3. **Duplicate Prevention**
   - Employee + Date + Roster Type uniqueness
   - Extends Frappe's default Employee + Date check

### Auto-Population

**Operations Fields** (`populate_operations_fields()`):
- Automatically fills site/project/role from shift assignment
- Gracefully handles missing Operations doctypes
- Only updates if shift assignment exists

**Day Off OT Tracking** (`set_day_off_ot()`):
- Auto-detects work on day off
- Sets flag for payroll processing
- Based on Employee schedule

## Troubleshooting

### Custom Fields Not Appearing

```bash
# Option 1: Re-run migration
bench --site [site-name] migrate

# Option 2: Clear cache and retry
bench --site [site-name] clear-cache
bench --site [site-name] migrate

# Option 3: Manual execution (emergency)
bench --site [site-name] execute frappe_ticktix.setup_attendance_fields.run
```

### Attendance Save Errors

**Error:** `Unknown column 'tabAttendance.roster_type'`

**Solution:** Custom fields not created. Run migration:
```bash
bench --site [site-name] migrate
```

**Error:** `ModuleNotFoundError: attendance_manager.AttendanceOverride`

**Solution:** Old hooks configuration. Fixed in latest version. Update code:
```bash
git pull
bench restart
```

### Status Options Not Showing

**Check:** Property Setter exists
```bash
bench --site [site-name] console
>>> frappe.db.exists('Property Setter', {'doc_type': 'Attendance', 'field_name': 'status'})
```

**Fix:** Re-run customization
```bash
bench --site [site-name] execute frappe_ticktix.install.setup_hr_customizations
```

## Rollback (Emergency)

If you need to rollback custom fields:

```bash
# 1. Delete all custom fields
bench --site [site-name] execute "import frappe; [frappe.delete_doc('Custom Field', cf.name) for cf in frappe.get_all('Custom Field', filters={'dt': 'Attendance'})]"

# 2. Remove Property Setter
bench --site [site-name] execute "import frappe; frappe.delete_doc('Property Setter', 'Attendance-status-options') if frappe.db.exists('Property Setter', 'Attendance-status-options') else None"

# 3. Clear cache
bench --site [site-name] clear-cache

# 4. Reload doctype
bench --site [site-name] execute "import frappe; frappe.reload_doctype('Attendance')"
```

## Architecture Notes

### Why after_migrate Instead of Fixtures?

**Fixtures** are static JSON files loaded once. **after_migrate** is dynamic:

✅ **Advantages:**
- Updates existing fields (fixtures don't)
- Handles conditional logic
- More flexible than static JSON
- Industry standard (used by HRMS)

✅ **Idempotent:**
- Safe to run multiple times
- Won't create duplicates
- Updates changed definitions

✅ **Production Ready:**
- Zero manual intervention
- Works on fresh installs
- Works on existing sites
- Works on app updates

### Integration with Frappe HRMS

**What Frappe Already Has:**
- Auto-attendance via Shift Type
- Late entry/early exit detection
- Working hours calculation
- 5 standard status options

**What We Add:**
- 4 additional status options (9 total)
- Operations tracking (21 custom fields)
- Multi-roster support (Basic/OT)
- Unscheduled employee handling
- Error correction (remark logic)
- Bulk processing APIs

**What We Override:**
- `validate()` - Add 9-status support
- `validate_duplicate_record()` - Add roster_type
- `validate_working_hours()` - Status-specific rules

**What We Extend:**
- `before_save()` - Auto-populate operations
- `after_insert()` - Set day_off_ot flag

## Version Compatibility

- **Frappe:** v15.82.1+
- **ERPNext:** v15.80.0+
- **HRMS:** v15.50.0+

## Support

For issues or questions:
1. Check this guide first
2. Review error logs: `bench --site [site-name] logs`
3. Clear cache and retry
4. Contact development team

## Summary

**Key Points:**
- ✅ Migration is automatic via `bench migrate`
- ✅ No manual steps required for deployments
- ✅ Follows Frappe/ERPNext/HRMS patterns
- ✅ Production-ready and battle-tested
- ✅ Idempotent and safe to re-run

**Deployment Checklist:**
- [ ] `git pull` to get latest code
- [ ] `bench migrate` to apply changes
- [ ] `bench restart` to reload services
- [ ] Test attendance creation in UI
- [ ] Verify custom fields visible
- [ ] Check scheduler tasks running

That's it! The app is designed for zero-friction deployments. 🚀
