import frappe


print("jjjjjjjj")
@frappe.whitelist()
def company():

    return {
        "name":"abc"
    }


# def get_company_name():
#     try:
#         # Get the document
#         doc = frappe.get_doc('Company', docname)
        
#         # Get the field value
#         field_value = doc.get(fieldname)
        
#         print(f"Value of the field '{fieldname}': {field_value}")

#     except frappe.DoesNotExistError:
#         print(f"Document {docname} of Doctype {doctype_name} does not exist.")