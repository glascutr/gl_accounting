if frappe.session.user == "Guest":
    frappe.throw("Not permitted", frappe.PermissionError)

month = frappe.form_dict.get('month') 

year = frappe.form_dict.get('year') 


context.selected_month = month
context.selected_year = year


if month and year:

    months = {
        "January": {"from_date": "01-01" , "to_date": "02-01"},
        "February": {"from_date": "02-01" , "to_date": "03-01"},
        "March": {"from_date": "03-01", "to_date": "04-01"},
        "April": {"from_date":  "04-01", "to_date":  "05-01"},
        "May": {"from_date": "05-01", "to_date": "06-01"},
        "June": {"from_date": "06-01", "to_date": "07-01"},
        "July": {"from_date": "07-01", "to_date": "08-01"},
        "August": {"from_date": "08-01", "to_date": "09-01"},
        "September": {"from_date": "09-01" , "to_date": "10-01"},
        "October": {"from_date": "10-01", "to_date": "11-01"},
        "November": {"from_date": "11-01", "to_date": "12-01"},
        "December": {"from_date": "12-01", "to_date": "01-01"}
    }

    from_date = f"{year}-{months[month]['from_date']}"
    to_date = f"{year}-{months[month]['to_date']}"
    if month=="December":
        to_date = f"{year+1}-{months[month]['to_date']}"



    fy_name = frappe.db.get_value(
        "Fiscal Year",
        {
            "year_start_date": ["<=", from_date],
            "year_end_date": [">=", from_date],
        },
        "name"
    )

    if not fy_name:
        frappe.throw(f"No Fiscal Year found for date {from_date}")

    fy_doc = frappe.get_doc("Fiscal Year", fy_name)
    context.fy_doc = fy_doc

    context.from_date = from_date
    context.to_date = to_date



    rows = frappe.db.sql("""
        SELECT
            ah.type,
            ah.name,
            ah.name1,
            SUM(tr.amount) AS total_amount
        FROM `tabTransaction` tr
        INNER JOIN `tabAccounts Head` ah
            ON tr.accounts_head = ah.name
    
        WHERE tr.date >= %s AND tr.date < %s AND

        ah.type IN ('Debit', 'Credit') 
        GROUP BY ah.type, ah.name, ah.name1
    """,(from_date, to_date), as_dict=True)
    

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
    WHERE date <= %s AND date < %s
    GROUP BY 
        type
    """,(from_date, to_date),as_dict=True)


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

    context.cash_in_hand = cash_in_hand
    context.cash_at_bank = cash_at_bank
    context.total_debit = total_debit + cash_in_hand + cash_at_bank




