"""
Attendance Status Override Plugin

This module extends Frappe HRMS Attendance to support additional status options:
- Day Off
- Holiday  
- Weekly Off

It overrides hardcoded status validations in the core HRMS module.
"""

import frappe
from frappe import _


def get_attendance_status_options():
	"""
	Get complete list of attendance status options.
	Reads from Property Setter if customized, otherwise returns extended list.
	
	Based on one_fm status options with name change:
	- Weekly Off (renamed from one_fm's "Day Off" - company-assigned weekly off)
	- Client Day Off (client-requested day off, billable)
	- Holiday (from Holiday List)
	- On Hold (pending client approval for billing)
	
	Returns:
		list: List of valid attendance status options
	"""
	# Try to get from Property Setter first (if customized via Customize Form)
	property_setter = frappe.db.get_value(
		"Property Setter",
		{
			"doc_type": "Attendance",
			"field_name": "status",
			"property": "options"
		},
		"value"
	)
	
	if property_setter:
		# Property Setter exists, use its options
		options = [opt.strip() for opt in property_setter.split('\n') if opt.strip()]
		return options
	
	# Fallback to extended default list (based on one_fm)
	return [
		"Present",
		"Absent", 
		"On Leave",
		"Half Day",
		"Work From Home",
		"Weekly Off",        # Company-assigned weekly off (one_fm's "Day Off")
		"Client Day Off",    # Client-requested day off (billable)
		"Holiday",           # From Holiday List
		"On Hold"            # Pending client approval
	]


def validate_attendance_status(status):
	"""
	Validate if the given status is in the list of allowed attendance statuses.
	
	Args:
		status (str): The attendance status to validate
		
	Raises:
		frappe.ValidationError: If status is not in allowed list
	"""
	allowed_statuses = get_attendance_status_options()
	
	if status not in allowed_statuses:
		frappe.throw(
			_("Invalid Attendance Status: {0}. Must be one of: {1}").format(
				frappe.bold(status),
				", ".join(allowed_statuses)
			),
			title=_("Invalid Status")
		)


def override_attendance_validate(doc, method=None):
	"""
	Override validate method for Attendance doctype.
	Replaces hardcoded status validation with dynamic validation.
	
	This is called via doc_events hook in hooks.py:
	doc_events = {
		"Attendance": {
			"validate": "frappe_ticktix.plugins.hr.attendance.attendance_status_override.override_attendance_validate"
		}
	}
	
	Args:
		doc: Attendance document
		method: Method name (from hook)
	"""
	# Validate status using our extended list
	validate_attendance_status(doc.status)
	
	frappe.logger().debug(f"Attendance status validated: {doc.status}")


@frappe.whitelist()
def get_status_options_for_client():
	"""
	API endpoint to get attendance status options for client-side JavaScript.
	Used by custom scripts to populate status dropdowns dynamically.
	
	Returns:
		list: List of attendance status options
	"""
	return get_attendance_status_options()


def get_status_options_string():
	"""
	Get attendance status options as newline-separated string.
	Useful for Select field options format.
	
	Returns:
		str: Newline-separated status options
	"""
	return '\n'.join(get_attendance_status_options())
