"""
class to create invoice standard and simplified
"""
import xml.etree.ElementTree as ET
# from .xml_tags import generate_xml_tags
from .invoice_detail import salesinvoice_data
from .document_currency import currency_data
from .utils import (
    base_64_hash,
    get_private_path,
    dateformat,
    timeformat,
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
)
from .reporting import reporting_API
from .clearence import clearance_API
from .compliance import compliance_api_call
import base64 
import os
import frappe
from .xml_tags import xml_tags
from .invoice_type import invoice_Typecode_Simplified,invoice_Typecode_Standard,invoice_Typecode_Compliance
from .invoice_doc_ref import doc_Reference,additional_Reference
from .company_details import company_Data
from .customer_details import customer_Data
from .invoice_pay_means import delivery_And_PaymentMeans,delivery_And_PaymentMeans_for_Compliance
from .invoice_tax import tax_Data,tax_Data_with_template
from .invoice_items import item_data, item_data_with_template
from .qrcode import generate_qr_code_base_64
from .discount import discount_and_charge


class SimplifiedInvoice:

    def __init__(self, cih, pih=None) -> None:
        """
        if invoice hash is not present then hash value of zero as pih
        """
        self.pih = pih
        self.cih = cih
        if not pih:
            self.pih = base_64_hash('0')
        

    # def create_simplified_invoice(self):
    #     """
    #     invoice generate for simplified
    #     """
    #     xml_tags = generate_xml_tags()
    #     inv_data = salesinvoice_data(xml_tags)
    #     cur = currency_data(inv_data)
    #     return cur
    
# file name  - vatnumber-datetime-invoicenumber //yyyy-mm-dd-hh-mm-ss //3xxxxxxxxx1xxx3_20210526T132400_2021-05-26-23555.xml
def create_invoice(doc,method):
    csr_details =  get_csr_deatils()
    vat_number =   csr_details.get('vat_registration_number')
    simp =  SimplifiedInvoice(1,pih=123)
    simp_inv = simp.create_simplified_invoice()
    tree = ET.ElementTree(simp_inv)


    #create path to save xmls if not exits
    private_path = get_private_path()
    if not os.path.exists(private_path+'/xmls'):
        os.makedirs(private_path+'/xmls')

    current_date = dateformat()
    current_time = timeformat()

    tree.write(f"{private_path}/xmls/{vat_number}_{current_date}T{current_time}_{doc.name}.xml", encoding="utf-8", xml_declaration=True)
    return True



def get_csr_deatils():
    docs = frappe.get_all('CSR Settings', fields=['name', 'vat_registration_number'])

    try:
        # Get the last added document (most recent) with all fields
        docs = frappe.get_list('CSR Settings', fields='*', order_by='creation desc', limit=1)
        
        # Iterate through the documents and print all field values
        doc_value = {}
        for doc in docs:
            print(f"Document: {doc}")
            doc_value = doc
            break


    except frappe.DoesNotExistError:
        print(f"No documents found for Doctype.")


    return doc_value

###### helper functions
import lxml.etree as MyTree


def removeTags(finalzatcaxml):
                try:
                    xml_file = MyTree.fromstring(finalzatcaxml)
                    xsl_file = MyTree.fromstring('''<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                                    xmlns:xs="http://www.w3.org/2001/XMLSchema"
                                    xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"
                                    xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"
                                    xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"
                                    xmlns:ext="urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2"
                                    exclude-result-prefixes="xs"
                                    version="2.0">
                                    <xsl:output omit-xml-declaration="yes" encoding="utf-8" indent="no"/>
                                    <xsl:template match="node() | @*">
                                        <xsl:copy>
                                            <xsl:apply-templates select="node() | @*"/>
                                        </xsl:copy>
                                    </xsl:template>
                                    <xsl:template match="//*[local-name()='Invoice']//*[local-name()='UBLExtensions']"></xsl:template>
                                    <xsl:template match="//*[local-name()='AdditionalDocumentReference'][cbc:ID[normalize-space(text()) = 'QR']]"></xsl:template>
                                        <xsl:template match="//*[local-name()='Invoice']/*[local-name()='Signature']"></xsl:template>
                                    </xsl:stylesheet>''')
                    transform = MyTree.XSLT(xsl_file.getroottree())
                    transformed_xml = transform(xml_file.getroottree())
                    return transformed_xml
                except Exception as e:
                    frappe.throw(" error in remove tags: "+ str(e) )


