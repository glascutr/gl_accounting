frappe.ready(function () {

  if (document.getElementById('add-particulars-btn')) return;

  const btn = document.createElement('button');
  btn.id = 'add-particulars-btn';
  btn.type = 'button';
  btn.className = 'btn btn-sm btn-primary mt-2';
  btn.innerText = '➕ Add New Particulars';

  const interval = setInterval(function () {
    const particularsField = document.querySelector('[data-fieldname="particulars"]');
    if (particularsField) {
      clearInterval(interval);
      particularsField.after(btn);
      btn.addEventListener('click', add_new_particulars);
    }
  }, 300);

});

function add_new_particulars() {
  frappe.prompt(
    [
      {
        fieldname: 'title',
        fieldtype: 'Data',
        label: 'Particular Title',
        reqd: 1
      }
    ],
    function (values) {
      frappe.call({
        method: "gl_accounting.api.create_particular.add_particulars",
        args: { title: values.title },
        callback: function (r) {
          if (!r.exc) {
            frappe.msgprint(__('Particular Added Successfully'));

            // Auto-select newly created Particular by name
            frappe.web_form.set_value('particulars', r.message);
            frappe.web_form.refresh_field('particulars');
          }
        }
      });
    },
    __('Add New Particular'),
    __('Add')
  );
}
