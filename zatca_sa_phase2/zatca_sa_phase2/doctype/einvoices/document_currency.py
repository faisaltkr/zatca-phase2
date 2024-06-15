import xml.etree.ElementTree as ET
import uuid 


def currency_data(invoice):
            try:
                # sales_invoice_doc = frappe.get_doc('Sales Invoice' ,invoice_number)
                cbc_DocumentCurrencyCode = ET.SubElement(invoice, "cbc:DocumentCurrencyCode")
                cbc_DocumentCurrencyCode.text = "SAR"
                cbc_TaxCurrencyCode = ET.SubElement(invoice, "cbc:TaxCurrencyCode")
                cbc_TaxCurrencyCode.text = "SAR"
                return invoice
            except Exception as e:
                    print(str(e))