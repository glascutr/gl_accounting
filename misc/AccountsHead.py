import frappe
import csv

# with open("/home/nazmul/Desktop/GLASCUTR_SAAS/apps/gl_accounting/misc/AccountsHead - Sheet1.csv") as f:
with open("AccountsHead - Sheet1.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        doc = frappe.get_doc({
            "doctype": "Accounts Head",
            **row
        })
        
        
        doc.insert(ignore_permissions=True)

frappe.db.commit()


# import frappe
# import csv

# # with open("AccountsHeadSheet1.csv") as f:
# with open("/home/nazmul/Desktop/GLASCUTR_SAAS/apps/gl_accounting/misc/AccountsHeadSheet1.csv") as f:
#     reader = csv.DictReader(f)
#     for row in reader:
#         print(row)