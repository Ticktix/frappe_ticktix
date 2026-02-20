"""
Counter Management Module

Handles counter generation with auto-detected scoping
"""

import frappe
from typing import Dict, Any, Optional


class CounterManager:
    """Manages employee ID counters with auto-detected scoping"""
    
    COUNTER_TABLE = "employee_id_counter"  # Custom table for storing counters
    COUNTER_PREFIX = "EMP_ID"
    
    def __init__(self, settings: Dict[str, Any]):
        """
        Initialize counter manager
        
        Args:
            settings: hr_employee_id_settings from config
        """
        self.settings = settings
        self._ensure_table_exists()
    
    def _ensure_table_exists(self):
        """
        Ensure the counter table exists in the database
        Creates it if it doesn't exist
        """
        table_name = self.COUNTER_TABLE
        
        # Check if table exists
        if frappe.db.exists(f"SELECT 1 FROM information_schema.TABLES WHERE TABLE_SCHEMA = '{frappe.conf.db_name}' AND TABLE_NAME = '{table_name}'"):
            return
        
        # Create table if it doesn't exist
        try:
            frappe.db.sql(f"""
                CREATE TABLE IF NOT EXISTS `{table_name}` (
                    `name` VARCHAR(255) PRIMARY KEY,
                    `counter` INT NOT NULL DEFAULT 0,
                    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX (`name`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            frappe.db.commit()
        except Exception as e:
            frappe.log_error(f"Error creating counter table: {str(e)}", "Employee ID Counter")
            # Table might already exist, continue anyway
    
    def get_next_counter(self, scope_key: str) -> int:
        """
        Get next counter value for a scope
        Auto-initializes from existing employee IDs on first use to continue from maximum
        
        Args:
            scope_key: Scope identifier (e.g., "global" or "dept:IT:year:2025")
        
        Returns:
            Next counter value
        """
        # Build series name
        series_name = self._build_series_name(scope_key)
        
        try:
            # Check if counter exists - if not, initialize from existing employee IDs
            current = frappe.db.get_value(self.COUNTER_TABLE, series_name, "counter")
            
            if current is None:
                # First time - determine starting counter value
                # Priority: 1) Existing IDs, 2) counter_start setting, 3) Default (0)
                max_counter = self._get_max_existing_counter(scope_key)
                
                if max_counter > 0:
                    # Initialize counter to the maximum found from existing data
                    initial_counter = max_counter
                    frappe.db.sql(f"""
                        INSERT INTO `{self.COUNTER_TABLE}` (`name`, `counter`)
                        VALUES (%s, %s)
                    """, (series_name, initial_counter))
                    frappe.db.commit()
                    frappe.msgprint(
                        f"Employee ID counter initialized from existing data. Starting from {initial_counter + 1}.",
                        alert=True,
                        indicator="blue"
                    )
                else:
                    # No existing IDs found - check for custom starting value
                    counter_start = self.settings.get("counter_start", 0)
                    if counter_start > 0:
                        # Use custom starting value (minus 1 because we'll increment it)
                        initial_counter = counter_start - 1
                        frappe.db.sql(f"""
                            INSERT INTO `{self.COUNTER_TABLE}` (`name`, `counter`)
                            VALUES (%s, %s)
                        """, (series_name, initial_counter))
                        frappe.db.commit()
                        frappe.msgprint(
                            f"Employee ID counter initialized to start from {counter_start}.",
                            alert=True,
                            indicator="green"
                        )
            
            # Use INSERT ... ON DUPLICATE KEY UPDATE for atomic counter increment
            frappe.db.sql(f"""
                INSERT INTO `{self.COUNTER_TABLE}` (`name`, `counter`)
                VALUES (%s, 1)
                ON DUPLICATE KEY UPDATE `counter` = `counter` + 1
            """, (series_name,))
            frappe.db.commit()
            
            # Get the updated counter value using direct SQL
            result = frappe.db.sql(f"""
                SELECT `counter` FROM `{self.COUNTER_TABLE}` WHERE `name` = %s
            """, (series_name,), as_dict=False)
            
            if result and result[0]:
                return int(result[0][0])
            else:
                return 1
            
        except Exception as e:
            frappe.log_error(f"Error getting counter for {series_name}: {str(e)}", "Employee ID Counter")
            raise
    
    def preview_counter(self, scope_key: str) -> int:
        """
        Preview what the next counter would be WITHOUT incrementing
        
        Args:
            scope_key: Scope identifier
        
        Returns:
            Next counter value (preview only)
        """
        series_name = self._build_series_name(scope_key)
        
        try:
            current = frappe.db.get_value(self.COUNTER_TABLE, series_name, "counter")
            if current is None:
                return 1
            return int(current) + 1
        except Exception:
            return 1
    
    def _build_series_name(self, scope_key: str) -> str:
        """
        Build series name from scope key
        
        Args:
            scope_key: Scope identifier
        
        Returns:
            Series name for Frappe Series doctype
        """
        # Format: EMP_ID.{scope_key}
        # Examples:
        # - EMP_ID.global
        # - EMP_ID.dept.IT
        # - EMP_ID.company.TTX.year.2025
        
        # Replace : with . for Frappe series naming
        normalized_key = scope_key.replace(":", ".")
        
        return f"{self.COUNTER_PREFIX}.{normalized_key}"
    
    def build_scope_key(self, scope_components: Dict[str, Any], component_values: Dict[str, str]) -> str:
        """
        Build scope key from components
        
        Args:
            scope_components: Dict from token_resolver.extract_scope_components()
            component_values: Dict from token_resolver.get_scope_key_components()
        
        Returns:
            Scope key string
        """
        entities = scope_components.get("entities", [])
        temporal = scope_components.get("temporal")
        
        # If no entities and no temporal, it's global
        if not entities and not temporal:
            return "global"
        
        # Build key parts
        key_parts = []
        
        # Add entity components in consistent order
        entity_order = ["company", "department", "branch", "employment_type"]
        for entity in entity_order:
            if entity in entities:
                value = component_values.get(entity)
                if value:
                    # Sanitize value (remove special characters)
                    sanitized = self._sanitize_key_component(value)
                    key_parts.append(f"{entity}:{sanitized}")
        
        # Add temporal component
        if temporal == "monthly":
            month = component_values.get("month")
            if month:
                key_parts.append(f"month:{month}")
        elif temporal == "yearly":
            year = component_values.get("year")
            if year:
                key_parts.append(f"year:{year}")
        
        # Join parts
        if not key_parts:
            return "global"
        
        return ":".join(key_parts)
    
    def _sanitize_key_component(self, value: str) -> str:
        """
        Sanitize a component value for use in scope key
        
        Args:
            value: Component value
        
        Returns:
            Sanitized value (alphanumeric and underscores only)
        """
        import re
        # Replace spaces and special chars with underscore
        sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', value)
        # Remove consecutive underscores
        sanitized = re.sub(r'_+', '_', sanitized)
        # Remove leading/trailing underscores
        sanitized = sanitized.strip('_')
        return sanitized
    
    def _get_max_existing_counter(self, scope_key: str) -> int:
        """
        Scan existing employee IDs and find the maximum counter value
        This ensures we continue from the highest existing ID instead of gap-filling
        
        Args:
            scope_key: Scope identifier
        
        Returns:
            Maximum counter value found, or 0 if none
        """
        import re
        
        pattern = self.settings.get("pattern", "")
        if not pattern:
            return 0
        
        try:
            # Get all existing employee numbers
            employees = frappe.get_all(
                "Employee",
                fields=["employee_number"],
                filters={"employee_number": ["is", "set"]}
            )
            
            if not employees:
                return 0
            
            # Extract the counter pattern from the full pattern
            # e.g., "icsp####" -> counter is {####}
            counter_match = re.search(r'\{(#+)\}', pattern)
            if not counter_match:
                return 0
            
            counter_token = counter_match.group(0)  # e.g., "{####}"
            counter_length = len(counter_match.group(1))  # e.g., 4
            
            # Build a regex pattern to extract the counter from employee IDs
            # Replace {####} with (\d+) and escape other special characters
            escaped_pattern = re.escape(pattern)
            # Unescape the counter token
            escaped_pattern = escaped_pattern.replace(re.escape(counter_token), r'(\d+)')
            # Replace other token placeholders with wildcards
            escaped_pattern = re.sub(r'\\\{[^}]+\\\}', r'.*?', escaped_pattern)
            
            max_counter = 0
            
            for emp in employees:
                emp_id = emp.get("employee_number", "")
                if not emp_id:
                    continue
                
                # Try to extract counter from employee ID
                match = re.match(escaped_pattern, emp_id)
                if match:
                    try:
                        counter_value = int(match.group(1))
                        max_counter = max(max_counter, counter_value)
                    except (ValueError, IndexError):
                        continue
            
            if max_counter > 0:
                frappe.log_error(
                    f"Counter auto-initialization: Found maximum employee ID counter = {max_counter} for pattern '{pattern}'",
                    "Employee ID Counter Init"
                )
            
            return max_counter
            
        except Exception as e:
            frappe.log_error(
                f"Error scanning existing employee IDs: {str(e)}. Starting counter from 0.",
                "Employee ID Counter Init"
            )
            return 0


def get_counter_manager(settings: Dict[str, Any]) -> CounterManager:
    """Factory function to create CounterManager instance"""
    return CounterManager(settings)
