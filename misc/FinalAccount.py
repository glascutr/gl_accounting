# Get today's date
today = frappe.utils.today()

# Query current fiscal year safely
fy = frappe.db.sql("""
    SELECT name
    FROM `tabFiscal Year`
    WHERE %s BETWEEN year_start_date AND year_end_date
    LIMIT 1
""", today, as_dict=True)

# Safe check if fiscal year exists
current_fiscal_year = fy[0]["name"] if fy else None

# Set context variable for Web Page template
context.current_fiscal_year = current_fiscal_year


# Only fetch Profit and Loss Appropriation Account if fiscal year exists
profit_loss_appropriation_account = None
if current_fiscal_year:
    profit_loss_appropriation_account = frappe.get_doc(
        "Profit and Loss Appropriation Account",
        {"year": current_fiscal_year}  # filter by unique field
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
    WHERE ah.type IN ('Debit', 'Credit')
    GROUP BY ah.type, ah.name, ah.name1
""", as_dict=True)

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
   GROUP BY
       type
""", as_dict=True)


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
    WHERE ah.final_account_type IN ('Liabilities', 'Assets', 'Equity')
    GROUP BY ah.type, ah.name, ah.name1
""", as_dict=True)


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


context.liability_list = liability_list
context.asset_list = asset_list
context.equity_list = equity_list   
# context.total_liability = total_liability
context.total_liability = total_liability + profit_loss_appropriation_account.total_balance if profit_loss_appropriation_account.is_profit else total_liability
context.total_asset = (total_asset + profit_loss_appropriation_account.total_balance if not profit_loss_appropriation_account.is_profit else total_asset)+ (cash_in_hand+cash_at_bank)
context.total_equity = total_equity

