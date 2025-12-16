# HR Module Documentation Guide

**Purpose:** Compare Frappe defaults with our overrides

---

## 📚 Navigation

1. **`00_INDEX.md`** - Overview & statistics
2. **`01_employee_checkin_override.md`** - Checkin module
3. **`02_attendance_override.md`** - Attendance module
4. **This file** - How to use

---

## 🎯 What This Shows

✅ What Frappe HRMS provides  
✅ What we've overridden  
✅ What features we added  
❌ NOT implementation details (see actual code)

---

## 📖 Symbol Legend

- ✅ = Has feature
- ❌ = Missing
- ⚠️ = Partial
- 🔵 = Frappe default
- 🟢 = Our override

---

## 🔍 Quick Reference

| Need | Document |
|------|----------|
| Overview | `00_INDEX.md` |
| APIs | `00_INDEX.md` |
| Checkin details | `01_employee_checkin_override.md` |
| Attendance details | `02_attendance_override.md` |

---

## 🛠️ For Developers

**Code locations:**
- Checkin: `frappe_ticktix/plugins/hr/checkin/`
- Attendance: `frappe_ticktix/plugins/hr/attendance/`
- Hooks: `frappe_ticktix/hooks.py`

**Integration:** Document event hooks (no core modifications)

---

*Last Updated: October 25, 2025*
