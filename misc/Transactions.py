transactions = frappe.db.sql("""
  SELECT 
         tr.date,
         tr.particulars,
         tr.cheque,
         tr.voucher_type,
         tr.folio_no,
         tr.type,
         tr.amount,
         ah.name1
  FROM `tabTransaction` tr

  INNER JOIN `tabAccounts Head` ah
    ON tr.accounts_head = ah.name

  ORDER BY tr.modified DESC
""", as_dict=True)


total_contra = 0
total_cash_amount = 0
total_expencess_amount = 0
total_bank_debit = 0
total_bank_credit = 0


for row in transactions:
    
    if row["name1"] =="Contra Account":
        total_contra = total_contra + row["amount"]
        
    if row["type"] =="Cash Amount":
        total_cash_amount = total_cash_amount + row["amount"]
        
    elif row["type"] =="Expencess Amount":
        total_expencess_amount = total_expencess_amount + row["amount"]
        
    elif row["type"] =="Bank Debit":
        total_bank_debit = total_bank_debit + row["amount"]
    
    elif row["type"] =="Bank Credit":
        total_bank_credit = total_bank_credit + row["amount"]
    
        

context.transactions = transactions
context.total_cash_amount = total_cash_amount
context.total_expencess_amount = total_expencess_amount
context.total_bank_debit = total_bank_debit + total_contra
context.total_bank_credit = total_bank_credit
