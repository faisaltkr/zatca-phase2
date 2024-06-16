import xml.etree.ElementTree as ET
import frappe


def customer_Data(invoice,sales_invoice_doc):
            try:
                # customer_doc= frappe.get_doc("Customer",sales_invoice_doc.customer)
                cac_AccountingCustomerParty = ET.SubElement(invoice, "cac:AccountingCustomerParty")
                cac_Party_2 = ET.SubElement(cac_AccountingCustomerParty, "cac:Party")
                cac_PartyIdentification_1 = ET.SubElement(cac_Party_2, "cac:PartyIdentification")
                cbc_ID_4 = ET.SubElement(cac_PartyIdentification_1, "cbc:ID")
                cbc_ID_4.set("schemeID", "CRN")
                cbc_ID_4.text = "sdfddfddf"
                # if int(frappe.__version__.split('.')[0]) == 13:
                #     address = frappe.get_doc("Address", sales_invoice_doc.customer_address)    
                # else:
                #     address = frappe.get_doc("Address", customer_doc.customer_primary_address)
                cac_PostalAddress_1 = ET.SubElement(cac_Party_2, "cac:PostalAddress")
                cbc_StreetName_1 = ET.SubElement(cac_PostalAddress_1, "cbc:StreetName")
                cbc_StreetName_1.text = "sdfdf"
                cbc_BuildingNumber_1 = ET.SubElement(cac_PostalAddress_1, "cbc:BuildingNumber")
                cbc_BuildingNumber_1.text = "sdsdf"
                cbc_PlotIdentification_1 = ET.SubElement(cac_PostalAddress_1, "cbc:PlotIdentification")
                # if hasattr(address, 'po_box'):
                # cbc_PlotIdentification_1.text = address.po_box
                # else:
                cbc_PlotIdentification_1.text = "dsdf"
                cbc_CitySubdivisionName_1 = ET.SubElement(cac_PostalAddress_1, "cbc:CitySubdivisionName")
                cbc_CitySubdivisionName_1.text = "sdfsdf"
                cbc_CityName_1 = ET.SubElement(cac_PostalAddress_1, "cbc:CityName")
                cbc_CityName_1.text = "sdfsdf"
                cbc_PostalZone_1 = ET.SubElement(cac_PostalAddress_1, "cbc:PostalZone")
                cbc_PostalZone_1.text = "23243"
                cbc_CountrySubentity_1 = ET.SubElement(cac_PostalAddress_1, "cbc:CountrySubentity")
                cbc_CountrySubentity_1.text = "sdfsdf"
                cac_Country_1 = ET.SubElement(cac_PostalAddress_1, "cac:Country")
                cbc_IdentificationCode_1 = ET.SubElement(cac_Country_1, "cbc:IdentificationCode")
                cbc_IdentificationCode_1.text = "SA" 
                cac_PartyTaxScheme_1 = ET.SubElement(cac_Party_2, "cac:PartyTaxScheme")
                cac_TaxScheme_1 = ET.SubElement(cac_PartyTaxScheme_1, "cac:TaxScheme")
                cbc_ID_5 = ET.SubElement(cac_TaxScheme_1, "cbc:ID")
                cbc_ID_5.text = "VAT"
                cac_PartyLegalEntity_1 = ET.SubElement(cac_Party_2, "cac:PartyLegalEntity")
                cbc_RegistrationName_1 = ET.SubElement(cac_PartyLegalEntity_1, "cbc:RegistrationName")
                cbc_RegistrationName_1.text = "sdfsdf"
                return invoice
            except Exception as e:
                    frappe.throw("error occured in customer data"+ str(e) )