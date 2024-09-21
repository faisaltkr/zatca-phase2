from lxml import etree
import xml.dom.minidom
import xml.etree.ElementTree as ET
import frappe
import json
import os
from ..einvoices.utils import (
     canonicalize_xml,getInvoiceHash,digital_signature,extract_certificate_details,
     certificate_hash,signxml_modify,generate_Signed_Properties_Hash,populate_The_UBL_Extensions_Output,
     generate_tlv_xml,get_tlv_for_value,update_Qr_toXml,structuring_signedxml
)
import base64
import lxml.etree as MyTree
from .complianceapi import compliance_api_call

basepath =  frappe.get_app_path('zatca_sa_phase2', 'zatca_sa_phase2')

print(basepath,"basepath")

invoice_files = {
    'simplified-credit' : 'simplified-credit.xml',
    'simplified' : 'simplified.xml',
    'standard-credit':'standard-credit.xml',
    'standard': 'standard.xml',
    'standard-debit':'standard-debit.xml',
    'simplified-debit':'simplified-debit.xml'
}

invoice_type_list = ['simplified-credit','simplified','standard-credit','standard']


@frappe.whitelist()
def check_compliance(data):
    data = json.loads(data)
    invoices = {
        "standard":data['standard_invoice'],
        "standard-debit": data['standard_debit_note'],
        "standard-credit": data['standard_credit_note'],
        "simplified": data['simplified_invoice'],
        "simplified-debit":data['simplified_debit_note'],
        "simplified-credit":data['simplified_credit_note']
    }
    try:
        customer = data['select_customer']
    except Exception as e:
        frappe.throw("Please select a customer")

    check_invoice(invoices,customer)

def getuuid(xml_data):
    root = etree.fromstring(xml_data)
    namespaces = {
        'ubl': 'urn:oasis:names:specification:ubl:schema:xsd:Invoice-2',
        'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2',
        'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2',
        'ext': 'urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2',
        'sig': 'urn:oasis:names:specification:ubl:schema:xsd:CommonSignatureComponents-2',
        'sac': 'urn:oasis:names:specification:ubl:schema:xsd:SignatureAggregateComponents-2',
        'ds': 'http://www.w3.org/2000/09/xmldsig#'
    }
    uuid_element = root.find('.//cbc:UUID', namespaces=namespaces)

    # Get the UUID value if the element exists
    if uuid_element is not None:
        invoice_uuid = uuid_element.text
        print(f"Invoice UUID: {invoice_uuid}")
    else:
        frappe.throw("uuid not found")

    return uuid_element

def check_invoice(invoices,customer):
    for key, value in invoices.items():
        if value:
            xml_file_path= f'{basepath}/doctype/compliance/invoices/{invoice_files[key]}'
            # print(xml_file_path)
            try:
                customer_doc = frappe.get_doc("Customer",customer)

                with open(xml_file_path, 'r') as file:
                    file_content = file.read()
                uuid1 = getuuid(file_content)
                # print(file_content)
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
                qrCodeB64 = base64.b64encode(qrCodeBuf).decode('utf-8')
                update_Qr_toXml(qrCodeB64)
                signed_xmlfile_name=structuring_signedxml()
                print(signed_xmlfile_name)
                print(encoded_hash,"hash")
                print(signed_xmlfile_name)
                compliance_api_call(uuid1, encoded_hash, signed_xmlfile_name)
                            # generate_xml_hash()
            #     xml_tree = etree.parse(xml_file_path)
            #     # print(xml_tree)
            #     dom = xml.dom.minidom.parse(xml_file_path)
            #     pretty_xml_as_string = dom.toprettyxml()
            #     print(pretty_xml_as_string)
                
                # root = ET.fromstring(pretty_xml_as_string)
                # child_to_remove = root.find('cac:AccountingCustomerParty')

                # if child_to_remove is not None:
                #     root.remove(child_to_remove)

                # # Convert back to string to see the result
                # updated_xml = ET.tostring(root, encoding='unicode')

                # print(updated_xml)
            except Exception as e:
                 print(str(e))
                


