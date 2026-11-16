# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "payroll_tax"
app_title = "Frappe Payroll Salary Tax Engine"
app_publisher = "Shyamkumar Pandey"
app_description = "Frappe Payroll Salary Tax Engine for Frappe and ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/payroll_tax/css/payroll_tax.bundle.css"
app_include_js = "/assets/payroll_tax/js/payroll_tax.bundle.js"

# Document Events
# ---------------
doc_events = {
    "DocType Event": {
        "on_submit": "payroll_tax.engine.on_document_submit",
        "on_cancel": "payroll_tax.engine.on_document_cancel"
    }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "payroll_tax.engine.daily_scheduled_sync"
    ]
}
