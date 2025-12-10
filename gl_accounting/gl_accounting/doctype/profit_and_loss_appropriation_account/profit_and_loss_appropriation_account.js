// Copyright (c) 2025, Glascutr Limited and contributors
// For license information, please see license.txt

// frappe.ui.form.on("Profit and Loss Appropriation Account", {
// 	refresh(frm) {

// 	},
// });


// Copyright (c) 2025, Glascutr Limited

frappe.ui.form.on('Profit and Loss Appropriation Account', {

    refresh(frm) {
        
        // Live typing bind for both fields
        bind_live_calculation(frm, 'previous_year_profit_or_loss_amount');
        bind_live_calculation(frm, 'current_year_profit_or_loss_amount');

        calculate_profit(frm);
    },

    previous_year_profit_or_loss_amount(frm) {
        calculate_profit(frm);
    },

    current_year_profit_or_loss_amount(frm) {
        calculate_profit(frm);
    }

});

function bind_live_calculation(frm, fieldname) {

    setTimeout(() => {
        let $input = frm.fields_dict[fieldname].$input;

        if ($input) {
            $input.on('input', function () {
                calculate_profit(frm);
            });
        }
    }, 300);

}

function calculate_profit(frm) {

    let prev = flt(frm.doc.previous_year_profit_or_loss_amount);
    let curr = flt(frm.doc.current_year_profit_or_loss_amount);

    let total = prev + curr;

    frm.set_value('total_balance', total);

}
