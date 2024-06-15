// Copyright (c) 2024, Insys Softwares and contributors
// For license information, please see license.txt

frappe.ui.form.on('CSR Settings', {
    onload: function(frm) {
        // Fetch value from the database asynchronously
        frappe.call({
            method: 'zatca_sa_phase2.zatca_sa_phase2.doctype.csr_settings.utils.get_values.company',
            args: {
                // Add any arguments needed for your method here
            },
            callback: function(response) {
                // Check if the call was successful and the value was retrieved
                console.log(response)
                if (response.message) {
                    // Set the value to the field
                    frm.set_value('company_name', response.message.name);
                } else {
                    frappe.msgprint('Failed to get value from the database.');
                }
            }
        });
    },
    refresh: function(frm) {
            // Bind the custom button click event
            frm.fields_dict['generate_csr'].$input.on('click', function() {
                console.log("button clicked")
                let formData = frm.doc;
            
                // Print form data to the console
                console.log(formData);
                // Define what happens when the button is clicked
                // frappe.msgprint(__('Custom button clicked!'));
    
                // Perform additional actions here
                frappe.call({
                    method: 'zatca_sa_phase2.zatca_sa_phase2.doctype.csr_settings.utils.helpers.helpers',
                    args: {
                        name:formData
                    },
                    callback: function(r) {
                        if(r.message) {
                            frappe.msgprint({
                                title: __('Error'),
                                message: 'Server-side method response: <b style="color:red">' + r.message + '</b>',
                                indicator: 'red'
                            });
                        }
                    }
                });
            });
        }
});