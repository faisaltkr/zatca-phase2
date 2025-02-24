import frappe
from zatca_sa_phase2.zatca_sa_phase2.doctype.einvoices.xml_tags import xml_tags
from zatca_sa_phase2.zatca_sa_phase2.doctype.purchase.purchase_invoice_data import purchase_invoice_data
from zatca_sa_phase2.zatca_sa_phase2.doctype.purchase.invoice_type import (
      invoice_Typecode_Simplified,
      invoice_Typecode_Standard,
      invoice_Typecode_Compliance
)
from zatca_sa_phase2.zatca_sa_phase2.doctype.purchase.purchase_pay_means import delivery_And_PaymentMeans
from zatca_sa_phase2.zatca_sa_phase2.doctype.purchase.purchase_doc_ref import doc_Reference,additional_Reference
from zatca_sa_phase2.zatca_sa_phase2.doctype.purchase.company import company_Data
from zatca_sa_phase2.zatca_sa_phase2.doctype.purchase.purchase_customer import customer_Data
from zatca_sa_phase2.zatca_sa_phase2.doctype.purchase.discount import discount_and_charge
from zatca_sa_phase2.zatca_sa_phase2.doctype.purchase.purchase_tax import tax_Data,tax_Data_with_template
from zatca_sa_phase2.zatca_sa_phase2.doctype.purchase.purchase_items import item_data,item_data_with_template
from zatca_sa_phase2.zatca_sa_phase2.doctype.purchase.utils import (
    xml_structuring,
    canonicalize_xml,
    getInvoiceHash,
    digital_signature,
    extract_certificate_details,
    certificate_hash,
    signxml_modify,
    generate_Signed_Properties_Hash,
    populate_The_UBL_Extensions_Output,
    generate_tlv_xml,
    get_tlv_for_value,
    update_Qr_toXml,
    structuring_signedxml,
    attach_QR_Image,
    removeTags
)
from zatca_sa_phase2.zatca_sa_phase2.doctype.purchase.reporting import reporting_API
from zatca_sa_phase2.zatca_sa_phase2.doctype.purchase.clearence import clearance_API
from zatca_sa_phase2.zatca_sa_phase2.doctype.purchase.compliance import compliance_api_call

import base64

def zatca_Call(invoice_number, compliance_type="0", any_item_has_tax_template= False):
                    # generate_qr_code_base_64(invoice_number=invoice_number)
                    
                    # compliance_type = "1" 
                    try:    
                            # create_compliance_x509()
                            # frappe.throw("Created compliance x509 certificate")
                            if not frappe.db.exists("Purchase Invoice", invoice_number):
                                frappe.throw("Invoice Number is NOT Valid:  " + str(invoice_number))
                            p_invoice_doc = frappe.get_doc('Purchase Invoice' ,invoice_number)
                            print("dfgfhfghf","vvvvvvv")
                            supplier_doc = frappe.get_doc("Supplier",p_invoice_doc.supplier)
                            is_b2c  = supplier_doc.is_custom_b2c


                            invoice = xml_tags(is_b2c=is_b2c)
                            # invoice= xml_tags()
                            invoice,uuid1 = purchase_invoice_data(invoice,invoice_number,p_invoice_doc)

                            if compliance_type == "0":
                                    # frappe.throw(str("here 7 " + str(compliance_type))) 
                                    if supplier_doc.is_custom_b2c == 1:
                                        invoice = invoice_Typecode_Simplified(invoice, p_invoice_doc)
                                    else:
                                        invoice = invoice_Typecode_Standard(invoice, p_invoice_doc)
                            else:  # if it a compliance test
                                # frappe.throw(str("here 8 " + str(compliance_type))) 
                                invoice = invoice_Typecode_Compliance(invoice, compliance_type)

                            invoice, icv=doc_Reference(invoice,p_invoice_doc,invoice_number)
                            invoice =additional_Reference(invoice,supplier_doc,invoice_number)
                            invoice=company_Data(invoice,p_invoice_doc)
                            invoice=customer_Data(invoice,p_invoice_doc)
                            invoice=delivery_And_PaymentMeans(invoice,p_invoice_doc, p_invoice_doc.is_return) 
                            invoice=discount_and_charge(invoice,p_invoice_doc)

                            if not any_item_has_tax_template:
                                invoice = tax_Data(invoice, p_invoice_doc)
                            else:
                                invoice = tax_Data_with_template(invoice, p_invoice_doc)
                            if not any_item_has_tax_template:
                                invoice=item_data(invoice,p_invoice_doc)
                            else:
                                   item_data_with_template(invoice,p_invoice_doc)
                            print(1)
                            pretty_xml_string=xml_structuring(invoice,p_invoice_doc)
                            print(p_invoice_doc.name)
                            with open(frappe.local.site + "/private/files/finalzatcaxml_{p_invoice_doc.name}.xml", 'r') as file:
                                    file_content = file.read()
                            print(3)
                            tag_removed_xml = removeTags(file_content)
                            canonicalized_xml = canonicalize_xml(tag_removed_xml)
                            hash1, encoded_hash = getInvoiceHash(canonicalized_xml)
                            encoded_signature = digital_signature(hash1,p_invoice_doc)
                            issuer_name,serial_number = extract_certificate_details(customer_doc=supplier_doc,p_invoice_doc=p_invoice_doc)
                            encoded_certificate_hash=certificate_hash(p_invoice_doc)
                            namespaces,signing_time=signxml_modify(customer_doc=supplier_doc,p_invoice_doc=p_invoice_doc)
                            signed_properties_base64=generate_Signed_Properties_Hash(signing_time,issuer_name,serial_number,encoded_certificate_hash)
                            populate_The_UBL_Extensions_Output(encoded_signature,namespaces,signed_properties_base64,encoded_hash,p_invoice_doc)
                            tlv_data = generate_tlv_xml(p_invoice_doc=p_invoice_doc)
                            # print(tlv_data)

                            tagsBufsArray = []
                            for tag_num, tag_value in tlv_data.items():
                                tagsBufsArray.append(get_tlv_for_value(tag_num, tag_value))
                            qrCodeBuf = b"".join(tagsBufsArray)
                            qrCodeB64 = base64.b64encode(qrCodeBuf).decode('utf-8')
                            update_Qr_toXml(qrCodeB64)
                            signed_xmlfile_name=structuring_signedxml(p_invoice_doc)
                            # generate_xml_hash()
                            if compliance_type == "0":
                                if supplier_doc.is_custom_b2c == 1:
                                    reporting_API(uuid1, encoded_hash, signed_xmlfile_name,invoice_number,p_invoice_doc)
                                    attach_QR_Image(qrCodeB64,p_invoice_doc)
                                else:
                                    xml_cleared=clearance_API(uuid1, encoded_hash, signed_xmlfile_name,invoice_number,p_invoice_doc)
                                    attach_QR_Image(qrCodeB64,p_invoice_doc)
                            else:  # if it a compliance test
                                # frappe.msgprint("Compliance test")
                                compliance_api_call(uuid1, encoded_hash, signed_xmlfile_name,p_invoice_doc)
                                attach_QR_Image(qrCodeB64,p_invoice_doc)
                    except Exception as e:       
                            frappe.throw("Error in background call:  " + str(e) )

