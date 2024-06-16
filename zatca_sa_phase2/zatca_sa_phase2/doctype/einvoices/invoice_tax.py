import frappe
import xml.etree.ElementTree as ET
import json

def get_exemption_reason_map():
    return {
        "VATEX-SA-29": "Financial services mentioned in Article 29 of the VAT Regulations.",
        "VATEX-SA-29-7": "Life insurance services mentioned in Article 29 of the VAT Regulations.",
        "VATEX-SA-30": "Real estate transactions mentioned in Article 30 of the VAT Regulations.",
        "VATEX-SA-32": "Export of goods.",
        "VATEX-SA-33": "Export of services.",
        "VATEX-SA-34-1": "The international transport of Goods.",
        "VATEX-SA-34-2": "International transport of passengers.",
        "VATEX-SA-34-3": "Services directly connected and incidental to a Supply of international passenger transport.",
        "VATEX-SA-34-4": "Supply of a qualifying means of transport.",
        "VATEX-SA-34-5": "Any services relating to Goods or passenger transportation, as defined in article twenty five of these Regulations.",
        "VATEX-SA-35": "Medicines and medical equipment.",
        "VATEX-SA-36": "Qualifying metals.",
        "VATEX-SA-EDU": "Private education to citizen.",
        "VATEX-SA-HEA ": "Private healthcare to citizen.",
        "VATEX-SA-MLTRY": "Supply of qualified military goods",
        "VATEX-SA-OOS": "The reason is a free text, has to be provided by the taxpayer on case to case basis."
    
    }


def get_Tax_for_Item(full_string,item):
            try:                                          # getting tax percentage and tax amount
                data = json.loads(full_string)
                tax_percentage=data.get(item,[0,0])[0]
                tax_amount = data.get(item, [0, 0])[1]
                return tax_amount,tax_percentage
            except Exception as e:
                    frappe.throw("error occured in tax for item"+ str(e) )

