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
""", ("2025-12-01", "2025-12-11"), as_dict=True)  # ✅ proper date format

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

# Assign to context
context.accounts_heads_debit_summation = accounts_heads_debit_summation
context.accounts_heads_credit_summation = accounts_heads_credit_summation
context.total_credit = total_credit

# 2️⃣ Transactions grouped by type
transaction_type_group_sum = frappe.db.sql("""
   SELECT 
       type,
       SUM(amount) AS total_amount
   FROM `tabTransaction`
   GROUP BY type
""", as_dict=True)

# Initialize variables
cash = 0
expense = 0
bank_credit = 0
bank_debit = 0

for row in transaction_type_group_sum:
    if row["type"] == "Cash Amount":
        cash += row["total_amount"]
    elif row["type"] == "Expencess Amount":
        expense += row["total_amount"]
    elif row["type"] == "Bank Credit":
        bank_credit += row["total_amount"]
    elif row["type"] == "Bank Debit":
        bank_debit += row["total_amount"]

# Calculate cash & bank balances
cash_in_hand = cash - expense
cash_at_bank = bank_credit - (total_contra + bank_debit)

# Assign totals to context
# context.total_debit = total_debit + cash_in_hand + cash_at_bank
context.total_debit = total_debit 

# context.cash_in_hand = cash_in_hand
# context.cash_at_bank = cash_at_bank
