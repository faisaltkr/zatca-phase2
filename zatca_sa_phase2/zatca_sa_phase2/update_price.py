import frappe

def update_item_price(doc, method):
    # Check if the 'Tax Inclusive' checkbox is checked
    print(doc,"sdddddsdfsdfsdfsdfsdfsdfsdfsdfsfsfsdfsdf")
    data = doc.as_dict()
    tax =  data['taxes']
    print(tax)
    print(data['tax_inclusive'])
    if data['tax_inclusive'] and tax:
        print(222)
        item_tax = tax[0]['name']
        item_tax_template = frappe.get_doc("Item Tax Template", tax[0]['item_tax_template'])  # Use your actual template name

        tax_rate = item_tax_template.as_dict()['taxes'][0]['tax_rate']


        print(tax_rate,"tax ddd")
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
                'currency': 'SAR'  # Assuming the item uses the default currency
            })
            print(new_item_price)
            new_item_price.insert()
            frappe.db.commit()



# {'name': '8001', 'owner': 'Administrator', 'creation': '2024-10-11 04:26:32.049226', 'modified': '2024-10-11 05:02:45.500217', 'modified_by': 'Administrator', 'docstatus': 0, 'idx': 0, 'naming_series': 'STO-ITEM-.YYYY.-', 'item_code': '8001', 'item_name': 'ssssssss1ts', 'item_group': 'All Item Groups', 'stock_uom': 'Nos', 'tax_inclusive': 1, 'disabled': 0, 'allow_alternative_item': 0, 'is_stock_item': 1, 'has_variants': 0, 'include_item_in_manufacturing': 1, 'opening_stock': 0.0, 'valuation_rate': 0.0, 'standard_rate': 100.0, 'is_fixed_asset': 0, 'auto_create_assets': 0, 'is_grouped_asset': 0, 'asset_category': None, 'asset_naming_series': None, 'over_delivery_receipt_allowance': 0.0, 'over_billing_allowance': 0.0, 'image': None, 'description': 'test', 'is_zero_rated': 0, 'is_exempt': 0, 'brand': None, 'shelf_life_in_days': 0, 'end_of_life': '2099-12-31', 'default_material_request_type': 'Purchase', 'valuation_method': '', 'warranty_period': None, 'weight_per_unit': 0.0, 'weight_uom': None, 'allow_negative_stock': 0, 'has_batch_no': 0, 'create_new_batch': 0, 'batch_number_series': None, 'has_expiry_date': 0, 'retain_sample': 0, 'sample_quantity': 0, 'has_serial_no': 0, 'serial_no_series': None, 'variant_of': None, 'variant_based_on': 'Item Attribute', 'enable_deferred_expense': 0, 'no_of_months_exp': 0, 'enable_deferred_revenue': 0, 'no_of_months': 0, 'purchase_uom': None, 'min_order_qty': 0.0, 'safety_stock': 0.0, 'is_purchase_item': 1, 'lead_time_days': 0, 'last_purchase_rate': 0.0, 'is_customer_provided_item': 0, 'customer': None, 'delivered_by_supplier': 0, 'country_of_origin': 'Saudi Arabia', 'customs_tariff_number': None, 'sales_uom': None, 'grant_commission': 1, 'is_sales_item': 1, 'max_discount': 0.0, 'inspection_required_before_purchase': 0, 'quality_inspection_template': None, 'inspection_required_before_delivery': 0, 'is_sub_contracted_item': 0, 'default_bom': None, 'customer_code': '', 'default_item_manufacturer': None, 'default_manufacturer_part_no': None, 'published_in_website': 0, 'total_projected_qty': 0.0, 'doctype': 'Item', 'taxes': [{'name': '9suhdj90ev', 'owner': 'Administrator', 'creation': '2024-10-11 04:26:32.049226', 'modified': '2024-10-11 05:02:45.500217', 'modified_by': 'Administrator', 'docstatus': 0, 'idx': 1, 'item_tax_template': 'KSA VAT 15% - ET', 'tax_category': 'Standard Rated', 'valid_from': None, 'minimum_net_rate': 0.0, 'maximum_net_rate': 0.0, 'parent': '8001', 'parentfield': 'taxes', 'parenttype': 'Item', 'doctype': 'Item Tax', '__unsaved': 1}], 'barcodes': [], 'reorder_levels': [], 'supplier_items': [], 'customer_items': [], 'uoms': [{'name': '9suksvhist', 'owner': 'Administrator', 'creation': '2024-10-11 04:26:32.427613', 'modified': '2024-10-11 05:02:45.500217', 'modified_by': 'Administrator', 'docstatus': 0, 'idx': 1, 'uom': 'Nos', 'conversion_factor': 1.0, 'parent': '8001', 'parentfield': 'uoms', 'parenttype': 'Item', 'doctype': 'UOM Conversion Detail'}], 'attributes': [], 'item_defaults': [{'name': '9suk6mjif6', 'owner': 'Administrator', 'creation': '2024-10-11 04:26:32.444304', 'modified': '2024-10-11 05:02:45.500217', 'modified_by': 'Administrator', 'docstatus': 0, 'idx': 1, 'company': 'Exone Technologies', 'default_warehouse': 'Stores - ET', 'default_price_list': None, 'default_discount_account': None, 'buying_cost_center': None, 'default_supplier': None, 'expense_account': None, 'default_provisional_account': None, 'selling_cost_center': None, 'income_account': None, 'deferred_expense_account': None, 'deferred_revenue_account': None, 'parent': '8001', 'parentfield': 'item_defaults', 'parenttype': 'Item', 'doctype': 'Item Default'}], '__onload': {'stock_exists': 0, 'asset_naming_series': 'ACC-ASS-.YYYY.-'}, '__unsaved': 1}