import frappe


def get_item_group_tax(item_group_name):
    # Fetch the tax template associated with the Item Group
    item_group = frappe.get_doc("Item Group", item_group_name)
    
    data = item_group.as_dict()
    # Assuming there's a field or link to a tax template in the Item Group
    item_tax_template = frappe.get_doc("Item Tax Template", data['taxes'][0]['item_tax_template'])  # Use your actual template name
    tax_rate = item_tax_template.as_dict()['taxes'][0]['tax_rate']

    return tax_rate

def update_item_price(doc, method):
    # Check if the 'Tax Inclusive' checkbox is checked
    data = doc.as_dict()
    print(data)
    tax =  data['taxes']

    if data['tax_inclusive']:
        if data['tax_inclusive'] and tax:
            item_tax_template = frappe.get_doc("Item Tax Template", tax[0]['item_tax_template'])  # Use your actual template name
            tax_rate = item_tax_template.as_dict()['taxes'][0]['tax_rate']

        elif data['tax_inclusive']:
            
            group  = data['item_group']

            tax_rate =get_item_group_tax(group)

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
            print("jjjjjjj",doc.item_code)
            new_item_price = frappe.get_doc({
                'doctype': 'Item Price',
                'item_code': data['item_code'],
                'price_list': 'Standard Selling',  # Modify this if you use a different price list
                'price_list_rate': exclusive_price,
                'currency': 'SAR'  # Assuming the item uses the default currency
            })
            new_item_price.insert()
            frappe.db.commit()
