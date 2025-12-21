import frappe

@frappe.whitelist()
def add_particulars(particulars):

    if not particulars:
        frappe.throw("Particulars is required")

    # Avoid duplicate entry
    if frappe.db.exists("Particulars", {"title": particulars}):
        return

    doc = frappe.get_doc({
        "doctype": "Particulars",
        "title": particulars
    })

    doc.insert(ignore_permissions=True)
    frappe.db.commit()

    return doc.name
