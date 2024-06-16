import xml.etree.ElementTree as ET
import frappe

def delivery_And_PaymentMeans(invoice,sales_invoice_doc, is_return):
            try:
                cac_Delivery = ET.SubElement(invoice, "cac:Delivery")
                cbc_ActualDeliveryDate = ET.SubElement(cac_Delivery, "cbc:ActualDeliveryDate")
                cbc_ActualDeliveryDate.text = str(sales_invoice_doc.due_date)
                cac_PaymentMeans = ET.SubElement(invoice, "cac:PaymentMeans")
                cbc_PaymentMeansCode = ET.SubElement(cac_PaymentMeans, "cbc:PaymentMeansCode")
                cbc_PaymentMeansCode.text = "30"
                
                if is_return == 1:
                    cbc_InstructionNote = ET.SubElement(cac_PaymentMeans, "cbc:InstructionNote")
                    cbc_InstructionNote.text = "Cancellation"    
                return invoice
            except Exception as e:
                    frappe.throw("Delivery and payment means failed"+ str(e) )
                    
def delivery_And_PaymentMeans_for_Compliance(invoice,sales_invoice_doc, compliance_type):
            try:
                cac_Delivery = ET.SubElement(invoice, "cac:Delivery")
                cbc_ActualDeliveryDate = ET.SubElement(cac_Delivery, "cbc:ActualDeliveryDate")
                cbc_ActualDeliveryDate.text = str(sales_invoice_doc.due_date)
                cac_PaymentMeans = ET.SubElement(invoice, "cac:PaymentMeans")
                cbc_PaymentMeansCode = ET.SubElement(cac_PaymentMeans, "cbc:PaymentMeansCode")
                cbc_PaymentMeansCode.text = "30"
                
                if compliance_type == "3" or compliance_type == "4" or compliance_type == "5" or compliance_type == "6":
                    cbc_InstructionNote = ET.SubElement(cac_PaymentMeans, "cbc:InstructionNote")
                    cbc_InstructionNote.text = "Cancellation"    
                return invoice
            except Exception as e:
                    frappe.throw("Delivery and payment means failed"+ str(e) )