import xml.etree.ElementTree as ET
import frappe

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

def customer_Data(invoice,sales_invoice_doc):
            try:
                customer_doc= frappe.get_doc("Customer",sales_invoice_doc.customer)
                cac_AccountingCustomerParty = ET.SubElement(invoice, "cac:AccountingCustomerParty")

                # print(customer_doc.custom_b2c,compliance_type,'3')
                if not customer_doc.custom_b2c:
                    customer_doc= frappe.get_doc("Customer",sales_invoice_doc.customer)
                    cac_Party_2 = ET.SubElement(cac_AccountingCustomerParty, "cac:Party")
                    # cac_PartyIdentification_1 = ET.SubElement(cac_Party_2, "cac:PartyIdentification")
                    # cbc_ID_4 = ET.SubElement(cac_PartyIdentification_1, "cbc:ID")
                    # cbc_ID_4.set("schemeID", "CRN")
                    # cbc_ID_4.text = customer_doc.tax_id
                    if int(frappe.__version__.split('.')[0]) == 13:
                        address = frappe.get_doc("Address", sales_invoice_doc.customer_address)    
                    else:
                        address = frappe.get_doc("Address", customer_doc.customer_primary_address)
                    cac_PostalAddress_1 = ET.SubElement(cac_Party_2, "cac:PostalAddress")
                    cbc_StreetName_1 = ET.SubElement(cac_PostalAddress_1, "cbc:StreetName")
                    cbc_StreetName_1.text = address.address_line1
                    cbc_BuildingNumber_1 = ET.SubElement(cac_PostalAddress_1, "cbc:BuildingNumber")
                    cbc_BuildingNumber_1.text =  address.address_line2
                    cbc_PlotIdentification_1 = ET.SubElement(cac_PostalAddress_1, "cbc:PlotIdentification")
                    if hasattr(address, 'po_box'):
                        cbc_PlotIdentification_1.text = address.po_box
                    else:
                        cbc_PlotIdentification_1.text = address.address_line1
                    cbc_CitySubdivisionName_1 = ET.SubElement(cac_PostalAddress_1, "cbc:CitySubdivisionName")
                    cbc_CitySubdivisionName_1.text = address.address_line2
                    cbc_CityName_1 = ET.SubElement(cac_PostalAddress_1, "cbc:CityName")
                    cbc_CityName_1.text = address.city
                    cbc_PostalZone_1 = ET.SubElement(cac_PostalAddress_1, "cbc:PostalZone")
                    cbc_PostalZone_1.text =address.pincode
                    cbc_CountrySubentity_1 = ET.SubElement(cac_PostalAddress_1, "cbc:CountrySubentity")
                    cbc_CountrySubentity_1.text = address.state
                    cac_Country_1 = ET.SubElement(cac_PostalAddress_1, "cac:Country")
                    cbc_IdentificationCode_1 = ET.SubElement(cac_Country_1, "cbc:IdentificationCode")
                    cbc_IdentificationCode_1.text = "SA" 
                    cac_PartyTaxScheme_1 = ET.SubElement(cac_Party_2, "cac:PartyTaxScheme")
                    cbc_company_id =  ET.SubElement(cac_PartyTaxScheme_1,"cbc:CompanyID")
                    cbc_company_id.text = customer_doc.tax_id
                    cac_TaxScheme_1 = ET.SubElement(cac_PartyTaxScheme_1, "cac:TaxScheme")

                    cbc_ID_5 = ET.SubElement(cac_TaxScheme_1, "cbc:ID")
                    cbc_ID_5.text = "VAT"
                    cac_PartyLegalEntity_1 = ET.SubElement(cac_Party_2, "cac:PartyLegalEntity")
                    cbc_RegistrationName_1 = ET.SubElement(cac_PartyLegalEntity_1, "cbc:RegistrationName")
                    cbc_RegistrationName_1.text = sales_invoice_doc.customer
                return invoice
            except Exception as e:
                    frappe.throw("error occured in customer data"+ str(e) )