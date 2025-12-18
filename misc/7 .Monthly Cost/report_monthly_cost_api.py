# /home/nazmul/Desktop/GLASCUTR_SAAS/apps/gl_accounting/gl_accounting/reports/monthly_cost.py
# http://accounting.localhost:8000/api/method/gl_accounting.reports.monthly_cost.get_monthly_cost?from_date=2025-12-01&to_date=2025-12-10

import frappe

@frappe.whitelist()
def get_monthly_cost(from_date, to_date):

    # 1️⃣ Transactions grouped by Account Head (Debit/Credit)
    rows = frappe.db.sql("""
        SELECT
            ah.type,
            ah.name,
            ah.name1,
            SUM(tr.amount) AS total_amount
        FROM `tabTransaction` tr
        INNER JOIN `tabAccounts Head` ah
            ON tr.accounts_head = ah.name
        WHERE ah.type IN ('Debit', 'Credit') 
          AND tr.date BETWEEN %s AND %s
        GROUP BY ah.type, ah.name, ah.name1
    """, (from_date, to_date), as_dict=True)

    accounts_heads_debit_summation = []
    accounts_heads_credit_summation = []

    total_debit = 0
    total_credit = 0
    total_contra = 0

    for row in rows:
        if row["name1"] == "Contra Account":
            total_contra += row["total_amount"]
        elif row["type"] == "Debit":
            accounts_heads_debit_summation.append(row)
            total_debit += row["total_amount"]
        elif row["type"] == "Credit":
            accounts_heads_credit_summation.append(row)
            total_credit += row["total_amount"]

    # 2️⃣ Transactions grouped by type (WITH date filter)
    transaction_type_group_sum = frappe.db.sql("""
        SELECT 
            type,
            SUM(amount) AS total_amount
        FROM `tabTransaction`
        WHERE date BETWEEN %s AND %s
        GROUP BY type
    """, (from_date, to_date), as_dict=True)

    cash = expense = bank_credit = bank_debit = 0

    for row in transaction_type_group_sum:
        if row["type"] == "Cash Amount":
            cash += row["total_amount"]
        elif row["type"] == "Expencess Amount":
            expense += row["total_amount"]
        elif row["type"] == "Bank Credit":
            bank_credit += row["total_amount"]
        elif row["type"] == "Bank Debit":
            bank_debit += row["total_amount"]

    # 3️⃣ Calculations
    cash_in_hand = cash - expense
    cash_at_bank = bank_credit - (total_contra + bank_debit)

    # 4️⃣ API JSON Response
    return {
        "from_date": from_date,
        "to_date": to_date,

        "accounts_heads_debit_summation": accounts_heads_debit_summation,
        "accounts_heads_credit_summation": accounts_heads_credit_summation,

        "total_debit": total_debit,
        "total_credit": total_credit,

        "cash_in_hand": cash_in_hand,
        "cash_at_bank": cash_at_bank
    }
