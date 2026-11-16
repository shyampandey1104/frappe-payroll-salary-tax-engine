import unittest
from payroll_tax.engine import PayrollSalaryTaxEngine, SalaryStructureSpec

class TestPayrollTaxEngine(unittest.TestCase):
    def test_standard_salary_calculation(self):
        engine = PayrollSalaryTaxEngine()
        spec = SalaryStructureSpec(
            employee_id="EMP-101",
            employee_name="Amit Sharma",
            monthly_ctc=50000.0,
            basic_pct_of_ctc=0.50,
            hra_pct_of_basic=0.50,
            is_pf_applicable=True,
            is_esi_applicable=True,
            is_pt_applicable=True
        )
        slip = engine.calculate_salary_slip(spec, month_name="April 2026", worked_days=30, total_month_days=30, monthly_tds_estimate=1500.0)
        self.assertEqual(slip.basic_salary, 25000.0)
        self.assertEqual(slip.hra, 12500.0)
        self.assertEqual(slip.employee_pf, 1800.0) # 12% capped at ₹15,000 wage ceiling
        self.assertEqual(slip.employee_esi, 0.0)   # Gross > 21k, ESI exempt
        self.assertEqual(slip.professional_tax, 200.0)
        self.assertEqual(slip.tds_deduction, 1500.0)
        self.assertGreater(slip.net_payable_salary, 40000.0)

    def test_esi_applicable_worker_salary(self):
        engine = PayrollSalaryTaxEngine()
        spec = SalaryStructureSpec(
            employee_id="EMP-WRK-01",
            employee_name="Ramesh Kumar",
            monthly_ctc=18000.0,
            is_pf_applicable=True,
            is_esi_applicable=True
        )
        slip = engine.calculate_salary_slip(spec, month_name="April 2026", worked_days=30, total_month_days=30)
        self.assertEqual(slip.gross_earnings, 18000.0)
        self.assertEqual(slip.employee_esi, 135.0) # 0.75% of 18,000 = 135
        self.assertEqual(slip.employer_esi, 585.0) # 3.25% of 18,000 = 585

if __name__ == "__main__":
    unittest.main()
