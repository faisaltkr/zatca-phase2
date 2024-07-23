import frappe

def rename_fields():
    # Update the title field

    # Update the label of existing fields using Property Setter
    if not frappe.db.exists('Property Setter', {'doc_type': 'Address', 'field_name': 'address_line1', 'property': 'label'}):
        frappe.get_doc({
            'doctype': 'Property Setter',
            'doc_type': 'Address',
            'field_name': 'address_line1',
            'property': 'label',
            'value': 'Street Name'
        }).insert()

    if not frappe.db.exists('Property Setter', {'doc_type': 'Address', 'field_name': 'address_line2', 'property': 'label'}):
        frappe.get_doc({
            'doctype': 'Property Setter',
            'doc_type': 'Address',
            'field_name': 'address_line2',
            'property': 'label',
            'value': 'Building Number'
        }).insert()
    
            
    if not frappe.db.exists('Property Setter', {'doc_type': 'Sales Invoice', 'field_name': 'is_return', 'property': 'read_only'}):        # Create a new property setter to make the field read-only
        property_setter = frappe.get_doc({
            'doctype': 'Property Setter',
            'doc_type': 'Sales Invoice',
            'field_name': 'is_return',
            'property': 'read_only',
            'value': '1',
            'property_type': 'Check'
        })
        property_setter.insert()

    # Commit changes to the database
    frappe.db.commit()

# Call the function
rename_fields()