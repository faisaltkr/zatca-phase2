import frappe
import xml.etree.ElementTree as ET
import json

def get_Tax_for_Item(full_string,item):
            try:                                          # getting tax percentage and tax amount
                data = json.loads(full_string)
                tax_percentage=data.get(item,[0,0])[0]
                tax_amount = data.get(item, [0, 0])[1]
                return tax_amount,tax_percentage
            except Exception as e:
                    frappe.throw("error occured in tax for item"+ str(e) )

def item_data(invoice,sales_invoice_doc):
            try:    
                for single_item in sales_invoice_doc.items : 
                    print(single_item.as_dict(),"djfdjfjdjfgjgjdfjfjjjjjjj")
                    item_tax_amount,item_tax_percentage =  get_Tax_for_Item(sales_invoice_doc.taxes[0].item_wise_tax_detail,single_item.item_code)
                    cac_InvoiceLine = ET.SubElement(invoice, "cac:InvoiceLine")
                    cbc_ID_10 = ET.SubElement(cac_InvoiceLine, "cbc:ID")
                    cbc_ID_10.text = str(single_item.idx)
                    cbc_InvoicedQuantity = ET.SubElement(cac_InvoiceLine, "cbc:InvoicedQuantity")
                    cbc_InvoicedQuantity.set("unitCode", str(single_item.uom))
                    cbc_InvoicedQuantity.text = str(abs(single_item.qty))
                    cbc_LineExtensionAmount_1 = ET.SubElement(cac_InvoiceLine, "cbc:LineExtensionAmount")
                    cbc_LineExtensionAmount_1.set("currencyID", sales_invoice_doc.currency)
                    cbc_LineExtensionAmount_1.text=  str(abs(single_item.amount))
                    cac_TaxTotal_2 = ET.SubElement(cac_InvoiceLine, "cac:TaxTotal")
                    cbc_TaxAmount_3 = ET.SubElement(cac_TaxTotal_2, "cbc:TaxAmount")
                    cbc_TaxAmount_3.set("currencyID", sales_invoice_doc.currency)
                    cbc_TaxAmount_3.text = str(abs(round(item_tax_percentage * single_item.amount / 100,2)))
                    cbc_RoundingAmount = ET.SubElement(cac_TaxTotal_2, "cbc:RoundingAmount")
                    cbc_RoundingAmount.set("currencyID", sales_invoice_doc.currency)
                    cbc_RoundingAmount.text=str(abs(round(single_item.amount + (item_tax_percentage * single_item.amount / 100),2)))
                    cac_Item = ET.SubElement(cac_InvoiceLine, "cac:Item")
                    cbc_Name = ET.SubElement(cac_Item, "cbc:Name")
                    cbc_Name.text = single_item.item_code
                    cac_ClassifiedTaxCategory = ET.SubElement(cac_Item, "cac:ClassifiedTaxCategory")
                    cbc_ID_11 = ET.SubElement(cac_ClassifiedTaxCategory, "cbc:ID")
                    if sales_invoice_doc.custom_zatca_tax_category == "Standard":
                        cbc_ID_11 .text = "S"
                    elif sales_invoice_doc.custom_zatca_tax_category == "Zero Rated":
                        cbc_ID_11 .text = "Z"
                    elif sales_invoice_doc.custom_zatca_tax_category == "Exempted":
                        cbc_ID_11 .text = "E"
                    elif sales_invoice_doc.custom_zatca_tax_category == "Services outside scope of tax / Not subject to VAT":
                        cbc_ID_11 .text = "O"
                    cbc_Percent_2 = ET.SubElement(cac_ClassifiedTaxCategory, "cbc:Percent")
                    cbc_Percent_2.text = f"{float(item_tax_percentage):.2f}"
                    cac_TaxScheme_4 = ET.SubElement(cac_ClassifiedTaxCategory, "cac:TaxScheme")
                    cbc_ID_12 = ET.SubElement(cac_TaxScheme_4, "cbc:ID")
                    cbc_ID_12.text = "VAT"
                    cac_Price = ET.SubElement(cac_InvoiceLine, "cac:Price")
                    cbc_PriceAmount = ET.SubElement(cac_Price, "cbc:PriceAmount")
                    cbc_PriceAmount.set("currencyID", sales_invoice_doc.currency)
                    cbc_PriceAmount.text =  str(abs(single_item.amount))
                    
                return invoice
            except Exception as e:
                    frappe.throw("error occured in item data"+ str(e) )

