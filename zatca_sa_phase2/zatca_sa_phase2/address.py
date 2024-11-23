import frappe

def set_customer_primary_address(doc, method):
    """
    Set the current address as the primary address for the linked customer
    when a new address is added.
    """
    # Check if the address has a linked customer
    customer_link = next((link for link in doc.links if link.link_doctype == "Customer"), None)
    
    if customer_link:
        customer_name = customer_link.link_name

        # Check if any other primary address exists for this customer
        existing_primary_address = frappe.db.sql(
            """
            SELECT parent
            FROM `tabDynamic Link`
            WHERE parenttype = 'Address'
            AND link_doctype = 'Customer'
            AND link_name = %s
            AND parent IN (
                SELECT name FROM `tabAddress` WHERE is_primary_address = 1
            )
            """,
            (customer_name,),
        )

        # If no primary address exists, set the current one as primary
        if not existing_primary_address:
            frappe.db.set_value("Address", doc.name, "is_primary_address", 1)
            frappe.db.set_value("Customer", customer_name, "customer_primary_address", doc.name)