# @frappe.whitelist(allow_guest=True) 
def zatca_Call(invoice_number, compliance_type=0, any_item_has_tax_template= False):
                    # generate_qr_code_base_64(invoice_number=invoice_number)
                    print(compliance_type,"comp")
                    # compliance_type = "1"
                    try:    
                            # create_compliance_x509()
                            # frappe.throw("Created compliance x509 certificate")
                            sales_invoice_doc = frappe.get_doc('Sales Invoice' ,invoice_number)
                            if not frappe.db.exists("Sales Invoice", invoice_number):
                                frappe.throw("Invoice Number is NOT Valid:  " + str(invoice_number))
                            print(0)
                            try:
                                customer_doc = frappe.get_doc("Customer",sales_invoice_doc.customer)
                                is_b2c  = customer_doc.custom_b2c
                            except Exception as e:
                                  print(str(e))
                            print(1)
                            invoice= xml_tags(is_b2c=is_b2c)
                            print(2)
                            invoice,uuid1,sales_invoice_doc=salesinvoice_data(invoice,invoice_number)
                            
                            if not compliance_type :
                                    # frappe.throw(str("here 7 " + str(compliance_type))) 
                                    if customer_doc.custom_b2c == 1:
                                        invoice = invoice_Typecode_Simplified(invoice, sales_invoice_doc)
                                    else:
                                        invoice = invoice_Typecode_Standard(invoice, sales_invoice_doc)
                            else:  # if it a compliance test
                                # frappe.throw(str("here 8 " + str(compliance_type))) 
                                invoice = invoice_Typecode_Compliance(invoice, compliance_type)

                            invoice=doc_Reference(invoice,sales_invoice_doc,invoice_number)
                            invoice=additional_Reference(invoice,customer_doc,invoice_number)
                            invoice=company_Data(invoice,sales_invoice_doc)
                            invoice=customer_Data(invoice,sales_invoice_doc)
                            invoice=delivery_And_PaymentMeans(invoice,sales_invoice_doc, sales_invoice_doc.is_return) 
                            invoice=discount_and_charge(invoice,sales_invoice_doc)
                            if not any_item_has_tax_template:
                                invoice = tax_Data(invoice, sales_invoice_doc)
                            else:
                                invoice = tax_Data_with_template(invoice, sales_invoice_doc)
                            if not any_item_has_tax_template:
                                invoice=item_data(invoice,sales_invoice_doc)
                            else:
                                   item_data_with_template(invoice,sales_invoice_doc)
                            pretty_xml_string=xml_structuring(invoice,sales_invoice_doc)

                            with open(frappe.local.site + "/private/files/finalzatcaxml.xml", 'r') as file:
                                    file_content = file.read()
                            tag_removed_xml = removeTags(file_content)
                            canonicalized_xml = canonicalize_xml(tag_removed_xml)
                            hash1, encoded_hash = getInvoiceHash(canonicalized_xml)
                            encoded_signature = digital_signature(hash1)
                            issuer_name,serial_number = extract_certificate_details(customer_doc=customer_doc)
                            encoded_certificate_hash=certificate_hash()
                            namespaces,signing_time=signxml_modify(customer_doc=customer_doc)
                            signed_properties_base64=generate_Signed_Properties_Hash(signing_time,issuer_name,serial_number,encoded_certificate_hash)
                            populate_The_UBL_Extensions_Output(encoded_signature,namespaces,signed_properties_base64,encoded_hash)
                            tlv_data = generate_tlv_xml()
                            # print(tlv_data)
                            tagsBufsArray = []
                            for tag_num, tag_value in tlv_data.items():
                                tagsBufsArray.append(get_tlv_for_value(tag_num, tag_value))
                            qrCodeBuf = b"".join(tagsBufsArray)
                            print(qrCodeBuf)
                            qrCodeB64 = base64.b64encode(qrCodeBuf).decode('utf-8')
                            print(qrCodeB64,"sdfsdfdsfgdfgdfgdfgdfdfgdgdgdgdgdgfdfg")
                            update_Qr_toXml(qrCodeB64)
                            signed_xmlfile_name=structuring_signedxml()
                            
                            # generate_xml_hash()
                            print(compliance_type,"comsdflkjsdlkfjdklfjn",type(compliance_type))
                            if not compliance_type:
                                if customer_doc.custom_b2c == 1:
                                    reporting_API(uuid1, encoded_hash, signed_xmlfile_name,invoice_number,sales_invoice_doc)
                                    attach_QR_Image(qrCodeB64,sales_invoice_doc)
                                else:

                                    xml_cleared=clearance_API(uuid1, encoded_hash, signed_xmlfile_name,invoice_number,sales_invoice_doc)
                                    attach_QR_Image(qrCodeB64,sales_invoice_doc)
                            else:  # if it a compliance test
                                # frappe.msgprint("Compliance test")
                                compliance_api_call(uuid1, encoded_hash, signed_xmlfile_name)
                                attach_QR_Image(qrCodeB64,sales_invoice_doc)
                    except:       
                            frappe.log_error(title='Zatca invoice call failed', message=frappe.get_traceback())


@frappe.whitelist(allow_guest=True)          
def zatca_Background_on_submit(doc, method=None):              
# def zatca_Background(invoice_number):
                    # print(doc.custom_zatca_tax_category)
                    print("hiiiiiii")
                    try:
                        sales_invoice_doc = doc
                        invoice_number = sales_invoice_doc.name
                        sales_invoice_doc= frappe.get_doc("Sales Invoice",invoice_number )
                        # settings = frappe.get_doc('Zatca ERPgulf Setting')
                        any_item_has_tax_template = False
        
                        for item in sales_invoice_doc.items:
                            if item.item_tax_template:
                                any_item_has_tax_template = True
                                break
                        
                        if any_item_has_tax_template:
                            for item in sales_invoice_doc.items:
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
                        
                        if not frappe.db.exists("Sales Invoice", invoice_number):
                                frappe.throw("Please save and submit the invoice before sending to Zatca:  " + str(invoice_number))
                                                
                        
            
                        if sales_invoice_doc.docstatus in [0,2]:
                            frappe.throw("Please submit the invoice before sending to Zatca:  " + str(invoice_number))
                            
                        if sales_invoice_doc.custom_zatca_status == "REPORTED" or sales_invoice_doc.custom_zatca_status == "CLEARED":
                            frappe.throw("Already submitted to Zakat and Tax Authority")
                        
                        zatca_Call(invoice_number,0,any_item_has_tax_template)
                        
                    except Exception as e:
                        frappe.throw("Error in background call:  " + str(e) )