import xml.etree.ElementTree as ET
import uuid
import frappe
from frappe.utils.data import  get_time
               

# <cac:AllowanceCharge>
#  <cbc:ChargeIndicator>false/true</cbc:ChargeIndicator>
#  <cbc:AllowanceChargeReasonCode>95/CG</cbc:AllowanceChargeReasonCode>
#  <cbc:AllowanceChargeReason>Discount/Cleaning</cbc:AllowanceChargeReason>
# <cbc:MultiplierFactorNumeric>10</cbc:MultiplierFactorNumeric> (2)
#  <cbc:Amount currencyID="SAR">200</cbc:Amount> (3)
#  <cbc:BaseAmount currencyID="SAR">2000</cbc:BaseAmount> (1)
#  <cac:TaxCategory>
#  <cbc:ID>S</cbc:ID>
#  <cbc:Percent>15</cbc:Percent>
#  <cac:TaxScheme>
#  <cbc:ID>VAT</cbc:ID>
#  </cac:TaxScheme>
#  </cac:TaxCategory>
# </cac:AllowanceCharge>


def discount_and_charge(invoice,p_invoice_doc):
            try:
                
                charges =  p_invoice_doc.as_dict()['taxes']
                if len(charges) >  1:
                    for charges in charges:
                        print(charges)
                        if charges['custom_is_charge'] != 'tax':
                            cac_allowance = ET.SubElement(invoice, "cac:AllowanceCharge")
                            cbc_chargeindicator =  ET.SubElement(cac_allowance,"cbc:ChargeIndicator")
                            cbc_chargeindicator.text =  'true'
                            cbc_allowance_charge_reason_code = ET.SubElement(cac_allowance,"cbc:AllowanceChargeReasonCode")
                            cbc_allowance_charge_reason_code.text = '95'
                            cbc_allowance_charge_reason = ET.SubElement(cac_allowance,"cbc:AllowanceChargeReason")
                            cbc_allowance_charge_reason.text = charges['description']
                            cbc_multifactor_numeric = ET.SubElement(cac_allowance,"cbc:MultiplierFactorNumeric")
                            cbc_multifactor_numeric.text = '10'
                            cbc_amount =  ET.SubElement(cac_allowance,"cbc:Amount")
                            cbc_amount.text = str(charges['tax_amount'])
                            cbc_amount.set("currencyID", "SAR")
                            cbc_base_amount = ET.SubElement(cac_allowance,"cbc:BaseAmount")                
                            cbc_base_amount.set("currencyID", "SAR")
                            cbc_base_amount.text = str(charges['base_total'])
                            cac_tax_category = ET.SubElement(cac_allowance,"cac:TaxCategory")
                            cbc_id =  ET.SubElement(cac_tax_category,"cbc:ID")
                            cbc_id.text = 'S'
                            cbc_percent = ET.SubElement(cac_tax_category,"cbc:Percent")
                            cbc_percent.text = '15'
                            cac_tax_scheme = ET.SubElement(cac_tax_category,"cac:TaxScheme")
                            cbc_id = ET.SubElement(cac_tax_scheme,"cbc:ID")
                            cbc_id.text = 'VAT'

                if p_invoice_doc.as_dict()['discount_amount']:
                    sdict = p_invoice_doc.as_dict()
                    get_code = sdict['additional_discount_account']
                    total_amount = sdict['total']
                    additional_discount_percentage = sdict['additional_discount_percentage']
                    discount_amount = sdict['discount_amount']
                    discount_percent = get_discount_percentage(total_amount,discount_amount,additional_discount_percentage)
                    discount_code =  get_discount_code(code=get_code)
                    print(discount_amount,"gjghjghjghjkj")
                    print(additional_discount_percentage,"fhfhfghfghfgh")
                    cac_allowance = ET.SubElement(invoice, "cac:AllowanceCharge")
                    cbc_chargeindicator =  ET.SubElement(cac_allowance,"cbc:ChargeIndicator")
                    cbc_chargeindicator.text =  'false'
                    cbc_allowance_charge_reason_code = ET.SubElement(cac_allowance,"cbc:AllowanceChargeReasonCode")
                    cbc_allowance_charge_reason_code.text = str(discount_code['custom_code'])
                    cbc_allowance_charge_reason = ET.SubElement(cac_allowance,"cbc:AllowanceChargeReason")
                    cbc_allowance_charge_reason.text = 'discount'
                    cbc_multifactor_numeric = ET.SubElement(cac_allowance,"cbc:MultiplierFactorNumeric")
                    cbc_multifactor_numeric.text = str(round(discount_percent,2))
                    cbc_amount =  ET.SubElement(cac_allowance,"cbc:Amount")
                    cbc_amount.text = str(round(discount_amount,2))
                    cbc_amount.set("currencyID", "SAR")
                    cbc_base_amount = ET.SubElement(cac_allowance,"cbc:BaseAmount")                
                    cbc_base_amount.set("currencyID", "SAR")
                    cbc_base_amount.text = str(round(p_invoice_doc.total-discount_amount,2))
                    cac_tax_category = ET.SubElement(cac_allowance,"cac:TaxCategory")
                    cbc_id =  ET.SubElement(cac_tax_category,"cbc:ID")
                    cbc_id.text = 'S'
                    cbc_percent = ET.SubElement(cac_tax_category,"cbc:Percent")
                    cbc_percent.text = str(round(discount_code['tax_rate'],2))
                    cac_tax_scheme = ET.SubElement(cac_tax_category,"cac:TaxScheme")
                    cbc_id = ET.SubElement(cac_tax_scheme,"cbc:ID")
                    cbc_id.text = 'VAT'
                      
                return invoice
            except Exception as e:
                    frappe.throw("error occured in discount data"+ str(e) )



def get_discount_code(code):
    try:
        # Fetch the document using doctype and name
        doc = frappe.get_doc("Account", code)
        
        # Convert the document to a dictionary to get its values
        doc_values = doc.as_dict()
        
        return doc_values
    except frappe.DoesNotExistError:
        print(f"Document of type  with name  does not exist.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def get_discount_percentage(total_amount,discount,discount_percentage=0):
     if discount_percentage:
          return round(discount_percentage,2)
     else:
          return round((discount*100)/total_amount,2)
          
          