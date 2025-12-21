frappe.ready(function () {

  // prevent duplicate button
  if (document.getElementById('add-particulars-btn')) return;

  // create button
  const btn = document.createElement('button');
  btn.id = 'add-particulars-btn';
  btn.type = 'button';
  btn.className = 'btn btn-sm btn-primary mt-2';
  btn.innerText = '➕ Add New Particulars';

  // wait until particulars field is rendered
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
          if (!r.exc && r.message) {
            const { name, title } = r.message;

            // Show success message with title
            frappe.msgprint(__('Particular Added Successfully: ' + title));

            // Set the field value as the DocType name
            frappe.web_form.set_value('particulars', name);
            frappe.web_form.refresh_field('particulars');

            // Update Link field display (so user sees title)
            const $linkField = document.querySelector('[data-fieldname="particulars"]');
            if ($linkField) {
              const linkInput = $linkField.querySelector('input[type="text"]');
              if (linkInput) linkInput.value = title;
            }
          }
        }
      });
    },
    __('Add New Particular'),
    __('Add')
  );
}
