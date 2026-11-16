"""Automated Payroll Engine (Salary Processing, bina Excel ke - Ek click mein poore staff ki salary slip)."""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class SalaryStructureSpec:
    employee_id: str
    employee_name: str
    monthly_ctc: float
    basic_pct_of_ctc: float = 0.50      # Standard 50% Basic Salary
    hra_pct_of_basic: float = 0.50       # 50% HRA
    is_pf_applicable: bool = True
    is_esi_applicable: bool = True
    is_pt_applicable: bool = True
    state_for_pt: str = "Maharashtra"     # PT slabs vary by state


@dataclass
class ProcessedSalarySlip:
    employee_id: str
    month_name: str
    gross_earnings: float
    basic_salary: float
    hra: float
    special_allowance: float
    employee_pf: float       # 12% on Basic (capped at ₹15,000 ceiling or un-capped)
    employer_pf: float       # 12% Employer Match
    employee_esi: float      # 0.75% if Gross <= ₹21,000
    employer_esi: float      # 3.25% if Gross <= ₹21,000
    professional_tax: float  # Slabs (e.g. ₹200 in MH)
    tds_deduction: float     # Income Tax TDS
    total_deductions: float
    net_payable_salary: float
    currency: str = "INR"


class PayrollSalaryTaxEngine:
    """Automated Statutory Payroll and Salary Slip Generator for India."""

    PF_STATUTORY_WAGE_CEILING = 15000.0  # ₹15,000 monthly ceiling
    ESI_WAGE_CEILING = 21000.0           # ₹21,000 gross ceiling

    def calculate_salary_slip(
        self,
        spec: SalaryStructureSpec,
        month_name: str,
        worked_days: float = 30.0,
        total_month_days: float = 30.0,
        monthly_tds_estimate: float = 0.0,
        bonus_or_arrears: float = 0.0
    ) -> ProcessedSalarySlip:
        """Calculates precise salary components with statutory PF, ESI, PT, and TDS deductions."""
        proration_ratio = max(0.0, min(1.0, worked_days / total_month_days))
        monthly_effective_ctc = spec.monthly_ctc * proration_ratio

        basic = round(monthly_effective_ctc * spec.basic_pct_of_ctc, 2)
        hra = round(basic * spec.hra_pct_of_basic, 2)
        special_allowance = max(0.0, round(monthly_effective_ctc - (basic + hra), 2)) + bonus_or_arrears
        gross_earnings = round(basic + hra + special_allowance, 2)

        # 1. Provident Fund (PF): 12% of Basic (capped at ₹1,800 if wage ceiling applied)
        emp_pf = 0.0
        empr_pf = 0.0
        if spec.is_pf_applicable:
            pf_wage_base = min(basic, self.PF_STATUTORY_WAGE_CEILING)
            emp_pf = round(pf_wage_base * 0.12, 2)
            empr_pf = emp_pf

        # 2. Employee State Insurance (ESI): 0.75% emp, 3.25% employer if Gross <= ₹21,000
        emp_esi = 0.0
        empr_esi = 0.0
        if spec.is_esi_applicable and gross_earnings <= self.ESI_WAGE_CEILING:
            emp_esi = round(gross_earnings * 0.0075, 2)
            empr_esi = round(gross_earnings * 0.0325, 2)

        # 3. Professional Tax (PT): ₹200 standard for salary > ₹10,000 in MH
        pt = 0.0
        if spec.is_pt_applicable:
            if gross_earnings > 10000.0:
                pt = 200.0  # (In Feb it is ₹300 in MH, standard ₹200)

        # 4. TDS
        tds = round(monthly_tds_estimate, 2)

        total_deductions = round(emp_pf + emp_esi + pt + tds, 2)
        net_payable = round(gross_earnings - total_deductions, 2)

        return ProcessedSalarySlip(
            employee_id=spec.employee_id,
            month_name=month_name,
            gross_earnings=gross_earnings,
            basic_salary=basic,
            hra=hra,
            special_allowance=special_allowance,
            employee_pf=emp_pf,
            employer_pf=empr_pf,
            employee_esi=emp_esi,
            employer_esi=empr_esi,
            professional_tax=pt,
            tds_deduction=tds,
            total_deductions=total_deductions,
            net_payable_salary=net_payable
        )
