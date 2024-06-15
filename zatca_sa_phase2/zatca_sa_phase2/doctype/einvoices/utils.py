import xml.etree.ElementTree as ET
import re
import hashlib
import base64

def base_64_hash(data):
        sha256_hash = hashlib.sha256(data.encode('utf-8')).digest()

        # Convert hash to hexadecimal string
        hex_hash = sha256_hash.hex()

        # Encode the hexadecimal hash in base64
        base64_encoded_hash = base64.b64encode(hex_hash.encode('utf-8')).decode('utf-8')

        return base64_encoded_hash

def invoice_Typecode_Compliance(invoice,compliance_type="1"):
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
                    print(str(e))



def billing_reference_for_credit_and_debit_note(invoice,sales_invoice_doc):
            try:
                #details of original invoice
                cac_BillingReference = ET.SubElement(invoice, "cac:BillingReference")
                cac_InvoiceDocumentReference = ET.SubElement(cac_BillingReference, "cac:InvoiceDocumentReference")
                cbc_ID13 = ET.SubElement(cac_InvoiceDocumentReference, "cbc:ID")
                cbc_ID13.text = sales_invoice_doc.return_against  # field from return against invoice. 
                
                return invoice
            except Exception as e:
                    print(str(e))

def get_ICV_code(invoice_number):
                try:
                    icv_code =  re.sub(r'\D', '', invoice_number)   # taking the number part only from doc name
                    return icv_code
                except Exception as e:
                    str(e)

       
def doc_Reference(invoice,sales_invoice_doc='1',invoice_number="DFSDF2434534959459"):
            try:
                cbc_DocumentCurrencyCode = ET.SubElement(invoice, "cbc:DocumentCurrencyCode")
                cbc_DocumentCurrencyCode.text = sales_invoice_doc.currency
                cbc_TaxCurrencyCode = ET.SubElement(invoice, "cbc:TaxCurrencyCode")
                cbc_TaxCurrencyCode.text = "SAR"  # SAR is as zatca requires tax amount in SAR
                # if sales_invoice_doc.is_return == 1:
                if True:
                    invoice=billing_reference_for_credit_and_debit_note(invoice,sales_invoice_doc)
                cac_AdditionalDocumentReference = ET.SubElement(invoice, "cac:AdditionalDocumentReference")
                cbc_ID_1 = ET.SubElement(cac_AdditionalDocumentReference, "cbc:ID")
                cbc_ID_1.text = "ICV"
                cbc_UUID_1 = ET.SubElement(cac_AdditionalDocumentReference, "cbc:UUID")
                cbc_UUID_1.text = str(get_ICV_code(invoice_number))
                return invoice  
            except Exception as e:
                    print(str(e))
