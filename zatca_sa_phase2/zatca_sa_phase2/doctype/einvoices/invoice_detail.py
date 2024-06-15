import xml.etree.ElementTree as ET
import uuid 


def salesinvoice_data(invoice):
            try:
                # sales_invoice_doc = frappe.get_doc('Sales Invoice' ,invoice_number)
                cbc_ProfileID = ET.SubElement(invoice, "cbc:ProfileID")
                cbc_ProfileID.text = "reporting:1.0"
                cbc_ID = ET.SubElement(invoice, "cbc:ID")
                cbc_ID.text = "MKL00034"
                cbc_UUID = ET.SubElement(invoice, "cbc:UUID")
                cbc_UUID.text =  str(uuid.uuid1())
                uuid1= cbc_UUID.text
                cbc_IssueDate = ET.SubElement(invoice, "cbc:IssueDate")
                cbc_IssueDate.text = "2022-09-0"
                cbc_IssueTime = ET.SubElement(invoice, "cbc:IssueTime")
                cbc_IssueTime.text = "12:21:28"
                return invoice
            except Exception as e:
                    print(str(e))
