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



# ______________________Profit and Loss________________________

profit_loss_acounts = frappe.db.sql("""
    SELECT
        ah.type,
        ah.name,
        ah.name1,
        SUM(tr.amount) AS total_amount
    FROM `tabTransaction` tr
    INNER JOIN `tabAccounts Head` ah
        ON tr.accounts_head = ah.name
    WHERE tr.date BETWEEN %s AND %s AND ah.is_profit_and_loss_account=1 and ah.type IN ('Debit', 'Credit')
    GROUP BY ah.type, ah.name, ah.name1
""", (from_date, to_date),as_dict=True)
        
        
profit_loss_total_debit = 0
profit_loss_total_credit = 0

profit_loss_debit_accounts = []
profit_loss_credit_accounts = []


for row in profit_loss_acounts:
    if row["type"] == "Credit":
        profit_loss_total_credit = profit_loss_total_credit + row["total_amount"]
        profit_loss_credit_accounts.append(row)
        
    elif row["type"] == "Debit":
        profit_loss_total_debit = profit_loss_total_debit + row["total_amount"]
        profit_loss_debit_accounts.append(row)
        
context.profit_loss_debit_accounts = profit_loss_debit_accounts
context.profit_loss_credit_accounts = profit_loss_credit_accounts



# # ________________________ Trading Account ________________________

trading_acounts = frappe.db.sql("""
    SELECT
        ah.type,
        ah.name,
        ah.name1,
        SUM(tr.amount) AS total_amount
    FROM `tabTransaction` tr
    INNER JOIN `tabAccounts Head` ah
        ON tr.accounts_head = ah.name
    WHERE tr.date BETWEEN %s AND %s AND ah.is_trading_account=1 and ah.type IN ('Debit', 'Credit')
    GROUP BY ah.type, ah.name, ah.name1
""", (from_date, to_date), as_dict=True)
        
        
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

gross_loss = 0 if profit >= 0 else abs(profit)
gross_profit = 0 if profit < 0 else profit

context.gross_loss = gross_loss
context.gross_profit = gross_profit



gross_total_debit  = profit_loss_total_debit + gross_loss
gross_total_credit = profit_loss_total_credit + gross_profit

net_profit_loss = gross_total_credit - gross_total_debit

net_loss = net_profit_loss if net_profit_loss < 0 else 0
net_profit = net_profit_loss if net_profit_loss >= 0 else 0

context.net_loss = net_loss
context.net_profit = net_profit



net_total_debit = profit_loss_total_debit + gross_loss + net_profit
net_total_credit = profit_loss_total_credit + gross_profit + net_loss




context.is_loss = bool(profit < 0)

context.is_net_loss = bool(net_profit_loss < 0)


context.net_total_debit = net_total_debit
context.net_total_credit = net_total_credit
