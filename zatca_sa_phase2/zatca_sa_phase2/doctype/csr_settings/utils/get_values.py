import frappe


print("jjjjjjjj")
@frappe.whitelist()
def company():
    return {
        "name":"abc"
    }