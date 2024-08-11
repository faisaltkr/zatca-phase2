import xml.etree.ElementTree as ET
import uuid
import frappe
from frappe.utils.data import  get_time
               
def  get_Issue_Time(invoice_number): 
                doc = frappe.get_doc("Purchase Invoice", invoice_number)
                time = get_time(doc.posting_time)
                issue_time = time.strftime("%H:%M:%S")  #time in format of  hour,mints,secnds
                # utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
                # issue_time = utc_now.strftime('%H:%M:%SZ') 
                return issue_time
  

def purchase_invoice_data(invoice,invoice_number):
            try:
                purchase_invoice_doc = frappe.get_doc('Purchase Invoice' ,invoice_number)
                cbc_ProfileID = ET.SubElement(invoice, "cbc:ProfileID")
                cbc_ProfileID.text = "reporting:1.0"
                cbc_ID = ET.SubElement(invoice, "cbc:ID")
                cbc_ID.text = str(purchase_invoice_doc.name)
                cbc_UUID = ET.SubElement(invoice, "cbc:UUID")
                uuid_val = str(uuid.uuid1())
                cbc_UUID.text =  uuid_val
                doc = frappe.get_doc('Purchase Invoice', purchase_invoice_doc.name)
                doc.set("custom_uuid", str(uuid_val))
                uuid1= cbc_UUID.text
                cbc_IssueDate = ET.SubElement(invoice, "cbc:IssueDate")
                cbc_IssueDate.text = str(purchase_invoice_doc.posting_date)
                cbc_IssueTime = ET.SubElement(invoice, "cbc:IssueTime")
                issue_time = get_Issue_Time(invoice_number)
                cbc_IssueTime.text = issue_time
                doc.set("custom_submit_time", str((str(purchase_invoice_doc.posting_date))+" "+issue_time))
                doc.save()
                return invoice ,uuid1 ,purchase_invoice_doc
            except Exception as e:
                    frappe.throw("error occured in salesinvoice data"+ str(e) )
