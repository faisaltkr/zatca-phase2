import frappe

@frappe.whitelist()
def get_latest_purchase_invoice_with_hash():
    try:
        # Fetch the latest Sales Invoice that has an invoice hash
        purchase_invoice = frappe.get_all(
            'Purchase Invoice',
            fields=['custom_pih'],
            filters={'custom_pih': ['!=', ''],'custom_zatca_status': ['in', ['CLEARED', 'REPORTED']]},  # Filter for invoices with a non-empty hash
            order_by='modified desc',  # Sort by modification date in descending order
            limit=1  # Get only the latest one
        )
        
        if purchase_invoice:
            return purchase_invoice[0]['custom_pih']  # Return the latest invoice with a hash
        else:
            return 'NWZlY2ViNjZmZmM4NmYzOGQ5NTI3ODZjNmQ2OTZjNzljMmRiYzIzOWRkNGU5MWI0NjcyOWQ3M2EyN2ZiNTdlOQ=='
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Failed to retrieve latest purchase_invoice with hash")
        frappe.throw("An error occurred while fetching the latest purchase_invoice with an invoice hash")