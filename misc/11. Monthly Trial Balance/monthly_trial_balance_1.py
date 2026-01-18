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
    

    this_month_accounts_head_wise_debit_list = []
    this_month_accounts_head_wise_credit_list = []

    this_month_total_contra = 0
    this_month_total_debit = 0
    this_month_total_credit = 0

    for row in rows:
        
        
        if row["name1"] =="Contra Account":
            this_month_total_contra = this_month_total_contra + row["total_amount"]
        
        elif row["type"] == "Debit":
            this_month_accounts_head_wise_debit_list.append(row)
            this_month_total_debit = this_month_total_debit + row["total_amount"]

        elif row["type"] == "Credit": # Already contra is added with credit
            this_month_accounts_head_wise_credit_list.append(row)
            this_month_total_credit = this_month_total_credit + row["total_amount"]

    
    
    # ✅ FINAL context assignment 
    context.this_month_accounts_head_wise_debit_list = this_month_accounts_head_wise_debit_list
    context.this_month_accounts_head_wise_credit_list = this_month_accounts_head_wise_credit_list

    # This month total credits and debits
    context.this_month_total_debit = this_month_total_debit 
    context.this_month_total_credit = this_month_total_credit
    
    
    # This Month `Cash In Hand` and `Cash at Bank`
    
    this_month_transactions = frappe.db.sql("""
        SELECT 
            type,
            SUM(amount) AS total_amount
        FROM 
            `tabTransaction`
        WHERE date BETWEEN %s AND %s 
        GROUP BY 
            type
    """,(from_date, to_date),as_dict=True)
        
    
    this_month_cash = 0
    this_month_expense = 0
    this_month_bank_credit = 0
    this_month_bank_debit = 0

    for row in this_month_transactions:
        if row["type"] == "Cash Amount":
            this_month_cash = this_month_cash + row["total_amount"]
        elif row["type"] == "Expencess Amount":
            this_month_expense = this_month_expense + row["total_amount"]
        elif row["type"] == "Bank Credit":
            this_month_bank_credit = this_month_bank_credit + row["total_amount"]
        elif row["type"] == "Bank Debit":
            this_month_bank_debit = this_month_bank_debit + row["total_amount"]
            
    this_month_cash_in_hand = this_month_cash - this_month_expense  # Credit Portion
    this_month_cash_at_bank = this_month_bank_credit - (this_month_bank_debit + this_month_total_contra) # Credit Portion
        
    # ==================================================================
    
    # prevous_contra_amount = 0
    
    prevous_contra = frappe.db.sql("""
        SELECT
            SUM(CASE WHEN ah.type = 'Debit' THEN tr.amount ELSE 0 END) AS debit_amount,
            SUM(CASE WHEN ah.type = 'Credit' THEN tr.amount ELSE 0 END) AS credit_amount
        FROM `tabTransaction` tr
        INNER JOIN `tabAccounts Head` ah
            ON tr.accounts_head = ah.name
        WHERE
            tr.date BETWEEN %s AND %s
            AND ah.name1 = %s
    """, (fy_doc.year_start_date, from_date, "Contra Account"), as_dict=True)[0]

    prevous_contra_debit = prevous_contra["debit_amount"] or 0
    prevous_contra_credit = prevous_contra["credit_amount"] or 0
    
    prevous_months_contra_balance = abs(prevous_contra_debit - prevous_contra_credit)
    
    # previous `Cash in Hand` and `Cash at Bank` -------------------------------

    previous_month_transactions = frappe.db.sql("""
        SELECT 
            type,
            SUM(amount) AS total_amount
        FROM 
            `tabTransaction`
        WHERE date BETWEEN %s AND %s 
        GROUP BY 
            type
    """,(from_date, to_date),as_dict=True)
        
    
    previous_months_cash = 0
    previous_months_expense = 0
    previous_months_bank_credit = 0
    previous_months_bank_debit = 0

    for row in previous_month_transactions:
        if row["type"] == "Cash Amount":
            previous_months_cash = previous_months_cash + row["total_amount"]
        elif row["type"] == "Expencess Amount":
            previous_months_expense = previous_months_expense + row["total_amount"]
        elif row["type"] == "Bank Credit":
            previous_months_bank_credit = previous_months_bank_credit + row["total_amount"]
        elif row["type"] == "Bank Debit":
            previous_months_bank_debit = previous_months_bank_debit + row["total_amount"]
        

    previous_months_cash_in_hand = (previous_months_cash-previous_months_expense)
    previous_months_cash_at_bank = previous_months_bank_credit - (prevous_months_contra_balance + previous_months_bank_debit)

    cash_in_hand_credit = previous_months_cash_in_hand + this_month_cash_in_hand
    context.cash_in_hand_credit = cash_in_hand_credit
    
    cash_at_bank_credit = previous_months_cash_at_bank + this_month_cash_at_bank
    context.cash_at_bank_credit = cash_at_bank_credit
    
    
    cash_in_hand_debit = cash_in_hand_credit - previous_months_expense - this_month_expense
    context.cash_in_hand_debit = cash_in_hand_debit
    
    cash_at_bank_debit = cash_at_bank_credit - previous_months_bank_debit - this_month_bank_debit
    context.cash_at_bank_debit = cash_at_bank_debit
    
    
    
    total_credit = this_month_total_credit + cash_in_hand_credit + cash_at_bank_credit
    total_debit = this_month_total_debit + cash_in_hand_debit + cash_at_bank_debit 
    
    context.total_credit = total_credit 
    context.total_debit = total_debit 
    
    
    
    

        
        
        
        