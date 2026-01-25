if frappe.session.user == "Guest":
    frappe.throw("Not permitted", frappe.PermissionError)

fy_name = frappe.db.get_single_value(
    "Active Fiscal Year",
    "fiscal_year"
)

fy_doc = None
if fy_name:
    fy_doc = frappe.db.get_value(
        "Fiscal Year",
        fy_name,
        "*",
        as_dict=True
    )

context.fy_doc = fy_doc

from_date = fy_doc.year_start_date
to_date = fy_doc.year_end_date

context.from_date = from_date
context.to_date = to_date


trading_acounts = frappe.db.sql("""
    SELECT
        ah.type,
        ah.name,
        ah.name1,
        SUM(tr.amount) AS total_amount
    FROM `tabTransaction` tr
    INNER JOIN `tabAccounts Head` ah
        ON tr.accounts_head = ah.name
    WHERE  
        tr.date BETWEEN %s AND %s AND ah.is_trading_account=1 and ah.type IN ('Debit', 'Credit')
    GROUP BY ah.type, ah.name, ah.name1
""",(from_date, to_date) ,as_dict=True)
        
        
total_credit = 0
total_debit = 0

trading_credit_accounts = []
trading_debit_accounts = []


for row in trading_acounts:
    if row["type"] == "Credit":
        total_credit = total_credit + row["total_amount"]
        trading_credit_accounts.append(row)
        
    elif row["type"] == "Debit":
        total_debit = total_debit + row["total_amount"]
        trading_debit_accounts.append(row)
        



profit = total_credit - total_debit

# profit = -10253400.0

context.profit = profit

profit_abs =  abs(profit)

context.total_credit = total_credit if profit >= 0 else total_credit + profit_abs
context.total_debit = total_debit + profit_abs if profit >= 0 else total_debit



context.trading_credit_accounts = trading_credit_accounts 
context.trading_debit_accounts = trading_debit_accounts

context.gross_profit = profit_abs

