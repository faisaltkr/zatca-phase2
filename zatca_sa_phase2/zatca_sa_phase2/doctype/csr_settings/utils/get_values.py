import frappe


print("jjjjjjjj")
@frappe.whitelist()
def company():

    return {
        "name":"abc"
    }

@frappe.whitelist()
def get_company_name():
        # Get the document
    doc = frappe.get_all('Company',fields = ['name','country','default_currency','tax_id','domain',])

    company_billing_addresses = []
    
    for company in doc:
        # Get billing addresses linked to the current company
        billing_addresses = frappe.get_all('Address', 
                                           filters={'link_doctype': 'Company', 
                                                    'link_name': company['name'],
                                                    'address_type': 'Billing'},
                                           fields=['address_line1', 'address_line2', 'city', 'state', 'country', 'pincode','county'])

        for address in billing_addresses:
            company_billing_address = {
                'company_name': company['name'],
                'address_line1': address.get('address_line1', ''),
                'address_line2': address.get('address_line2', ''),
                'city': address.get('city', ''),
                'county': address.get('county', ''),

                'state': address.get('state', ''),
                'country': address.get('country', ''),
                'pincode': address.get('pincode', ''),
                'name':doc[0]['name'],
                'country':doc[0]['country'],
                'default_currency':doc[0]['default_currency'],
                'tax_id':doc[0]['tax_id'],
                'domain':doc[0]['domain'],
            }
            company_billing_addresses.append(company_billing_address)
    
    return company_billing_addresses[0]

# Call the function to get all company billing addresses
# all_company_billing_addresses = get_company_name()

# print(all_company_billing_addresses)
# for company_billing_address in all_company_billing_addresses:
#     print(f"Company: {company_billing_address['company_name']}, Address: {company_billing_address['address_line1']}, {company_billing_address['address_line2']}, {company_billing_address['city']}, {company_billing_address['state']}, {company_billing_address['country']}, {company_billing_address['pincode']}")        
        # Get the field value
        # field_value = doc.get(fieldname)
        
        # print(f"Value of the field '{fieldname}': {field_value}")

    # except frappe.DoesNotExistError:
        # print(f"Document {docname} of Doctype {doctype_name} does not exist.")
        # pass

# get_company_name()


def get_zatca_settings():
    doc = frappe.get_all('CSR Settings',fields = ['company_name','street','building_number','city','district','postal_code','vat_registration_number'])
    return doc[0]

print(get_zatca_settings())