// Copyright (c) 2024, Insys Softwares and contributors
// For license information, please see license.txt

// frappe.your_hook_name = function(cur_doc) {
//     // Replace with your actual HTML content for the extra tab
//     var html_content = `
//       <div class="custom-tab">
//         <h2>Extra Tab</h2>
//         <p>This is the content of the extra tab. You can display data from your library management app here using JavaScript.</p>
//         <div id="dynamic-content"></div>  </div>
//     `;
  
//     // Inject the HTML content into the sales invoice form using jQuery
//     if (cur_doc.doctype === "Sales Invoice") {
//       $(document).ready(function() {
//         // Replace with the appropriate selector to target the desired location in the form
//         $("#sales_invoice_form").find(".frappe-form-group").last().after(html_content);
  
//         // Example: Fetch data from library management app using frappe.get_doc (replace with your logic)
//         var library_item_code = cur_doc.get("library_item_code");  // Assuming a library item code field exists
//         if (library_item_code) {
//           frappe.get_doc("Library Item", library_item_code, function(library_item) {
//             var content = `
//               <p>Borrower Name: ${library_item.borrower_name}</p>
//               <p>Due Date: ${library_item.due_date}</p>
//             `;
//             $("#dynamic-content").html(content);  // Update the placeholder with fetched data
//           });
//         }
//       });
//     }
//   };

console.log("jjjjjjjjjjjjj")


frappe.ui.form.on('CSR Settings', {
    onload: function(frm) {
    
        // Fetch value from the database asynchronously
        frappe.call({
            method: 'zatca_sa_phase2.zatca_sa_phase2.doctype.csr_settings.utils.get_values.get_company_name',
            args: {
                // Add any arguments needed for your method here
            },
            callback: function(response) {
                // Check if the call was successful and the value was retrieved
                console.log(response)
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
                            frm.set_value('csr', r.message.csr);

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



frappe.ui.form.on('CSR Settings', {
    onload: function(frm) {


}});