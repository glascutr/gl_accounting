function printTable() {
	let printContents = document.getElementById("print-area").innerHTML;
	let originalContents = document.body.innerHTML;

	document.body.innerHTML = printContents;
	window.print();
	document.body.innerHTML = originalContents;

	location.reload();
}

function submit_form(event) {
	event.preventDefault();

	const from_date = document.getElementById("from_date").value;
	const to_date = document.getElementById("to_date").value;

	frappe.call({
		method: "gl_accounting.reports.monthly_cost.get_monthly_cost",
		args: { from_date, to_date },
		freeze: true,
		freeze_message: "Loading transactions...",
		callback: function (r) {
			if (r.message) {
				// Show From/To Dates
				document.getElementById("report-results").innerHTML = `
                 <h5>Accounts Heads Wise Debit</h5>
                    <div class="alert alert-success">
                        <strong>From Date:</strong> ${from_date}<br>
                        <strong>To Date:</strong> ${to_date}
                    </div>
                `;

				// Build Debit Table
				let debitRows = "";
				r.message.accounts_heads_debit_summation.forEach((item, index) => {
					debitRows += `
                        <tr>
                            <td class="text-center">${index + 1}</td>
                            <td>${item.name1}</td>
                            <td class="text-right">${item.total_amount.toLocaleString()}</td>
                        </tr>
                    `;
				});

				document.getElementById("debit-table").innerHTML = `
                   
                    <table class="table table-bordered table-striped">
                        <thead class="fw bold thead-light table-warning">
                            <tr>
                                <th class="text-center">#SL</th>
                                <th>Account Name</th>
                                <th class="text-center">Total Amount</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${debitRows}
                            <tr class="fw bold table-warning">
                            <td colspan="2" class="text-center">Total</td>
                            <td class="text-right">${r.message.total_debit.toLocaleString()}</td>
                            </tr>

                        </tbody>
                    </table>
                
                `;
			}
		},
	});
}
