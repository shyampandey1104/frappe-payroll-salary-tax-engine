# Frappe & ERPNext Automated Payroll Engine (Bina Excel Ke)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Frappe Framework](https://img.shields.io/badge/frappe-v14%20%7C%20v15-orange.svg)](https://frappe.io)
[![ERPNext Payroll](https://img.shields.io/badge/erpnext-Payroll%20Engine-teal.svg)](https://erpnext.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![India Ready](https://img.shields.io/badge/India%20Statutory-PF%20%7C%20ESI%20%7C%20PT%20%7C%20TDS-darkgreen.svg)]()
[![Coverage: 100%](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)]()

> **"Salary Processing, bina Excel ke — Ek click mein poore staff ki salary slip"**  
> Comprehensive statutory payroll engine for Frappe & ERPNext calculating employee salary slips, formula-based components, Indian statutory deductions (PF, ESI, Professional Tax, TDS), and automated bank disbursement entries.

---

## 🎯 The Real-World Client Problem & Business Context

Managing payroll in Excel sheets creates operational bottlenecks and compliance nightmares:
1. **Excel Calculation Glitches & Formula Errors:** Human errors in formulas result in overpaid salaries, incorrect tax deductions, or missed statutory deductions that attract heavy interest.
2. **Statutory Non-Compliance Penalties:** Incorrect Provident Fund (PF) calculations under EPFO guidelines or failure to deduct ESI and Professional Tax leads to severe labour department fines.
3. **Manual Bank Transfer Preparation:** Finance teams spend days re-entering salary figures from spreadsheets into corporate banking portals (HDFC, ICICI, SBI), risking duplicate transfers.

**This engine automates the 8-step standard ERPNext payroll flow:** It connects employee attendance records to formula-driven salary structures, executes bulk payroll processing by branch/department, generates bilingual salary slips, and posts automated Bank Payment Journal Entries.

---

## 🏗️ Standard ERPNext Payroll Workflow Flow

```mermaid
flowchart LR
    1[1. Salary Component] --> 2[2. Salary Structure]
    2 --> 3[3. Structure Assignment]
    3 --> 4[4. Attendance & Leave]
    4 --> 5[5. Payroll Entry]
    5 --> 6[6. Salary Slip]
    6 --> 7[7. Bank Entry]
    7 --> 8[8. Disbursed Payment]
```

---

## ⚙️ Key Enterprise Features & Capabilities

- **Formula-Based Salary Components:** Define earnings (Basic, HRA, Conveyance, Special Allowance) and deductions using dynamic Python expressions.
- **Flexible Salary Structures:** Assign custom salary templates per employee, grade, branch, or designation with automatic proration for mid-month joiners.
- **Bulk Payroll Entry:** Process salary slips for hundreds of employees across multiple branches in a single click based on approved monthly attendance.
- **Salary Slip Generation:** Automated computation of payable days, Loss of Pay (LOP) deductions, email dispatch, and tamper-proof PDF generation.
- **Additional Salary & Arrears:** Seamless handling of performance bonuses, sales incentives, one-time allowances, and salary arrears.
- **Loans & Salary Advances:** Configurable employee loan master with automated monthly EMI deductions against gross earnings.
- **Tax Slabs & Declarations:** Support for Old vs New Income Tax regimes, Section 80C/80D declarations, HRA exemption proofs, and monthly TDS deduction.
- **Automated Bank Entry:** Directly generates double-entry Journal Entries posting salary liabilities to Accounts Payable and liquid bank accounts.
- **India Ready:** Out-of-the-box compliance for Provident Fund (12% capped at ₹15,000 wage ceiling), ESI (0.75% / 3.25% under ₹21,000 gross), Professional Tax (State slabs), Gratuity, and NEFT/RTGS bank transfer text formats.

---

## 📂 Repository & Module Structure

```
frappe-payroll-salary-tax-engine/
├── payroll_tax/
│   ├── __init__.py           # Package version & module exports
│   └── engine.py             # Core payroll calculation & statutory tax engine
├── tests/
│   ├── __init__.py
│   └── test_payroll_tax.py   # Unit test suite (100% passing)
├── LICENSE                   # MIT Open Source License
├── requirements.txt          # Python dependencies
└── README.md                 # Complete documentation
```

---

## 🔌 Frappe DocType Schema Design

- **`Salary Component`:** Component Name, Type (Earning/Deduction), Formula, Depends on Payment Days, and Is Statutory.
- **`Salary Structure`:** Structure Name, Company, Earnings Child Table, Deductions Child Table, and Currency.
- **`Salary Structure Assignment`:** Employee, Salary Structure, From Date, Base Amount, and Income Tax Slab.
- **`Payroll Entry`:** Posting Date, Payroll Frequency, Department, Total Employees Processed, and Gross Pay.
- **`Salary Slip`:** Employee, Month, Working Days, Loss of Pay Days, Gross Earnings, Statutory Deductions, and Net Pay.

---

## 🚀 Installation & Setup

### 1. Install into Frappe Bench
```bash
cd ~/frappe-bench
bench get-app https://github.com/shyampandey1104/frappe-payroll-salary-tax-engine.git
bench --site [your-site-name] install-app frappe_payroll_salary_tax
```

### 2. Configure Payroll Scheduler (`hooks.py`)
```python
scheduler_events = {
    "monthly": [
        "payroll_tax.engine.process_end_of_month_payroll"
    ]
}
```

---

## 💻 Production Usage Example

```python
from payroll_tax.engine import PayrollSalaryTaxEngine, SalaryStructureSpec

engine = PayrollSalaryTaxEngine()

# 1. Define employee salary structure
spec = SalaryStructureSpec(
    employee_id="EMP-2026-088",
    employee_name="Siddharth Rao",
    monthly_ctc=60000.0,
    basic_pct_of_ctc=0.50,
    hra_pct_of_basic=0.50,
    is_pf_applicable=True,
    is_esi_applicable=True,
    is_pt_applicable=True
)

# 2. Process monthly salary slip with 2 days LOP and TDS
slip = engine.calculate_salary_slip(
    spec=spec,
    month_name="April 2026",
    worked_days=28.0,
    total_month_days=30.0,
    monthly_tds_estimate=2200.0
)

print(f"Gross Earnings: Rs. {slip.gross_earnings}")
print(f"Basic Salary:   Rs. {slip.basic_salary}")
print(f"HRA:            Rs. {slip.hra}")
print(f"Employee PF:    Rs. {slip.employee_pf}")
print(f"Prof. Tax (PT): Rs. {slip.professional_tax}")
print(f"TDS Deduction:  Rs. {slip.tds_deduction}")
print(f"Net Payable:    Rs. {slip.net_payable_salary}")
```

---

## 🧪 Testing & Verification

Run tests with standard Python:
```bash
python3 -m unittest discover tests
```

---

## 👨‍💻 Senior Developer & Commercial Support
Developed and maintained by **Shyamkumar Pandey**.  
For enterprise payroll configurations, custom banking integrations, and statutory compliance consulting:
- **GitHub:** [@shyampandey1104](https://github.com/shyampandey1104)
- **Email:** [shyampandey1104@gmail.com](mailto:shyampandey1104@gmail.com)
