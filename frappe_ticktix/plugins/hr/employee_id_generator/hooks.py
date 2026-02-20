"""
Frappe Hooks for Employee ID Generation

Hooks into Employee doctype lifecycle
"""

import frappe
from .id_generator import generate_employee_id
from .validators import validate_employee_id


def before_insert_employee(doc, method):
    """
    Hook: before_insert for Employee doctype
    Generates employee ID if auto-generation is enabled
    
    Args:
        doc: Employee document
        method: Hook method name (unused)
    """
    try:
        generate_employee_id(doc, method)
    except Exception as e:
        frappe.log_error(
            f"Error in before_insert_employee hook: {str(e)}",
            "Employee ID Generation"
        )
        # Re-raise to prevent employee creation if ID generation fails
        raise


def validate_employee(doc, method):
    """
    Hook: validate for Employee doctype
    Validates employee ID uniqueness
    
    Args:
        doc: Employee document
        method: Hook method name (unused)
    """
    try:
        validate_employee_id(doc)
    except Exception as e:
        frappe.log_error(
            f"Error in validate_employee hook: {str(e)}",
            "Employee ID Validation"
        )
        # Re-raise to show validation error
        raise
