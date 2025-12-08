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

accounts_heads_debit_summation = []
accounts_heads_credit_summation = []

total_debit = 0
total_credit = 0
total_contra = 0

for row in rows:
    
    if row["name1"] =="Contra Account":
        total_contra = total_contra + row["total_amount"]
    
    elif row["type"] == "Debit":
        accounts_heads_debit_summation.append(row)
        total_debit = total_debit + row["total_amount"]

    elif row["type"] == "Credit":
        accounts_heads_credit_summation.append(row)
        total_credit = total_credit + row["total_amount"]

# ✅ FINAL context assignment (SAFE)
context.accounts_heads_debit_summation = accounts_heads_debit_summation
context.accounts_heads_credit_summation = accounts_heads_credit_summation

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


cash=0
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
cash_at_bank = bank_credit - (total_contra+ bank_debit)

context.total_debit = total_debit + cash_in_hand + cash_at_bank
context.cash_in_hand = cash_in_hand
context.cash_at_bank = cash_at_bank

