// frappe.ready(function() {
// 	// bind events here
// })


frappe.ready(function () {

  const FIELDNAME = 'particulars';

  // listen when link field gets focus
  $(document).on('focus', `[data-fieldname="${FIELDNAME}"] input`, function () {
    setTimeout(add_button_to_link_dropdown, 200);
  });

  function add_button_to_link_dropdown() {
    const $dropdown = $('.awesomplete ul');

    // prevent duplicate button
    if (!$dropdown.length || $dropdown.find('.add-particular-item').length) return;

    const $btnItem = $(`
      <li class="add-particular-item text-center p-2">
        <button type="button"
          class="btn btn-sm btn-outline-primary btn-block">
          <i class="fa fa-plus-circle mr-1"></i>
          Add New Particular
        </button>
      </li>
    `);

    $btnItem.on('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      add_new_particulars();
    });

    $dropdown.append($btnItem);
  }
});

function add_new_particulars() {
  frappe.prompt(
    [
      {
        fieldname: 'title',
        fieldtype: 'Data',
        label: 'Particular Title',
        reqd: 1,
        placeholder: 'e.g. Office Rent / Transport Cost'
      }
    ],
    function (values) {
      frappe.call({
        method: "gl_accounting.api.create_particular.add_particulars",
        args: { title: values.title },
        freeze: true,
        freeze_message: __("Creating Particular..."),
        callback: function (r) {
          if (!r.exc && r.message) {
            const { name, title } = r.message;

            frappe.show_alert(
              {
                message: __('<strong>Success!</strong> ' + title + ' added'),
                indicator: 'green'
              },
              4
            );

            frappe.web_form.set_value('particulars', name);
            frappe.web_form.refresh_field('particulars');

            // show title instead of name
            const input = document.querySelector('[data-fieldname="particulars"] input');
            if (input) input.value = title;
          }
        }
      });
    },
    __('Add New Particular'),
    __('Add')
  );
}