def item_data_with_template(invoice, sales_invoice_doc):
    try:
        for single_item in sales_invoice_doc.items:
            print(single_item.as_dict(),"djfdjfjdjfgjgjdfjfjjjjjjj")
            item_tax_template = frappe.get_doc('Item Tax Template', single_item.item_tax_template)
            item_tax_percentage = item_tax_template.taxes[0].tax_rate if item_tax_template.taxes else 15
            
            cac_InvoiceLine = ET.SubElement(invoice, "cac:InvoiceLine")
            cbc_ID_10 = ET.SubElement(cac_InvoiceLine, "cbc:ID")
            cbc_ID_10.text = str(single_item.idx)
            cbc_InvoicedQuantity = ET.SubElement(cac_InvoiceLine, "cbc:InvoicedQuantity")
            cbc_InvoicedQuantity.set("unitCode", str(single_item.uom))
            cbc_InvoicedQuantity.text = str(abs(single_item.qty))
            cbc_LineExtensionAmount_1 = ET.SubElement(cac_InvoiceLine, "cbc:LineExtensionAmount")
            cbc_LineExtensionAmount_1.set("currencyID", sales_invoice_doc.currency)
            cbc_LineExtensionAmount_1.text = str(abs(single_item.amount))
            
            cac_TaxTotal_2 = ET.SubElement(cac_InvoiceLine, "cac:TaxTotal")
            cbc_TaxAmount_3 = ET.SubElement(cac_TaxTotal_2, "cbc:TaxAmount")
            cbc_TaxAmount_3.set("currencyID", sales_invoice_doc.currency)
            cbc_TaxAmount_3.text = str(abs(round(item_tax_percentage * single_item.amount / 100, 2)))
            cbc_RoundingAmount = ET.SubElement(cac_TaxTotal_2, "cbc:RoundingAmount")
            cbc_RoundingAmount.set("currencyID", sales_invoice_doc.currency)
            cbc_RoundingAmount.text = str(abs(round(single_item.amount + (item_tax_percentage * single_item.amount / 100), 2)))
            
            cac_Item = ET.SubElement(cac_InvoiceLine, "cac:Item")
            cbc_Name = ET.SubElement(cac_Item, "cbc:Name")
            cbc_Name.text = single_item.item_code
            
            cac_ClassifiedTaxCategory = ET.SubElement(cac_Item, "cac:ClassifiedTaxCategory")
            cbc_ID_11 = ET.SubElement(cac_ClassifiedTaxCategory, "cbc:ID")
            # zatca_tax_category = item_tax_template.custom_zatca_tax_category
            zatca_tax_category = "Standard"
            if zatca_tax_category == "Standard":
                cbc_ID_11.text = "S"
            elif zatca_tax_category == "Zero Rated":
                cbc_ID_11.text = "Z"
            elif zatca_tax_category == "Exempted":
                cbc_ID_11.text = "E"
            elif zatca_tax_category == "Services outside scope of tax / Not subject to VAT":
                cbc_ID_11.text = "O"
            
            cbc_Percent_2 = ET.SubElement(cac_ClassifiedTaxCategory, "cbc:Percent")
            cbc_Percent_2.text = f"{float(item_tax_percentage):.2f}"
            
            cac_TaxScheme_4 = ET.SubElement(cac_ClassifiedTaxCategory, "cac:TaxScheme")
            cbc_ID_12 = ET.SubElement(cac_TaxScheme_4, "cbc:ID")
            cbc_ID_12.text = "VAT"
            
            cac_Price = ET.SubElement(cac_InvoiceLine, "cac:Price")
            cbc_PriceAmount = ET.SubElement(cac_Price, "cbc:PriceAmount")
            cbc_PriceAmount.set("currencyID", sales_invoice_doc.currency)
            cbc_PriceAmount.text = str(abs(single_item.rate))
            
        return invoice
    except Exception as e:
        frappe.throw("Error occurred in item data" + str(e))
