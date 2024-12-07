import frappe

def set_customer_primary_address(doc, method):
    print("ddd")
    """
    Set the current address as the primary address for the linked Customer or Supplier
    if no primary address is currently set.
    """
    # Define the mapping of primary address fields for supported entities
    entity_primary_address_field = {
        "Customer": "customer_primary_address",
        "Supplier": "supplier_primary_address",
    }

    # Iterate through links to identify if the address is linked to a Customer or Supplier
    for link in doc.links:
        if link.link_doctype in entity_primary_address_field:
            entity_type = link.link_doctype
            entity_name = link.link_name
            primary_address_field = entity_primary_address_field[entity_type]

            # Check if the entity already has a primary address set
            current_primary_address = frappe.db.get_value(
                entity_type, entity_name, primary_address_field
            )

            if not current_primary_address:
                # Set the current address as primary
                frappe.db.set_value("Address", doc.name, "is_primary_address", 1)

                # Update the Customer/Supplier with the new primary address
                frappe.db.set_value(entity_type, entity_name, primary_address_field, doc.name)

                frappe.msgprint(
                    f"The address {doc.name} has been set as the primary address for {entity_type} {entity_name}.",
                    alert=True,
                )
            else:
                frappe.msgprint(
                    f"{entity_type} {entity_name} already has a primary address: {current_primary_address}. No changes made.",
                    alert=True,
                )
