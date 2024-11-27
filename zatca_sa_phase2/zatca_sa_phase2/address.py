import frappe

def set_customer_primary_address(doc, method):
    """
    Set the current address as the primary address for the linked customer
    when a new address is added.
    """
    # Check if the address has a linked customer
    supported_entities = ["Customer", "Supplier"]
    
    # Iterate through linked entities to check for Customer or Supplier
    for link in doc.links:
        if link.link_doctype in supported_entities:
            entity_name = link.link_name
            entity_type = link.link_doctype

            # Check if any other primary address exists for this entity
            existing_primary_address = frappe.db.sql(
                """
                SELECT parent
                FROM `tabDynamic Link`
                WHERE parenttype = 'Address'
                AND link_doctype = %s
                AND link_name = %s
                AND parent IN (
                    SELECT name FROM `tabAddress` WHERE is_primary_address = 1
                )
                """,
                (entity_type, entity_name),
            )

            # If no primary address exists, set the current one as primary
            if not existing_primary_address:
                frappe.db.set_value("Address", doc.name, "is_primary_address", 1)
                
                # Update the entity with the new primary address
                primary_address_field = (
                    "customer_primary_address"
                    if entity_type == "Customer"
                    else "supplier_primary_address"
                )
                frappe.db.set_value(entity_type, entity_name, primary_address_field, doc.name)
