import xml.etree.ElementTree as ET
import uuid
import frappe
from frappe.utils.data import  get_time
               
def  get_Issue_Time(invoice_number): 
                doc = frappe.get_doc("Sales Invoice", invoice_number)
                time = get_time(doc.posting_time)
                issue_time = time.strftime("%H:%M:%S")  #time in format of  hour,mints,secnds
                # utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
                # issue_time = utc_now.strftime('%H:%M:%SZ') 
                return issue_time
  

def salesinvoice_data(invoice,invoice_number):
            try:
                sales_invoice_doc = frappe.get_doc('Sales Invoice' ,invoice_number)
                cbc_ProfileID = ET.SubElement(invoice, "cbc:ProfileID")
                cbc_ProfileID.text = "reporting:1.0"
                cbc_ID = ET.SubElement(invoice, "cbc:ID")
                cbc_ID.text = str(sales_invoice_doc.name)
                cbc_UUID = ET.SubElement(invoice, "cbc:UUID")
                cbc_UUID.text =  str(uuid.uuid1())
                uuid1= cbc_UUID.text
                cbc_IssueDate = ET.SubElement(invoice, "cbc:IssueDate")
                cbc_IssueDate.text = str(sales_invoice_doc.posting_date)
                cbc_IssueTime = ET.SubElement(invoice, "cbc:IssueTime")
                cbc_IssueTime.text = get_Issue_Time(invoice_number)
                return invoice ,uuid1 ,sales_invoice_doc
            except Exception as e:
                    frappe.throw("error occured in salesinvoice data"+ str(e) )
