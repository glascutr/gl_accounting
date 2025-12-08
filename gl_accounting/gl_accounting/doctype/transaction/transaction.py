# Copyright (c) 2025, Glascutr Limited and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Transaction(Document):
    pass


# Transaction List

'''
transactions = frappe.db.sql("""
  SELECT 
         tr.date,
         tr.particulars,
         tr.cheque,
         tr.voucher_type,
         tr.folio_no,
         tr.type,
         tr.amount,
         ah.name,
         ah.name1,
         ah.type
  FROM `tabTransaction` tr

  INNER JOIN `tabAccounts Head` ah
    ON tr.accounts_head = ah.name

  ORDER BY tr.modified DESC
""", as_dict=True)

'''


# Credit transactions

'''
credit_transactions = frappe.db.sql("""
  SELECT 
         tr.date,
         tr.particulars,
         tr.cheque,
         tr.voucher_type,
         tr.folio_no,
         tr.type,
         tr.amount,
         ah.name,
         ah.name1,
         ah.type
  FROM `tabTransaction` tr

  INNER JOIN `tabAccounts Head` ah
    ON tr.accounts_head = ah.name

 Where  ah.type = "Credit"
    

  ORDER BY tr.modified DESC
""", as_dict=True)

'''



# Credit Accounts Head wise Summatiuon

'''
credit_accounts_head_summation =  frappe.db.sql("""
  SELECT 
         ah.name,
         ah.name1,
        #  ah.type,
         SUM(tr.amount) AS total_amount
  FROM `tabTransaction` tr

  INNER JOIN `tabAccounts Head` ah
    ON tr.accounts_head = ah.name
    
  where  ah.type = "Credit"

  GROUP BY ah.name, ah.name1, ah.type

""", as_dict=True)

'''


# Debit Accounts Head wise Summatiuon

'''
debit_accounts_head_summation =  frappe.db.sql("""
  SELECT 
         ah.name,
         ah.name1,
        #  ah.type,
         SUM(tr.amount) AS total_amount
  FROM `tabTransaction` tr

  INNER JOIN `tabAccounts Head` ah
    ON tr.accounts_head = ah.name
    
  where  ah.type = "Debit"

  GROUP BY ah.name, ah.name1, ah.type

""", as_dict=True)

'''

# Total Debit and Credit 1

'''
total_credit = 0
total_debit = 0

for row in accounts_head_summation:
    if row['type'] == 'Credit':
        total_credit += row['total_amount']
    elif row['type'] == 'Debit':
        total_debit += row['total_amount']

print("Total Credit =", total_credit)
print("Total Debit =", total_debit)


'''
# Total Debit and Credit 1

'''
total_debit_credit = frappe.db.sql("""
   SELECT 
       ah.type,
       SUM(tr.amount) AS total_amount
   FROM `tabTransaction` tr
   INNER JOIN `tabAccounts Head` ah
        ON tr.accounts_head = ah.name
   GROUP BY ah.type
""", as_dict=True)

'''



######
######
######
######

'''

context.accounts_heads_debit_summation =  frappe.db.sql("""
  SELECT 
         ah.name,
         ah.name1,
        #  ah.type,
         SUM(tr.amount) AS total_amount
  FROM `tabTransaction` tr

  INNER JOIN `tabAccounts Head` ah
    ON tr.accounts_head = ah.name
    
  where  ah.type = "Debit"

  GROUP BY ah.name, ah.name1, ah.type

""", as_dict=True)




context.accounts_heads_credit_summation =  frappe.db.sql("""
  SELECT 
         ah.name,
         ah.name1,
        #  ah.type,
         SUM(tr.amount) AS total_amount
  FROM `tabTransaction` tr

  INNER JOIN `tabAccounts Head` ah
    ON tr.accounts_head = ah.name
    
  where  ah.type = "Credit"

  GROUP BY ah.name, ah.name1, ah.type

""", as_dict=True)



context.total_credit = frappe.db.sql("""
    SELECT 
        IFNULL(SUM(tr.amount), 0) AS total_credit
    FROM `tabTransaction` tr

    INNER JOIN `tabAccounts Head` ah
        ON tr.accounts_head = ah.name

    WHERE ah.type = "Credit"
""", as_dict=True)[0]["total_credit"]


context.total_debit = frappe.db.sql("""
    SELECT 
        IFNULL(SUM(tr.amount), 0) AS total_credit
    FROM `tabTransaction` tr

    INNER JOIN `tabAccounts Head` ah
        ON tr.accounts_head = ah.name

    WHERE ah.type = "Debit"
""", as_dict=True)[0]["total_credit"]

'''

###### ______________________Trial Balance / Credit and Debit Balance________________________

'''



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



'''