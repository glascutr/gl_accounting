if frappe.session.user == "Guest":
    frappe.throw("Not permitted", frappe.PermissionError)

from_date = frappe.form_dict.get("from_date")
to_date = frappe.form_dict.get("to_date")

context.from_date = from_date
context.to_date = to_date


if from_date and to_date:
    accounts_head_title = "Revenue(Service Charge)"

    transactions = frappe.db.sql("""
        SELECT
            tr.date,
            tr.amount,
            pr.title AS particulars
        FROM `tabTransaction` tr
        INNER JOIN `tabAccounts Head` ah
            ON tr.accounts_head = ah.name
        LEFT JOIN `tabParticulars` pr
            ON tr.particulars = pr.name
        WHERE tr.date BETWEEN %(from_date)s AND %(to_date)s
        AND ah.name1 = %(accounts_head_title)s
        ORDER BY tr.date ASC
    """, {
        "from_date": from_date,
        "to_date": to_date,
        "accounts_head_title": accounts_head_title
    }, as_dict=True)


    context.transaction_list = transactions
    context.total_revenue = sum(tr["amount"] for tr in transactions)
    