def tax_Data(invoice,sales_invoice_doc):
            try:

                #for foreign currency
                if sales_invoice_doc.currency != "SAR":
                    cac_TaxTotal = ET.SubElement(invoice, "cac:TaxTotal")
                    cbc_TaxAmount_SAR = ET.SubElement(cac_TaxTotal, "cbc:TaxAmount")
                    cbc_TaxAmount_SAR.set("currencyID", "SAR") # SAR is as zatca requires tax amount in SAR
                    tax_amount_without_retention_sar =  round(sales_invoice_doc.conversion_rate * abs(get_tax_total_from_items(sales_invoice_doc)),2)
                    cbc_TaxAmount_SAR.text = str(round( tax_amount_without_retention_sar,2))     # str( abs(sales_invoice_doc.base_total_taxes_and_charges))
                #end for foreign currency
                
                
                #for SAR currency
                if sales_invoice_doc.currency == "SAR":
                    cac_TaxTotal = ET.SubElement(invoice, "cac:TaxTotal")
                    cbc_TaxAmount_SAR = ET.SubElement(cac_TaxTotal, "cbc:TaxAmount")
                    cbc_TaxAmount_SAR.set("currencyID", "SAR") # SAR is as zatca requires tax amount in SAR
                    tax_amount_without_retention_sar =  round(abs(get_tax_total_from_items(sales_invoice_doc)),2)
                    cbc_TaxAmount_SAR.text = str(round( tax_amount_without_retention_sar,2))     # str( abs(sales_invoice_doc.base_total_taxes_and_charges))
                #end for SAR currency
                
                
        
                cac_TaxTotal = ET.SubElement(invoice, "cac:TaxTotal")
                cbc_TaxAmount = ET.SubElement(cac_TaxTotal, "cbc:TaxAmount")
                cbc_TaxAmount.set("currencyID", sales_invoice_doc.currency) # SAR is as zatca requires tax amount in SAR
                tax_amount_without_retention =  round(abs(get_tax_total_from_items(sales_invoice_doc)),2)
                cbc_TaxAmount.text = str(round( tax_amount_without_retention,2))     # str( abs(sales_invoice_doc.base_total_taxes_and_charges))
                cac_TaxSubtotal = ET.SubElement(cac_TaxTotal, "cac:TaxSubtotal")
                cbc_TaxableAmount = ET.SubElement(cac_TaxSubtotal, "cbc:TaxableAmount")
                cbc_TaxableAmount.set("currencyID", sales_invoice_doc.currency)
                cbc_TaxableAmount.text =str(abs(round(sales_invoice_doc.base_net_total,2)))
                cbc_TaxAmount_2 = ET.SubElement(cac_TaxSubtotal, "cbc:TaxAmount")
                cbc_TaxAmount_2.set("currencyID", sales_invoice_doc.currency)
                
                cbc_TaxAmount_2.text = str(tax_amount_without_retention) # str(abs(sales_invoice_doc.base_total_taxes_and_charges))
                cac_TaxCategory_1 = ET.SubElement(cac_TaxSubtotal, "cac:TaxCategory")
                cbc_ID_8 = ET.SubElement(cac_TaxCategory_1, "cbc:ID")
                # if sales_invoice_doc.custom_zatca_tax_category == "Standard":
                #     cbc_ID_8.text = "S"
                # elif sales_invoice_doc.custom_zatca_tax_category == "Zero Rated":
                #     cbc_ID_8.text = "Z"
                # elif sales_invoice_doc.custom_zatca_tax_category == "Exempted":
                #     cbc_ID_8.text = "E"
                # elif sales_invoice_doc.custom_zatca_tax_category == "Services outside scope of tax / Not subject to VAT":
                #     cbc_ID_8.text = "O"
                cbc_ID_8.text = "S"

                cbc_Percent_1 = ET.SubElement(cac_TaxCategory_1, "cbc:Percent")
                # cbc_Percent_1.text = str(sales_invoice_doc.taxes[0].rate)
                cbc_Percent_1.text = f"{float(sales_invoice_doc.taxes[0].rate):.2f}" 
                exemption_reason_map = get_exemption_reason_map()
                # if sales_invoice_doc.custom_zatca_tax_category != "Standard":
                #     cbc_TaxExemptionReasonCode = ET.SubElement(cac_TaxCategory_1, "cbc:TaxExemptionReasonCode")
                #     cbc_TaxExemptionReasonCode.text = sales_invoice_doc.custom_exemption_reason_code
                #     cbc_TaxExemptionReason = ET.SubElement(cac_TaxCategory_1, "cbc:TaxExemptionReason")
                #     reason_code = sales_invoice_doc.custom_exemption_reason_code
                #     if reason_code in exemption_reason_map:
                #         cbc_TaxExemptionReason.text = exemption_reason_map[reason_code]       
                cac_TaxScheme_3 = ET.SubElement(cac_TaxCategory_1, "cac:TaxScheme")
                cbc_ID_9 = ET.SubElement(cac_TaxScheme_3, "cbc:ID")
                cbc_ID_9.text = "VAT"
                
                # cac_TaxTotal = ET.SubElement(invoice, "cac:TaxTotal")
                # cbc_TaxAmount = ET.SubElement(cac_TaxTotal, "cbc:TaxAmount")
                # cbc_TaxAmount.set("currencyID", sales_invoice_doc.currency)
                # cbc_TaxAmount.text =str(round(tax_amount_without_retention,2))
                
                cac_LegalMonetaryTotal = ET.SubElement(invoice, "cac:LegalMonetaryTotal")
                cbc_LineExtensionAmount = ET.SubElement(cac_LegalMonetaryTotal, "cbc:LineExtensionAmount")
                cbc_LineExtensionAmount.set("currencyID", sales_invoice_doc.currency)
                cbc_LineExtensionAmount.text =  str(abs(sales_invoice_doc.base_net_total))
                cbc_TaxExclusiveAmount = ET.SubElement(cac_LegalMonetaryTotal, "cbc:TaxExclusiveAmount")
                cbc_TaxExclusiveAmount.set("currencyID", sales_invoice_doc.currency)
                cbc_TaxExclusiveAmount.text = str(abs(sales_invoice_doc.net_total))
                cbc_TaxInclusiveAmount = ET.SubElement(cac_LegalMonetaryTotal, "cbc:TaxInclusiveAmount")
                cbc_TaxInclusiveAmount.set("currencyID", sales_invoice_doc.currency)
                cbc_TaxInclusiveAmount.text = str(round(abs(sales_invoice_doc.net_total) + abs(tax_amount_without_retention),2))
                cbc_AllowanceTotalAmount = ET.SubElement(cac_LegalMonetaryTotal, "cbc:AllowanceTotalAmount")
                cbc_AllowanceTotalAmount.set("currencyID", sales_invoice_doc.currency)
                cbc_AllowanceTotalAmount.text = str(sales_invoice_doc.base_change_amount)
                cbc_PayableAmount = ET.SubElement(cac_LegalMonetaryTotal, "cbc:PayableAmount")
                cbc_PayableAmount.set("currencyID", sales_invoice_doc.currency)
                cbc_PayableAmount.text = str(round(abs(sales_invoice_doc.net_total) + abs(tax_amount_without_retention),2))
                return invoice
             
            except Exception as e:
                        frappe.throw("error occured in tax data"+ str(e) )

