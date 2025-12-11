# Get today's date
today = frappe.utils.today()

# Query current fiscal year safely
fy = frappe.db.sql("""
    SELECT name
    FROM `tabFiscal Year`
    WHERE %s BETWEEN year_start_date AND year_end_date
    LIMIT 1
""", today, as_dict=True)

# Safe check if fiscal year exists
current_fiscal_year = fy[0]["name"] if fy else None

# Set context variable for Web Page template
context.current_fiscal_year = current_fiscal_year

# Only fetch Profit and Loss Appropriation Account if fiscal year exists
profit_loss_appropriation_account = None
if current_fiscal_year:
    profit_loss_appropriation_account = frappe.get_doc(
        "Profit and Loss Appropriation Account",
        {"year": current_fiscal_year}  # filter by unique field
    )

total_profit_balanced = 0
total_loss_balanced = 0

if profit_loss_appropriation_account.is_previous_year_profit:
    total_profit_balanced = total_profit_balanced + profit_loss_appropriation_account.previous_year_profit_or_loss_amount
else:
    total_loss_balanced = total_loss_balanced + profit_loss_appropriation_account.previous_year_profit_or_loss_amount
    
if profit_loss_appropriation_account.is_current_year_profit:
    total_profit_balanced = total_profit_balanced + profit_loss_appropriation_account.current_year_profit_or_loss_amount
else:
    total_loss_balanced = total_loss_balanced + profit_loss_appropriation_account.current_year_profit_or_loss_amount
    
    
if not profit_loss_appropriation_account.is_profit:
    total_profit_balanced = total_profit_balanced + profit_loss_appropriation_account.total_balance
else:
    total_loss_balanced = total_loss_balanced + profit_loss_appropriation_account.total_balance
    

    

# Set to context so template can use it
context.profit_loss_appropriation_account = profit_loss_appropriation_account

context.total_profit_balanced = total_profit_balanced
context.total_loss_balanced = total_loss_balanced

