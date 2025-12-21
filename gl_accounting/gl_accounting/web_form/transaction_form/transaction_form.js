// frappe.ready(function() {
// 	// bind events here
// })

frappe.ready(function () {

  // prevent duplicate button
  if (document.getElementById('add-particulars-btn')) {
    return;
  }

  // create button
  const btn = document.createElement('button');
  btn.id = 'add-particulars-btn';
  btn.type = 'button';
  btn.className = 'btn btn-sm btn-primary mt-2';
  btn.innerText = '➕ Add New Particulars';

  // wait until particulars field exists
  const interval = setInterval(function () {

    const particularsField = document.querySelector('[data-fieldname="particulars"]');

    if (particularsField) {
      clearInterval(interval);

      // insert button after field
      particularsField.after(btn);

      // click event
      btn.addEventListener('click', add_new_particulars);
    }

  }, 300);
});

function add_new_particulars() {

  frappe.prompt(
    [
      {
        fieldname: 'particulars',
        fieldtype: 'Data',
        label: 'Particulars',
        reqd: 1
      }
    ],
    function (values) {

      frappe.call({
        method: "gl_accounting.api.create_particular.add_particulars",
        args: {
          particulars: values.particulars
        },
        callback: function (r) {

          if (!r.exc) {
            frappe.msgprint(__('Particulars Added Successfully'));

            // refresh field safely
            frappe.web_form.refresh_field('particulars');
          }
        }
      });

    },
    __('Add New Particulars'),
    __('Add')
  );
}
