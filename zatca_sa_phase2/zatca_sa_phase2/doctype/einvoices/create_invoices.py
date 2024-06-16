"""
class to create invoice standard and simplified
"""
import xml.etree.ElementTree as ET
from .xml_tags import generate_xml_tags
from .invoice_detail import salesinvoice_data
from .document_currency import currency_data
from .utils import base_64_hash,get_private_path,dateformat,timeformat
import os
import frappe


class SimplifiedInvoice:

    def __init__(self, cih, pih=None) -> None:
        """
        if invoice hash is not present then hash value of zero as pih
        """
        self.pih = pih
        self.cih = cih
        if not pih:
            self.pih = base_64_hash('0')
        

    def create_simplified_invoice(self):
        """
        invoice generate for simplified
        """
        xml_tags = generate_xml_tags()
        inv_data = salesinvoice_data(xml_tags)
        cur = currency_data(inv_data)
        return cur
    
# file name  - vatnumber-datetime-invoicenumber //yyyy-mm-dd-hh-mm-ss //3xxxxxxxxx1xxx3_20210526T132400_2021-05-26-23555.xml
def create_invoice(doc,method):
    print(doc)
    simp =  SimplifiedInvoice(1,pih=123)
    simp_inv = simp.create_simplified_invoice()
    tree = ET.ElementTree(simp_inv)


    #create path to save xmls if not exits
    private_path = get_private_path()
    if not os.path.exists(private_path+'/xmls'):
        os.makedirs(private_path+'/xmls')

    current_date = dateformat()
    current_time = timeformat()
    get_vat()

    tree.write(f"{private_path}/xmls/invoice_simple.xml", encoding="utf-8", xml_declaration=True)
    return True



def get_vat():
    docs = frappe.get_all('CSR Settings', fields=['name', 'vat_registration_number'])

    try:
        # Get the last added document (most recent) with all fields
        docs = frappe.get_list('CSR Settings', fields='*', order_by='creation desc', limit=1)
        
        # Iterate through the documents and print all field values
        for doc in docs:
            print(f"Document: {doc}")

    except frappe.DoesNotExistError:
        print(f"No documents found for Doctype.")


