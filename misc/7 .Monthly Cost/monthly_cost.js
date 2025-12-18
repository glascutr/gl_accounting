function printTable() {
	let printContents = document.getElementById("print-area").innerHTML;
	let originalContents = document.body.innerHTML;

	document.body.innerHTML = printContents;
	window.print();
	document.body.innerHTML = originalContents;

	location.reload();
}

function formatDateDDMMYYYY(dateStr) {
	let [year, month, day] = dateStr.split("-");
	return `${day}-${month}-${year}`;
}

function submit_form(event) {
	event.preventDefault();

	const from_date = document.getElementById("from_date").value;
	const to_date = document.getElementById("to_date").value;

	console.log("from_date: ", from_date);

	frappe.call({
		method: "gl_accounting.reports.monthly_cost.get_monthly_cost",
		args: { from_date, to_date },
		freeze: true,
		freeze_message: "Loading transactions...",
		callback: function (r) {
			if (r.message) {
				// Show From/To Dates
				document.getElementById("report-results").innerHTML = `
					<h5 class="text-center mb-3">Accounts Heads Wise Debit</h5>
					<div class="alert alert-info text-center">
						<strong>From Date:</strong> ${formatDateDDMMYYYY(from_date)} &nbsp;&nbsp;
						<strong>To Date:</strong> ${formatDateDDMMYYYY(to_date)}
					</div>
				`;

				// Build Debit Table
				let debitRows = r.message.accounts_heads_debit_summation
					.map((item, index) => {
						return `
						<tr>
							<td class="text-center align-middle">${index + 1}</td>
							<td class="align-middle">${item.name1}</td>
							<td class="text-right align-middle">${item.total_amount.toLocaleString()}</td>
						</tr>
					`;
					})
					.join("");

				document.getElementById("debit-table").innerHTML = `

                <div class="container mb-4">
                    <div class="row g-4">
                        <!-- Debit -->
                        <div class="col-md-12">
                            <div class="card shadow border-0 h-100">
                                <div class="card-header bg-warning bg-gradient text-white">
                                    <h5 class="mb-0 fw-semibold">💳 Debit</h5>
                                </div>

                                <div class="card-body p-3"> 

                                    <div class="table-responsive shadow-sm rounded">
                                        <table class="table table-bordered table-striped table-hover mb-0">
                                            <thead class="thead-dark">
                                                <tr>
                                                    <th class="text-center">#SL</th>
                                                    <th>Account Name</th>
                                                    <th class="text-center">Total Amount</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                ${debitRows}
                                                <tr class="fw-bold table-warning">
                                                    <td colspan="2" class="text-center">Total</td>
                                                    <td class="text-right">${r.message.total_debit.toLocaleString()}</td>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>
                                    </div>
                                </div>
                            </div>
                        </div>
					</div>
				`;
			}
		},
	});
}
