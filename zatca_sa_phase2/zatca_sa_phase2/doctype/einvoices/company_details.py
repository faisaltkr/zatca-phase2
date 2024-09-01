import xml.etree.ElementTree as ET
import frappe
from zatca_sa_phase2.zatca_sa_phase2.doctype.csr_settings.utils.get_values import get_zatca_settings

def company_Data(invoice,sales_invoice_doc):
            try:
                # company_doc = frappe.get_doc("Company", sales_invoice_doc.company)

                # customer_doc= frappe.get_doc("Customer",sales_invoice_doc.customer)
                cac_AccountingSupplierParty = ET.SubElement(invoice, "cac:AccountingSupplierParty")
                cac_Party_1 = ET.SubElement(cac_AccountingSupplierParty, "cac:Party")
                cac_PartyIdentification = ET.SubElement(cac_Party_1, "cac:PartyIdentification")
                company_details = get_zatca_settings()
                scheme = company_details['additional_id'][-4:-1:1]
                scheme_value = company_details['value_number']
                cbc_ID_2 = ET.SubElement(cac_PartyIdentification, "cbc:ID")
                cbc_ID_2.set("schemeID", scheme)
                # doc = frappe.get_all('Additional IDs-Zatca',fields = ['id_name','type_code','valueid_number',])
                # datas = [{'id_name': 'MISA LICENCE', 'type_code': 'SAG', 'valueid_number': None}, {'id_name': 'MHRSD LICENCE', 'type_code': 'MLS', 'valueid_number': None}, {'id_name': 'MOMRAH LICENCE', 'type_code': 'MOM', 'valueid_number': None}, {'id_name': 'OTHER ID', 'type_code': 'OTH', 'valueid_number': None}, {'id_name': 'Commercial Registration Number', 'type_code': 'CRN', 'valueid_number': 'sssss'}, {'id_name': 'Seven Hundred Number', 'type_code': '700', 'valueid_number': None}]
                
                # for datas in doc:
                #     if datas['type_code'] == 'CRN':
                #         crn = datas['valueid_number']
                        
                # cbc_ID_2.text =company_doc.tax_id   # COmpany CR - Need to have a field in company doctype called company_registration 
                
                cbc_ID_2.text = scheme_value  # COmpany CR - Need to have a field in company doctype called company_registration 

                # address_list = frappe.get_list("Address", filters={"is_your_company_address": "1"}, fields=["address_line1", "address_line2","city","pincode","state"])
                # if len(address_list) == 0:
                #     frappe.throw("Zatca requires proper address. Please add your company address in address master")
                # for address in address_list:
                cac_PostalAddress = ET.SubElement(cac_Party_1, "cac:PostalAddress")
                cbc_StreetName = ET.SubElement(cac_PostalAddress, "cbc:StreetName")
                cbc_StreetName.text = company_details['street']
                cbc_BuildingNumber = ET.SubElement(cac_PostalAddress, "cbc:BuildingNumber")
                cbc_BuildingNumber.text = company_details['building_number']
                # cbc_PlotIdentification = ET.SubElement(cac_PostalAddress, "cbc:PlotIdentification")
                # cbc_PlotIdentification.text =  ''
                cbc_CitySubdivisionName = ET.SubElement(cac_PostalAddress, "cbc:CitySubdivisionName")
                cbc_CitySubdivisionName.text = company_details['district']
                cbc_CityName = ET.SubElement(cac_PostalAddress, "cbc:CityName")
                cbc_CityName.text = company_details['city']
                cbc_PostalZone = ET.SubElement(cac_PostalAddress, "cbc:PostalZone")
                cbc_PostalZone.text = company_details['postal_code']
                # cbc_CountrySubentity = ET.SubElement(cac_PostalAddress, "cbc:CountrySubentity")
                # cbc_CountrySubentity.text = ''
                    # break
                cac_Country = ET.SubElement(cac_PostalAddress, "cac:Country")
                cbc_IdentificationCode = ET.SubElement(cac_Country, "cbc:IdentificationCode")
                cbc_IdentificationCode.text = "SA"
                cac_PartyTaxScheme = ET.SubElement(cac_Party_1, "cac:PartyTaxScheme")
                cbc_CompanyID = ET.SubElement(cac_PartyTaxScheme, "cbc:CompanyID")
                cbc_CompanyID.text = company_details['vat_registration_number']
                cac_TaxScheme = ET.SubElement(cac_PartyTaxScheme, "cac:TaxScheme")
                cbc_ID_3 = ET.SubElement(cac_TaxScheme, "cbc:ID")
                cbc_ID_3.text = "VAT"
                cac_PartyLegalEntity = ET.SubElement(cac_Party_1, "cac:PartyLegalEntity")
                cbc_RegistrationName = ET.SubElement(cac_PartyLegalEntity, "cbc:RegistrationName")
                cbc_RegistrationName.text = company_details['company_name']
                return invoice
            except Exception as e:
                    frappe.throw("error occured in company data"+ str(e) )