@frappe.whitelist(allow_guest=True)          
def on_submit_new(doc, method=None):       
 #def zatca_Background(invoice_number):
                    print("dfkjdskjldjflkd============")
                    try:
                        purchase_invoice_doc = doc
                        if doc.is_return:
                            invoice_number = purchase_invoice_doc.name
                            p_invoice_doc= frappe.get_doc("Purchase Invoice",invoice_number )
                            # settings = frappe.get_doc('Zatca ERPgulf Setting')
                            any_item_has_tax_template = False
                            for item in purchase_invoice_doc.items:
                                if item.item_tax_template:
                                    any_item_has_tax_template = True
                                    break
                            if any_item_has_tax_template:
                                for item in purchase_invoice_doc.items:
                                    if not item.item_tax_template:
                                        frappe.throw("If any one item has an Item Tax Template, all items must have an Item Tax Template.")
                            # for item in sales_invoice_doc.items:
                            #     if item.item_tax_template:
                            #         item_tax_template = frappe.get_doc('Item Tax Template', item.item_tax_template)

                            #         zatca_tax_category = item_tax_template.custom_zatca_tax_category
                            #         for tax in item_tax_template.taxes:
                            #             tax_rate = float(tax.tax_rate)
                                        
                            #             if f"{tax_rate:.2f}" not in ['5.00', '15.00'] and zatca_tax_category not in ["Zero Rated", "Exempted", "Services outside scope of tax / Not subject to VAT"]:
                            #                 frappe.throw("Zatca tax category should be 'Zero Rated', 'Exempted' or 'Services outside scope of tax / Not subject to VAT' for items with tax rate not equal to 5.00 or 15.00.")
                                        
                            #             if f"{tax_rate:.2f}" == '15.00' and zatca_tax_category != "Standard":
                            #                 frappe.throw("Check the Zatca category code and enable it as standard.")

                            # if settings.zatca_invoice_enabled != 1:
                            #     frappe.throw("Zatca Invoice is not enabled in Zatca Settings, Please contact your system administrator")
                            if not frappe.db.exists("Purchase Invoice", invoice_number):
                                    frappe.throw("Please save and submit the invoice before sending to Zatca:  " + str(invoice_number))
                                                    
                            
                            if p_invoice_doc.docstatus in [0,2]:
                                frappe.throw("Please submit the invoice before sending to Zatca:  " + str(invoice_number))
                                

                            # TODO status to be added
                            if purchase_invoice_doc.custom_zatca_status == "REPORTED" or purchase_invoice_doc.custom_zatca_status == "CLEARED":
                                frappe.throw("Already submitted to Zakat and Tax Authority")
                            zatca_Call(invoice_number,"0",any_item_has_tax_template)
                        
                    except Exception as e:
                        frappe.throw("Error in background call:  " + str(e) )