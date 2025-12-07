# Copyright (c) 2025, Glascutr Limited and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Transaction(Document):
    pass


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
         ah.name1
  FROM `tabTransaction` tr

  INNER JOIN `tabAccounts Head` ah
    ON tr.accounts_head = ah.name

  ORDER BY tr.modified DESC
""", as_dict=True)


'''
