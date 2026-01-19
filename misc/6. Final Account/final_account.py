# # Get today's date
# today = frappe.utils.today()

# # Query current fiscal year safely
# fy = frappe.db.sql("""
#     SELECT name
#     FROM `tabFiscal Year`
#     WHERE %s BETWEEN year_start_date AND year_end_date
#     LIMIT 1
# """, today, as_dict=True)

# # Safe check if fiscal year exists
# current_fiscal_year = fy[0]["name"] if fy else None

# # Set context variable for Web Page template
# context.current_fiscal_year = current_fiscal_year



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



# Only fetch Profit and Loss Appropriation Account if fiscal year exists
profit_loss_appropriation_account = None
if fy_doc:
    profit_loss_appropriation_account = frappe.get_doc(
        "Profit and Loss Appropriation Account",
        {"year": fy_doc.year}  # filter by unique field
    )

context.profit_loss_appropriation_account = profit_loss_appropriation_account


# -----------------------------------------------------
# Cash in Hand
# Cash at Bank
rows = frappe.db.sql("""
    SELECT
        ah.type,
        ah.name,
        ah.name1,
        SUM(tr.amount) AS total_amount
    FROM `tabTransaction` tr
    INNER JOIN `tabAccounts Head` ah
        ON tr.accounts_head = ah.name
    WHERE tr.date BETWEEN %s AND %s AND ah.type IN ('Debit', 'Credit')
    GROUP BY ah.type, ah.name, ah.name1
""",(from_date, to_date), as_dict=True)

# accounts_heads_debit_summation = []
# accounts_heads_credit_summation = []

total_debit = 0
total_credit = 0
total_contra = 0

for row in rows:

    if row["name1"] == "Contra Account":
        total_contra = total_contra + row["total_amount"]

    elif row["type"] == "Debit":
        # accounts_heads_debit_summation.append(row)
        total_debit = total_debit + row["total_amount"]

    elif row["type"] == "Credit":
        # accounts_heads_credit_summation.append(row)
        total_credit = total_credit + row["total_amount"]

# # ✅ FINAL context assignment (SAFE)
# context.accounts_heads_debit_summation = accounts_heads_debit_summation
# context.accounts_heads_credit_summation = accounts_heads_credit_summation

# context.total_debit = total_debit
context.total_credit = total_credit


transaction_type_group_sum = frappe.db.sql("""
   SELECT
       type,
       SUM(amount) AS total_amount
   FROM
       `tabTransaction`
   WHERE date BETWEEN %s AND %s 
   GROUP BY
       type
""",(from_date, to_date), as_dict=True)


cash = 0
expense = 0
bank_credit = 0
bank_debit = 0

for row in transaction_type_group_sum:
    if row["type"] == "Cash Amount":
        cash = cash + row["total_amount"]
    elif row["type"] == "Expencess Amount":
        expense = expense + row["total_amount"]
    elif row["type"] == "Bank Credit":
        bank_credit = bank_credit + row["total_amount"]
    elif row["type"] == "Bank Debit":
        bank_debit = bank_debit + row["total_amount"]


cash_in_hand = cash-expense
cash_at_bank = bank_credit - (total_contra + bank_debit)

context.total_debit = total_debit + cash_in_hand + cash_at_bank
context.cash_in_hand = cash_in_hand
context.cash_at_bank = cash_at_bank


# ----------------------------------------
final_accounts = frappe.db.sql("""
    SELECT
        ah.name,
        ah.final_account_type,
        ah.name1,
        SUM(tr.amount) AS total_amount
    FROM `tabTransaction` tr
    INNER JOIN `tabAccounts Head` ah
        ON tr.accounts_head = ah.name
    WHERE tr.date BETWEEN %s AND %s  AND ah.final_account_type IN ('Liabilities', 'Assets', 'Equity')
    GROUP BY ah.type, ah.name, ah.name1
""",(from_date, to_date), as_dict=True)


liability_list = []
asset_list = []
equity_list = []

total_liability = 0
total_asset = 0
total_equity = 0

for final_account in final_accounts:
    if final_account["final_account_type"] == "Liabilities":
        total_liability = total_liability + final_account["total_amount"]
        liability_list.append(final_account)

    elif final_account["final_account_type"] == "Assets":
        total_asset = total_asset + final_account["total_amount"]
        asset_list.append(final_account)

    elif final_account["final_account_type"] == "Equity":
        total_equity = total_equity + final_account["total_amount"]
        equity_list.append(final_account)


entry_liabilies_list = frappe.db.sql("""
    SELECT
        accounts_head,
        SUM(amount) AS total_amount
    FROM
        `tabEntry Liabilities`
    GROUP BY
        accounts_head
    ORDER BY
        date DESC
    WHERE tr.date BETWEEN %s AND %s
""", (from_date, to_date), as_dict=True)

entry_liabilies = []
total_entry_liabilies_amount = 0

for row in entry_liabilies_list:
    entry_liabilies.append(row)
    total_entry_liabilies_amount = total_entry_liabilies_amount + row["total_amount"]
    
    


entry_assets_list = frappe.db.sql("""
    SELECT
        accounts_head,
        SUM(amount) AS total_amount
    FROM
        `tabEntry Liabilities`
    GROUP BY
        accounts_head
    ORDER BY
        date DESC
    WHERE tr.date BETWEEN %s AND %s
""", (from_date, to_date), as_dict=True)


entry_assets = []
total_entry_assets_amount = 0

for row in entry_assets_list:
    entry_assets.append(row)
    total_entry_assets_amount = total_entry_assets_amount + row["total_amount"]
    
    


context.liability_list = liability_list
context.asset_list = asset_list
context.entry_liabilies = entry_liabilies
context.entry_assets = entry_assets

context.equity_list = equity_list   
# context.total_liability = total_liability
context.total_liability = (total_liability + profit_loss_appropriation_account.total_balance if profit_loss_appropriation_account.is_profit else total_liability)+total_entry_liabilies_amount
context.total_asset = ((total_asset + profit_loss_appropriation_account.total_balance if not profit_loss_appropriation_account.is_profit else total_asset)+ (cash_in_hand+cash_at_bank))+total_entry_assets_amount
context.total_equity = total_equity

