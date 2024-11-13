
frappe.ui.form.on('CSR Settings', {

    company_name: function(frm) {
        // This function is triggered every time the Company field changes
        const company_name = frm.doc.company_name;
        // Call your custom function and pass the selected company name
        frappe.call({
            method: 'zatca_sa_phase2.zatca_sa_phase2.doctype.csr_settings.utils.get_values.get_company_name',
            args: {
                company_name: company_name
            },
            callback: function(response) {
                // Check if the call was successful and the value was retrieved
                if (response.message) {
                    // Set the value to the field
                    frm.set_value('company_name', response.message.company_name);
                    frm.set_value('street', response.message.address_line1);
                    frm.set_value('building_number', response.message.address_line2);
                    frm.set_value('city', response.message.city);
                    frm.set_value('district', response.message.county);
                    frm.set_value('postal_code', response.message.pincode);
                    frm.set_value('vat_registration_number', response.message.tax_id);
                } else {
                    frappe.msgprint('Failed to get value from the database.');
                }
            }
        });    
},

    refresh: function(frm) {
        // frm.set_value('company_name', '');

            // Bind the custom button click event
            frm.fields_dict['generate_csr'].$input.on('click', function() {
                let formData = frm.doc;
                frappe.show_alert({message: __("Generating CSR..."), indicator: 'green'}, 5);

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
                            frm.set_value('csr', r.message.csr);
                            frm.set_value('issuer_name', r.message.issuer_name);
                            frm.set_value('issuer_serial_number', r.message.s_no);


                        }
                    }
                });
            });
            frm.fields_dict['perform_compliance_check'].$input.on('click',function(){
                console.log("compliance button clicked");
                let formData =  frm.doc
                frappe.show_alert({message: __("Checking Compliance..."), indicator: 'blue'}, 5);

                frappe.call({
                    method: 'zatca_sa_phase2.zatca_sa_phase2.doctype.compliance.compliance.check_compliance',
                    args:{
                        data : formData
                    },
                    callback: function(r) {
                        console.log("hi")
                    }
                })
            });
            frm.fields_dict['get_production_csid'].$input.on('click',function(){
                console.log("Generating Production csid");
                let formData =  frm.doc
                frappe.show_alert({message: __("Generating Production CSID..."), indicator: 'blue'}, 5);

                frappe.call({
                    method: 'zatca_sa_phase2.zatca_sa_phase2.doctype.csr_settings.utils.p_csid.generate_pcsid',
                    args:{
                        data : formData
                    },
                    callback: function(r) {
                        console.log(r)
                        if(r.message.success ==='true')
                        {
                        frappe.msgprint({
                                title: __('Success'),
                                message: '<b style="color:green">' + r.message.message + '</b>',
                                indicator: 'red'
                        });
                        frm.set_value('production_csid', r.message.token);
                        }
                        else{
                            frappe.msgprint({
                                title: __('Failed'),
                                message: '<b style="color:red">' + r.message.error.errors + '</b>',
                                indicator: 'red'
                            });
                        }
                    }
                })
            });
            frm.fields_dict['egs_onboard'].$input.on('click', function() {
                frappe.show_alert({message: __("Generating CSID..."), indicator: 'green'}, 5);
                let formData = frm.doc;
                frappe.call({
                    method: 'zatca_sa_phase2.zatca_sa_phase2.doctype.csr_settings.utils.helpers.csid',
                    args: {
                        dict:formData
                    },
                    callback: function(r) {
                        if(r.message.success ==='true') {
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
                        else{
                            frappe.msgprint({
                                title: __('Failed'),
                                message: '<b style="color:red">' + r.message.error.errors + '</b>',
                                indicator: 'red'
                            });
                        }
                    }
                });
            });
        },
        additional_id: function(frm) {
            // Check if the select field has a value
            //alert('hhhhh')
            if (frm.doc.additional_id) {
                $(frm.fields_dict.value_number.input).focus();
                
            }
        },

});