def tax_Data_with_template(invoice,sales_invoice_doc):
       
            try:
             
                total_tax = sum(single_item.net_amount * (frappe.get_doc('Item Tax Template', single_item.item_tax_template).taxes[0].tax_rate / 100)
                    for single_item in sales_invoice_doc.items)
                #for foreign currency
                if sales_invoice_doc.currency != "SAR":
                    cac_TaxTotal = ET.SubElement(invoice, "cac:TaxTotal")
                    cbc_TaxAmount_SAR = ET.SubElement(cac_TaxTotal, "cbc:TaxAmount")
                    cbc_TaxAmount_SAR.set("currencyID", "SAR") # SAR is as zatca requires tax amount in SAR
                    tax_amount_without_retention_sar =  round(sales_invoice_doc.conversion_rate * abs(total_tax),2)
                    cbc_TaxAmount_SAR.text = str(round( tax_amount_without_retention_sar,2))     # str( abs(sales_invoice_doc.base_total_taxes_and_charges))
                #end for foreign currency
                
                
                #for SAR currency   
                if sales_invoice_doc.currency == "SAR":
                    cac_TaxTotal = ET.SubElement(invoice, "cac:TaxTotal")
                    cbc_TaxAmount_SAR = ET.SubElement(cac_TaxTotal, "cbc:TaxAmount")
                    cbc_TaxAmount_SAR.set("currencyID", "SAR") # SAR is as zatca requires tax amount in SAR
                    tax_amount_without_retention_sar =  round(abs(total_tax),2)
                    cbc_TaxAmount_SAR.text = str(round( tax_amount_without_retention_sar,2))     # str( abs(sales_invoice_doc.base_total_taxes_and_charges))
                #end for SAR currency
                
                
        
                cac_TaxTotal = ET.SubElement(invoice, "cac:TaxTotal")
                cbc_TaxAmount = ET.SubElement(cac_TaxTotal, "cbc:TaxAmount")
                cbc_TaxAmount.set("currencyID", sales_invoice_doc.currency) # SAR is as zatca requires tax amount in SAR
                tax_amount_without_retention =  round(abs(total_tax),2)
                cbc_TaxAmount.text = str(round( tax_amount_without_retention,2))     # str( abs(sales_invoice_doc.base_total_taxes_and_charges))
                processed_tax_templates = set()

                for item in sales_invoice_doc.items:
                    item_tax_template = frappe.get_doc('Item Tax Template', item.item_tax_template)
                    if item.item_tax_template in processed_tax_templates:
                        continue
                    processed_tax_templates.add(item.item_tax_template)

                    # zatca_tax_category = item_tax_template.custom_zatca_tax_category
                    zatca_tax_category = "Standard"

                    exemption_reason_code = item_tax_template.custom_exemption_reason_code 
                    
                    for tax in item_tax_template.taxes:
                        item_tax_percentage = item_tax_template.taxes[0].tax_rate if item_tax_template.taxes else 15

                        cac_TaxSubtotal = ET.SubElement(cac_TaxTotal, "cac:TaxSubtotal")
                        cbc_TaxableAmount = ET.SubElement(cac_TaxSubtotal, "cbc:TaxableAmount")
                        cbc_TaxableAmount.set("currencyID", sales_invoice_doc.currency)
                        cbc_TaxableAmount.text = str(abs(item.base_net_amount))
                        cbc_TaxAmount_2 = ET.SubElement(cac_TaxSubtotal, "cbc:TaxAmount")
                        cbc_TaxAmount_2.set("currencyID", sales_invoice_doc.currency)
                        cbc_TaxAmount_2.text =str(abs(round(item_tax_percentage * item.base_net_amount / 100,2)))

                        cac_TaxCategory_1 = ET.SubElement(cac_TaxSubtotal, "cac:TaxCategory")
                        cbc_ID_8 = ET.SubElement(cac_TaxCategory_1, "cbc:ID")

                        if zatca_tax_category == "Standard":
                            cbc_ID_8.text = "S"
                        elif zatca_tax_category == "Zero Rated":
                            cbc_ID_8.text = "Z"
                        elif zatca_tax_category == "Exempted":
                            cbc_ID_8.text = "E"
                        elif zatca_tax_category == "Services outside scope of tax / Not subject to VAT":
                            cbc_ID_8.text = "O"

                        cbc_Percent_1 = ET.SubElement(cac_TaxCategory_1, "cbc:Percent")
                        cbc_Percent_1.text = f"{float(tax.tax_rate):.2f}"

                        exemption_reason_map = get_exemption_reason_map()

                        if zatca_tax_category != "Standard":
                            cbc_TaxExemptionReasonCode = ET.SubElement(cac_TaxCategory_1, "cbc:TaxExemptionReasonCode")
                            cbc_TaxExemptionReasonCode.text = exemption_reason_code
                            cbc_TaxExemptionReason = ET.SubElement(cac_TaxCategory_1, "cbc:TaxExemptionReason")

                            if exemption_reason_code in exemption_reason_map:
                                cbc_TaxExemptionReason.text = exemption_reason_map[exemption_reason_code]

                        cac_TaxScheme = ET.SubElement(cac_TaxCategory_1, "cac:TaxScheme")
                        cbc_TaxScheme_ID = ET.SubElement(cac_TaxScheme, "cbc:ID")
                        cbc_TaxScheme_ID.text = "VAT"


                # cac_TaxTotal = ET.SubElement(invoice, "cac:TaxTotal")
                # cbc_TaxAmount = ET.SubElement(cac_TaxTotal, "cbc:TaxAmount")
                # cbc_TaxAmount.set("currencyID", sales_invoice_doc.currency)
                # cbc_TaxAmount.text =str(round(tax_amount_without_retention,2))
                
                cac_LegalMonetaryTotal = ET.SubElement(invoice, "cac:LegalMonetaryTotal")
                cbc_LineExtensionAmount = ET.SubElement(cac_LegalMonetaryTotal, "cbc:LineExtensionAmount")
                cbc_LineExtensionAmount.set("currencyID", sales_invoice_doc.currency)
                cbc_LineExtensionAmount.text =  str(abs(sales_invoice_doc.base_net_total))
                cbc_TaxExclusiveAmount = ET.SubElement(cac_LegalMonetaryTotal, "cbc:TaxExclusiveAmount")
                cbc_TaxExclusiveAmount.set("currencyID", sales_invoice_doc.currency)
                cbc_TaxExclusiveAmount.text = str(abs(sales_invoice_doc.net_total))
                cbc_TaxInclusiveAmount = ET.SubElement(cac_LegalMonetaryTotal, "cbc:TaxInclusiveAmount")
                cbc_TaxInclusiveAmount.set("currencyID", sales_invoice_doc.currency)
                cbc_TaxInclusiveAmount.text = str(round(abs(sales_invoice_doc.net_total) + abs(tax_amount_without_retention),2))
                cbc_AllowanceTotalAmount = ET.SubElement(cac_LegalMonetaryTotal, "cbc:AllowanceTotalAmount")
                cbc_AllowanceTotalAmount.set("currencyID", sales_invoice_doc.currency)
                cbc_AllowanceTotalAmount.text = str(sales_invoice_doc.base_change_amount)
                cbc_PayableAmount = ET.SubElement(cac_LegalMonetaryTotal, "cbc:PayableAmount")
                cbc_PayableAmount.set("currencyID", sales_invoice_doc.currency)
                cbc_PayableAmount.text = str(round(abs(sales_invoice_doc.net_total) + abs(tax_amount_without_retention),2))
                return invoice
             
            except Exception as e:
                    frappe.throw("error occured in tax data"+ str(e) )
                    
def get_tax_total_from_items(sales_invoice_doc):
            try:
                total_tax = 0
                for single_item in sales_invoice_doc.items : 
                    item_tax_amount,tax_percent =  get_Tax_for_Item(sales_invoice_doc.taxes[0].item_wise_tax_detail,single_item.item_code)
                    total_tax = total_tax + (single_item.net_amount * (tax_percent/100))
                return total_tax 
            except Exception as e:
                    frappe.throw("Error occured in get_tax_total_from_items "+ str(e) )