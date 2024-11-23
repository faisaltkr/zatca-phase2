# sales_invoice.py
import frappe
from frappe.model.document import Document
from .create_invoices import zatca_Background_on_submit
import  json

@frappe.whitelist()
def resend(data):
        # Your custom logic here
        data = json.loads(data)
        sales_invoice = frappe.get_doc('Sales Invoice', data['name'])
        print(sales_invoice,"dsssss")
        zatca_Background_on_submit(sales_invoice)
        
        frappe.msgprint("Backend function called!")
        
        return {
            "message":"resend"
        }