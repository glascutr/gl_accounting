### GL Accounting

Simple Acounting for money craft.

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch main
bench install-app gl_accounting
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/gl_accounting
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade
### CI

This app can use GitHub Actions for CI. The following workflows are configured:

- CI: Installs this app and runs unit tests on every push to `develop` branch.
- Linters: Runs [Frappe Semgrep Rules](https://github.com/frappe/semgrep-rules) and [pip-audit](https://pypi.org/project/pip-audit/) on every pull request.


### License

mit



# HTML

```
<div style="display: flex; justify-content: flex-end">
  <button class="btn btn-secondary mb-3" onclick="printTable()">🖨 Print</button>
</div>

<div id="print-area">
  <!-- <div style="display: flex; justify-content: center; align-items: center"> -->
    <h4  style="display: flex; justify-content: center; align-items: center">GLASCUTR LIMITED</h4>

    <div  style="display: flex; justify-content: center; align-items: center"> Regent Red Wood, House 3/A, Unit B4, Road 2, Gulshan-1, Dhaka-1212, Bangladesh</div>

    <strong style="display: flex; justify-content: center; align-items: center" class="mb-3"
      >Transaction List</strong
    >
  <!-- </div> -->

  <!-- <div class="mb-3 mt-2 d-flex justify-content-between align-items-center"> -->
<div class="mb-3 mt-2 d-flex justify-content-between align-items-center no-print">

    <div></div>

    <div>
      <button class="btn btn-primary">
        <a href="/transactions-form/new" class="btn btn-primary">
          + Add Transaction
        </a>
      </button>
    </div>
    <div></div>

  </div>

  <table class="table table-bordered">
    <thead>
      <tr class="bg-dark text-white">
        <!--<th class="text-center">SL.</th>-->
        <th>Date</th>
        <th>Particulars</th>
        <th>Cheque</th>
        <!-- <th>Voucher</th> -->
        <th colspan="2" class="text-center">Folio</th>

        <th>Cash Amount</th>
        <th>Expencess Amount</th>
        <th>Bank Debit</th>
        <th>Bank Credit</th>

        <th>Account Head</th>
        <!-- <th>Action</th> -->
      </tr>
    </thead>
    <tbody>
      {% for tr in transactions %}
      <tr>
        <!--<th scope="row">{{ loop.index }}</th>-->
        <!-- <td>{% if tr.date %} {{ tr.date }} {% endif %}</td> -->

        <!-- <td class="text-nowrap">
        {% if tr.date %} {{ frappe.format_date(tr.date) }} {% endif %}
      </td> -->
        <td class="text-nowrap">
          <!-- {% if tr.date %} {{ frappe.format_date(tr.date) }} {% endif %} -->
          <!-- {% if tr.date %} {{ tr.date }} {% endif %} -->

          {% if tr.date %} {{ tr.date.strftime("%d-%m-%Y") }} {% endif %}
        </td>
        <!-- <td class="text-nowrap">
          {% if tr.particulars %} {{ tr.particulars }} {% endif %}
        </td> -->

        <td class="text-nowrap">
          {% if tr.particulars %} {% for i in range(0, tr.particulars|length,
          45) %} {{ tr.particulars[i:i+45] }}<br />
          {% endfor %} {% endif %}
        </td>

        <!-- <td >{% if tr.particulars %} {{ tr.particulars }} {% endif %}</td> -->
        <td>{% if tr.cheque %} {{ tr.cheque }} {% endif %}</td>
        <td>{% if tr.voucher_type %} {{ tr.voucher_type }} {% endif %}</td>
        <td>{% if tr.folio_no %} {{ tr.folio_no }} {% endif %}</td>

        {% if tr.type == 'Cash Amount'%}
        <td class="bg-info">{{tr.amount}}</td>
        <td class="bg-warning"></td>
        <td class="bg-warning"></td>
        <td class="bg-info"></td>

        {% elif tr.type == 'Expencess Amount' %}
        <td class="bg-info"></td>
        <td class="bg-warning">{{tr.amount}}</td>
        <td class="bg-warning"></td>
        <td class="bg-info"></td>

        {% elif tr.type == 'Bank Debit' %}
        <td class="bg-info"></td>
        <td class="bg-warning"></td>
        <td class="bg-warning">{{tr.amount}}</td>
        <td class="bg-info"></td>

        {% elif tr.type == 'Bank Credit' %}
        <td class="bg-info"></td>
        <td class="bg-warning"></td>
        <td class="bg-warning"></td>
        <td class="bg-info">{{tr.amount}}</td>
        {% endif %}

        <!-- <td>{% if tr.accounts_head %} {{ tr.accounts_head }} {% endif %}</td> -->
        <td class="text-nowrap">
          {% if tr.accounts_head %} {{frappe.get_doc("Accounts Head",
          tr.accounts_head, fields=["name1"]).name1 }} {% endif %}
        </td>
        <!-- <td>🗑️</td> -->
      </tr>

      {% endfor%}
    </tbody>
  </table>
</div>

```

# Context
```
context.transactions  = frappe.db.get_all("Transaction", fields="*") 
```

# Script
```

function printTable() {
  let printContents = document.getElementById("print-area").innerHTML;
  let originalContents = document.body.innerHTML;

  document.body.innerHTML = printContents;
  window.print();
  document.body.innerHTML = originalContents;

  location.reload();
}

```


# Style
```
@media print {
  .no-print {
    display: none !important;
  }
}

```


# SQL with python script

```

total_cash_amount = frappe.db.sql("""
    SELECT SUM(amount)
    FROM `tabTransaction`
    WHERE type='Cash Amount'
""")[0][0]

print("Total Cash =", total_cash_amount)

# 
# -------------------
#

total_cash_amount = frappe.db.sql("""
    SELECT SUM(amount)
    FROM `tabTransaction`
    WHERE type='Cash Amount' or type='Bank Credit'
""")[0][0]

print("Total Cash =", total_cash_amount)


```




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

""")