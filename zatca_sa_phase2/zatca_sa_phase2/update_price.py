import frappe

def update_item_price(doc, method):
    # Check if the 'Tax Inclusive' checkbox is checked
    print(doc)
    if doc.custom_tax_inclusive and not doc.taxes:
        tax_rate = 0

        item_tax_template = doc.taxes

        # Check if an Item Tax Template is linked to the item
        if item_tax_template:
            # Fetch the tax rate from the Item Tax child table inside the Item Tax Template
            taxes = frappe.get_all("Item Tax", filters={"parent": item_tax_template}, fields=["tax_rate"])

            if taxes:
                tax_rate = taxes[0].tax_rate  # Assuming the first tax entry is the one to use; modify if needed

        # If a valid tax rate was found, calculate the price excluding tax
        if tax_rate > 0:
            # Calculate exclusive price from the tax-inclusive price
            exclusive_price = doc.standard_rate / (1 + tax_rate / 100)
        else:
            exclusive_price = doc.standard_rate  # No tax template, assume price is exclusive already

        # Check if an Item Price entry exists for the item and update or insert accordingly
        existing_price = frappe.get_all('Item Price', filters={
            'item_code': doc.item_code, 
            'price_list': 'Standard Selling'  # Modify this if you're using a different price list
        }, fields=['name'])

        if existing_price:
            # Update the existing Item Price with the exclusive price
            frappe.db.set_value('Item Price', existing_price[0].name, 'price_list_rate', exclusive_price)
        else:
            # Create a new Item Price record
            new_item_price = frappe.get_doc({
                'doctype': 'Item Price',
                'item_code': doc.item_code,
                'price_list': 'Standard Selling',  # Modify this if you use a different price list
                'price_list_rate': exclusive_price,
                'currency': doc.default_currency  # Assuming the item uses the default currency
            })
            print(new_item_price)
            new_item_price.insert()
            frappe.db.commit()

