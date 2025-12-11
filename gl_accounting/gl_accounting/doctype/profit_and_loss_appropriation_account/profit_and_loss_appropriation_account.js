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
        bind_live_calculation(frm, 'is_previous_year_profit');
        bind_live_calculation(frm, 'current_year_profit_or_loss_amount');
        bind_live_calculation(frm, 'is_current_year_profit');
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

    let is_prev_year_profit = flt(frm.doc.is_previous_year_profit);
    let prev = flt(frm.doc.previous_year_profit_or_loss_amount);
    let is_curr_year_profit = flt(frm.doc.is_current_year_profit);
    let curr = flt(frm.doc.current_year_profit_or_loss_amount);

    let total = 0;
    let balance_loss = 0
    let balance_profit = 0
    let is_profit = false

    if (is_prev_year_profit==true && is_curr_year_profit==true){

        total = prev + curr;
        balance_profit =  prev + curr;
        is_profit = true;

    }
    else if (is_prev_year_profit==false && is_curr_year_profit==false){

        total =  prev + curr;
        balance_loss = prev + curr;

    }
   
    else if (is_prev_year_profit==true && is_curr_year_profit==false){

        if(prev >= curr){
            balance_profit =  prev - curr;
            is_profit = true;
            total = balance_profit;
        }
        else{
            balance_loss =  curr - prev;
            is_profit = false;
            total = balance_loss;

        }

    }
   
    else if (is_prev_year_profit==false && is_curr_year_profit==true){

        if(prev > curr){
            balance_loss =  prev - curr;
            is_profit = false;
            total = balance_loss;
        }
        else{
            balance_profit =  curr - prev;
            is_profit = true;
            total = balance_profit;

        }

    }
   


    // let total = prev + curr;

    frm.set_value('is_profit', is_profit);
    frm.set_value('total_balance', total);

}
