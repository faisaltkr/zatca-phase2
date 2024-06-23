// Copyright (c) 2024, Insys Softwares and contributors
// For license information, please see license.txt

frappe.ui.form.on('CSR Settings', {
    onload: function (frm) {
        // Check if the child table is empty before adding default rows

        // Add default row with specified values
        let default_rows = [
            { id_name: 'Commercial Registration Number', type_code: 'CRN' },
            { id_name: 'MOMRAH LICENCE', type_code: 'MOM' },
            { id_name: 'MHRSD LICENCE', type_code: 'MLS' },
            { id_name: 'Seven Hundred Number', type_code: '700' },
            { id_name: 'MISA LICENCE', type_code: 'SAG' },
            { id_name: 'OTHER ID', type_code: 'OTH' }
        ];

        // Refresh the field to reflect changes on the UI
        default_rows.forEach(row => {
            let child_row = frm.add_child('additional_ids', row);
        });

        // Refresh the field to reflect changes on the UI
        frm.refresh_field('additional_ids');

    },
    refresh: function(frm) {
            // Bind the custom button click event
            frm.fields_dict['generate_csr'].$input.on('click', function() {
                console.log("button clicked")
                let formData = frm.doc;
            
                // Print form data to the console
                console.log(formData);
                frappe.call({
                    method: 'zatca_sa_phase2.zatca_sa_phase2.doctype.csr_settings.utils.helpers.helpers',
                    args: {
                        name:formData
                    },
                    callback: function(r) {
                        if(r.message) {
                            frappe.msgprint({
                                title: __('Success'),
                                message: '<b style="color:green">' + r.message.message + '</b>',
                                indicator: 'red'
                            });
                            frm.set_value('private_key', r.message.key);
                            frm.set_value('public_key', r.message.public_key);


                        }
                    }
                });
            });
            frm.fields_dict['egs_onboard'].$input.on('click', function() {
                console.log("button clicked")
                let formData = frm.doc;
                frappe.call({
                    method: 'zatca_sa_phase2.zatca_sa_phase2.doctype.csr_settings.utils.helpers.csid',
                    args: {
                        dict:formData
                    },
                    callback: function(r) {
                        if(r.message) {
                            frappe.msgprint({
                                title: __('Success'),
                                message: '<b style="color:green">' + r.message.message + '</b>',
                                indicator: 'red'
                            });
                            frm.set_value('compliance_request_id', r.message.compliance_request_id);
                            frm.set_value('csr', r.message.csr);
                            frm.set_value('csid',r.message.csid);
                            frm.set_value('secret',r.message.secret);
                        }
                    }
                });
            });
        }
});