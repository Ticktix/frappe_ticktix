# one_fm to frappe_ticktix Migration Documentation

**Last Updated:** October 20, 2025  
**Project:** frappe_ticktix Facility Management System  
**Source:** one_fm (500+ doctypes across 36 modules)

---

## 📚 Documentation Index

This folder contains all documentation related to migrating features from one_fm to frappe_ticktix.

### **Core Documents**

1. **[COMPLETE_MIGRATION_GUIDE.md](./COMPLETE_MIGRATION_GUIDE.md)** ⭐ **START HERE**
   - Complete consolidated guide with all migration information
   - Feature inventory, priorities, timeline, implementation strategy
   - Single source of truth for the entire migration

2. **[ONE_FM_FEATURE_INVENTORY.md](./ONE_FM_FEATURE_INVENTORY.md)**
   - Detailed feature categorization of all one_fm modules
   - 11 categories with effort estimates
   - Phase-by-phase migration priorities

3. **[HR_MIGRATION_PLAN.md](./HR_MIGRATION_PLAN.md)**
   - Specific plan for HR feature migration
   - Step-by-step migration process
   - First feature recommendations

4. **[HR_MIGRATION_STRATEGY.md](./HR_MIGRATION_STRATEGY.md)**
   - Strategic approach to HR migration
   - Why not install one_fm directly
   - Quick start guide

---

## 🎯 Quick Navigation

### **For Project Managers:**
→ Read [COMPLETE_MIGRATION_GUIDE.md](./COMPLETE_MIGRATION_GUIDE.md) - Section: "Migration Priority Matrix"

### **For Developers:**
→ Read [COMPLETE_MIGRATION_GUIDE.md](./COMPLETE_MIGRATION_GUIDE.md) - Section: "Implementation Strategy"

### **For Product Owners:**
→ Read [ONE_FM_FEATURE_INVENTORY.md](./ONE_FM_FEATURE_INVENTORY.md) - Section: "Recommended Approach"

### **For HR Team:**
→ Read [HR_MIGRATION_PLAN.md](./HR_MIGRATION_PLAN.md)

---

## 📊 Migration Overview

### **Source: one_fm**
- **Total Modules:** 36
- **Total Doctypes:** ~468
- **Main Categories:** HR, Operations, Accommodation, Fleet, Legal, Procurement

### **Target: frappe_ticktix**
- **Architecture:** Plugin-based
- **Existing Plugins:** Authentication, Branding
- **New Plugins:** HR, Operations, Accommodation, Fleet, etc.

### **Migration Approach:**
✅ **Option 1 Selected:** Build fresh in frappe_ticktix  
- Extract features from one_fm
- Rebuild in plugin architecture
- Incremental, tested migration

---

## 🚀 Getting Started

### **Step 1: Choose Your Approach**
- **MVP** (3 months) - HR Core + Operations Core
- **Core System** (6 months) - Full operational capability
- **Complete System** (9-12 months) - Everything from one_fm

### **Step 2: Read the Complete Guide**
Open [COMPLETE_MIGRATION_GUIDE.md](./COMPLETE_MIGRATION_GUIDE.md)

### **Step 3: Start Implementation**
Follow the implementation strategy in the complete guide

---

## 📈 Migration Status

| Phase | Status | Timeline | Features |
|-------|--------|----------|----------|
| **Phase 1** | 🔄 Planning | Weeks 1-6 | HR Core, Operations Core |
| **Phase 2** | ⏳ Pending | Weeks 7-16 | Advanced Operations, Recruitment, Accommodation |
| **Phase 3** | ⏳ Pending | Weeks 17-26 | Payroll, Procurement, Fleet |
| **Phase 4** | ⏳ Pending | Weeks 27-36 | Compliance, Legal, Assets |

---

## 🔗 Related Resources

### **In frappe_ticktix:**
- `apps/frappe_ticktix/hooks.py` - Plugin registration
- `apps/frappe_ticktix/plugins/` - Existing plugin structure
- `apps/frappe_ticktix/docs/CONFIGURATION_SUMMARY.md` - Current system config

### **In one_fm:**
- `apps/one_fm/one_fm/` - Source modules
- `apps/one_fm/one_fm/overrides/` - ERPNext customizations

---

## 📞 Support

For questions about this migration:
1. Read the [COMPLETE_MIGRATION_GUIDE.md](./COMPLETE_MIGRATION_GUIDE.md)
2. Check specific feature docs (HR_MIGRATION_PLAN.md, etc.)
3. Review one_fm source code in `apps/one_fm/`

---

*All migration documentation consolidated and organized for easy reference.*
