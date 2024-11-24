import frappe
import re
import xml.etree.ElementTree as ET
from .qrcode import generate_qr_code_base_64
from .get_invoice_hash import get_latest_sales_invoice_with_hash

def get_ICV_code(invoice_number):
                try:
                    icv_code =  re.sub(r'\D', '', invoice_number)   # taking the number part only from doc name
                    return icv_code
                except Exception as e:
                    frappe.throw("error in getting icv number:  "+ str(e) )




def get_icv_code(sales_invoice_doc):
    data = frappe.get_all('CSR Settings', fields=['name','icv_invoice','icv_credit_note','icv_debit_note'],filters={'company_name': sales_invoice_doc.company })
    if sales_invoice_doc.is_debit_note:
        icv = data[0]['icv_debit_note'] + 1
        value = {
            'icv_debit_note': icv
        }

    elif sales_invoice_doc.is_return:
        icv = data[0]['icv_credit_note'] + 1
        value = {
            'icv_credit_note': icv
        }
    else:
        icv = data[0]['icv_invoice'] + 1
        value = {
            'icv_invoice': icv
        }
    update_icv(data[0]['name'],value)
    return icv


def update_icv(name,value):

    frappe.db.set_value(
        'CSR Settings',
            name,  # Record name
            value
        )
    frappe.db.commit()

        

def billing_reference_for_credit_and_debit_note(invoice,sales_invoice_doc):
            try:
                #details of original invoice
                cac_BillingReference = ET.SubElement(invoice, "cac:BillingReference")
                cac_InvoiceDocumentReference = ET.SubElement(cac_BillingReference, "cac:InvoiceDocumentReference")
                cbc_ID13 = ET.SubElement(cac_InvoiceDocumentReference, "cbc:ID")
                cbc_ID13.text = sales_invoice_doc.return_against  # field from return against invoice. 
                
                return invoice
            except Exception as e:
                    frappe.throw("credit and debit note billing failed"+ str(e) )

def doc_Reference(invoice,sales_invoice_doc,invoice_number):
            try:
                cbc_DocumentCurrencyCode = ET.SubElement(invoice, "cbc:DocumentCurrencyCode")
                cbc_DocumentCurrencyCode.text = sales_invoice_doc.currency
                cbc_TaxCurrencyCode = ET.SubElement(invoice, "cbc:TaxCurrencyCode")
                cbc_TaxCurrencyCode.text = "SAR"  # SAR is as zatca requires tax amount in SAR

                if sales_invoice_doc.is_debit_note == 1 or sales_invoice_doc.is_return == 1:
                                invoice=billing_reference_for_credit_and_debit_note(invoice,sales_invoice_doc)
                cac_AdditionalDocumentReference = ET.SubElement(invoice, "cac:AdditionalDocumentReference")
                cbc_ID_1 = ET.SubElement(cac_AdditionalDocumentReference, "cbc:ID")
                cbc_ID_1.text = "ICV"
                cbc_UUID_1 = ET.SubElement(cac_AdditionalDocumentReference, "cbc:UUID")
                icv = str(get_icv_code(sales_invoice_doc))
                cbc_UUID_1.text = icv
                return invoice ,icv
            except Exception as e:
                    frappe.throw("Error occured in  reference doc" + str(e) )


def get_pih_for_company(pih_data, company_name):
                
                try:
                    for entry in pih_data.get("data", []):
                        if entry.get("company") == company_name:
                            return entry.get("pih")
                    frappe.throw("Error while retrieving  PIH of company for production:  " + str(e) )
                except Exception as e:
                        frappe.throw("Error in getting PIH of company for production:  " + str(e) )


def additional_Reference(invoice,customer_doc,invoice_number):
            try:
                # settings = frappe.get_doc('Zatca ERPgulf Setting')
                cac_AdditionalDocumentReference2 = ET.SubElement(invoice, "cac:AdditionalDocumentReference")
                cbc_ID_1_1 = ET.SubElement(cac_AdditionalDocumentReference2, "cbc:ID")
                cbc_ID_1_1.text = "PIH"
                cac_Attachment = ET.SubElement(cac_AdditionalDocumentReference2, "cac:Attachment")
                cbc_EmbeddedDocumentBinaryObject = ET.SubElement(cac_Attachment, "cbc:EmbeddedDocumentBinaryObject")
                cbc_EmbeddedDocumentBinaryObject.set("mimeCode", "text/plain")
                
                
                # company = settings.company # TODO
                # company = "mycompany"

                # company_name = frappe.db.get_value("Company", company, "abbr")
                # pih_data_raw = settings.get("pih", "{}")
                # pih_data_raw = settings.get("pih", "{}") # TODO

                # company = settings.company

                # pih_data = json.loads(pih_data_raw)

                # pih = get_pih_for_company(pih_data, company_name)
                
                # cbc_EmbeddedDocumentBinaryObject.text = pih
                pih = get_latest_sales_invoice_with_hash()
                cbc_EmbeddedDocumentBinaryObject.text = pih

                # cbc_EmbeddedDocumentBinaryObject.text = "L0Awl814W4ycuFvjDVL/vIW08mNRNAwqfdlF5i/3dpU="
            # QR CODE ------------------------------------------------------------------------------------------------------------------------------------------------------------------
                cac_AdditionalDocumentReference22 = ET.SubElement(invoice, "cac:AdditionalDocumentReference")
                cbc_ID_1_12 = ET.SubElement(cac_AdditionalDocumentReference22, "cbc:ID")
                cbc_ID_1_12.text = "QR"
                cac_Attachment22 = ET.SubElement(cac_AdditionalDocumentReference22, "cac:Attachment")
                cbc_EmbeddedDocumentBinaryObject22 = ET.SubElement(cac_Attachment22, "cbc:EmbeddedDocumentBinaryObject")
                cbc_EmbeddedDocumentBinaryObject22.set("mimeCode", "text/plain")

                if customer_doc.custom_b2c == 1:
                    cbc_EmbeddedDocumentBinaryObject22.text = generate_qr_code_base_64(invoice_number=invoice_number)
                else:
                    cbc_EmbeddedDocumentBinaryObject22.text = "GsiuvGjvchjbFhibcDhjv1886G"
            #END  QR CODE ------------------------------------------------------------------------------------------------------------------------------------------------------------------
                cac_sign = ET.SubElement(invoice, "cac:Signature")
                cbc_id_sign = ET.SubElement(cac_sign, "cbc:ID")
                cbc_method_sign = ET.SubElement(cac_sign, "cbc:SignatureMethod")
                cbc_id_sign.text = "urn:oasis:names:specification:ubl:signature:Invoice"
                cbc_method_sign.text = "urn:oasis:names:specification:ubl:dsig:enveloped:xades"
                return invoice
            except Exception as e:
                    frappe.throw("error occured in additional refrences" + str(e) )