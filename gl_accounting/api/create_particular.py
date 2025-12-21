# import frappe

# @frappe.whitelist()
# def add_particulars(title):
#     if not title:
#         frappe.throw("Title is required")

#     # Avoid duplicate entry based on title
#     doc = frappe.get_all(
#         "Particulars",
#         filters={"title": title},
#         limit=1
#     )

#     if doc:
#         particular_name = doc[0].name
#     else:
#         # create new Particular
#         new_doc = frappe.get_doc({
#             "doctype": "Particulars",
#             "title": title
#         })
#         new_doc.insert(ignore_permissions=True)
#         frappe.db.commit()
#         particular_name = new_doc.name

#     # return particular_name  # return DocType name
#     # return new_doc.title  # return DocType name
#     return new_doc  # return DocType name



import frappe

@frappe.whitelist()
def add_particulars(title):
    if not title:
        frappe.throw("Title is required")

    # Check duplicate
    doc = frappe.get_all("Particulars", filters={"title": title}, limit=1)

    if doc:
        particular_name = doc[0].name
        particular_title = title
    else:
        new_doc = frappe.get_doc({
            "doctype": "Particulars",
            "title": title
        })
        new_doc.insert(ignore_permissions=True)
        frappe.db.commit()
        particular_name = new_doc.name
        particular_title = new_doc.title

    # Return both name and title
    return {"name": particular_name, "title": particular_title}
