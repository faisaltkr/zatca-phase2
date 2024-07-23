import xml.etree.ElementTree as ET
import frappe


invoice_Typecode_Simplified_dict = {
      'Third Party': '0210000',
      'Nominal Invoice': '0201000',
      'Export Invoice': '0200100',
      'Summary Invoice': '0200010',
      'Self Billed': '0200001'
}
invoice_Typecode_Standard_dict = {
      'Third Party': '0110000',
      'Nominal Invoice': '0101000',
      'Export Invoice': '0100100',
      'Summary Invoice': '0100010',
      'Self Billed': '0100001'
}


def invoice_Typecode_Simplified(invoice,sales_invoice_doc):
            try:                             
                cbc_InvoiceTypeCode = ET.SubElement(invoice, "cbc:InvoiceTypeCode")
                if sales_invoice_doc.custom_invoice_transaction_type1 in invoice_Typecode_Simplified_dict:
                    type_code = invoice_Typecode_Simplified_dict[sales_invoice_doc.custom_invoice_transaction_type1]
                else:
                    type_code = "0200000"
                cbc_InvoiceTypeCode.set("name", type_code) # Simplified

                if sales_invoice_doc.is_return == 0 and sales_invoice_doc.is_debit_note !=1: 

                    # cbc_InvoiceTypeCode.set("name", type_code) # Simplified
                    cbc_InvoiceTypeCode.text = "388"
                elif sales_invoice_doc.is_return == 1:       # return items and simplified invoice
                    # cbc_InvoiceTypeCode.set("name", type_code)  # Simplified,
                    cbc_InvoiceTypeCode.text = "381"  # Credit note
                elif sales_invoice_doc.is_debit_note == 1:
                        cbc_InvoiceTypeCode.text = "383" # Debit note
                        # cbc_billing_reference = ET.SubElement(invoice,"cac:BillingReference")
                        # cbc_cac_InvoiceDocumentReference  = ET.SubElement(cbc_billing_reference,"cac:InvoiceDocumentReference")
                        # cbc_id = ET.SubElement(cbc_cac_InvoiceDocumentReference,"cbc:ID")
                        # cbc_id.text = sales_invoice_doc.return_against
                return invoice
            except Exception as e:
                    frappe.throw("error occured in simplified invoice typecode"+ str(e) )

def invoice_Typecode_Standard(invoice,sales_invoice_doc):
            try:
                    # print(sales_invoice_doc.custom_invoice_transaction_type1,"lsdjfdslfjdlflfdjkl")
                    if sales_invoice_doc.custom_invoice_transaction_type1 in invoice_Typecode_Standard_dict:
                          type_code = invoice_Typecode_Standard_dict[sales_invoice_doc.custom_invoice_transaction_type1]
                    else:
                          type_code = "0100000"
                    cbc_InvoiceTypeCode = ET.SubElement(invoice, "cbc:InvoiceTypeCode")
                    cbc_InvoiceTypeCode.set("name", type_code) # Standard
                    # frappe.throw("Error in standard invoice type code: ")

                    if sales_invoice_doc.is_return == 0 and sales_invoice_doc.is_debit_note !=1:
                        cbc_InvoiceTypeCode.text = "388"
                    elif sales_invoice_doc.is_return == 1:     # return items and simplified invoice
                        cbc_InvoiceTypeCode.text = "381" # Credit note
                    elif sales_invoice_doc.is_debit_note == 1:
                        cbc_InvoiceTypeCode.text = "383" # Debit note
                        # cbc_billing_reference = ET.SubElement(invoice,"cac:BillingReference")
                        # cbc_cac_InvoiceDocumentReference  = ET.SubElement(cbc_billing_reference,"cac:InvoiceDocumentReference")
                        # cbc_id = ET.SubElement(cbc_cac_InvoiceDocumentReference,"cbc:ID")
                        # cbc_id.text = sales_invoice_doc.return_against

                    return invoice
            except Exception as e:
                    frappe.throw("Error in standard invoice type code: "+ str(e))

def invoice_Typecode_Compliance(invoice,compliance_type):
                    # 0 is default. Not for compliance test. But normal reporting or clearance call.
                    # 1 is for compliance test. Simplified invoice
                    # 2 is for compliance test. Standard invoice
                    # 3 is for compliance test. Simplified Credit Note
                    # 4 is for compliance test. Standard Credit Note
                    # 5 is for compliance test. Simplified Debit Note
                    # 6 is for compliance test. Standard Debit Note
            # frappe.throw(str("here 5 " + str(compliance_type)))
            try:                         
                # cbc_InvoiceTypeCode = ET.SubElement(invoice, "cbc:InvoiceTypeCode")
                # cbc_InvoiceTypeCode.set("name", "0200000")
                # cbc_InvoiceTypeCode.text = "388"
                # return invoice
                 
                if compliance_type == "1":       # simplified invoice
                    cbc_InvoiceTypeCode = ET.SubElement(invoice, "cbc:InvoiceTypeCode") 
                    cbc_InvoiceTypeCode.set("name", "0200000")
                    cbc_InvoiceTypeCode.text = "388"
                    
                elif compliance_type == "2":       # standard invoice
                    cbc_InvoiceTypeCode = ET.SubElement(invoice, "cbc:InvoiceTypeCode")
                    cbc_InvoiceTypeCode.set("name", "0100000")
                    cbc_InvoiceTypeCode.text = "388"
                  
                elif compliance_type == "3":       # simplified Credit note
                    cbc_InvoiceTypeCode = ET.SubElement(invoice, "cbc:InvoiceTypeCode")
                    cbc_InvoiceTypeCode.set("name", "0200000")
                    cbc_InvoiceTypeCode.text = "381"
                    
                   
                elif compliance_type == "4":       # Standard Credit note
                    cbc_InvoiceTypeCode = ET.SubElement(invoice, "cbc:InvoiceTypeCode")
                    cbc_InvoiceTypeCode.set("name", "0100000")
                    cbc_InvoiceTypeCode.text = "381"
                   
                elif compliance_type == "5":       # simplified Debit note
                    cbc_InvoiceTypeCode = ET.SubElement(invoice, "cbc:InvoiceTypeCode")
                    cbc_InvoiceTypeCode.set("name", "0211000")
                    cbc_InvoiceTypeCode.text = "383"
                   
                elif compliance_type == "6":       # Standard Debit note
                    cbc_InvoiceTypeCode = ET.SubElement(invoice, "cbc:InvoiceTypeCode")
                    cbc_InvoiceTypeCode.set("name", "0100000")
                    cbc_InvoiceTypeCode.text = "383"
                return invoice
                
                
                
            except Exception as e:
                    frappe.throw("error occured in Compliance typecode"+ str(e) )