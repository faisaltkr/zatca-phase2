import xml.etree.ElementTree as ET


def invoice_Typecode_Simplified(invoice,is_return=0):
            try:                             
                cbc_InvoiceTypeCode = ET.SubElement(invoice, "cbc:InvoiceTypeCode")
                if is_return == 0:         
                    cbc_InvoiceTypeCode.set("name", "0200000") # Simplified
                    cbc_InvoiceTypeCode.text = "388"
                elif is_return == 1:       # return items and simplified invoice
                    cbc_InvoiceTypeCode.set("name", "0200000")  # Simplified
                    cbc_InvoiceTypeCode.text = "381"  # Credit note
                return invoice
            except Exception as e:
                    print(str(e))


def invoice_Typecode_Standard(invoice, is_return=0):
            try:
                    cbc_InvoiceTypeCode = ET.SubElement(invoice, "cbc:InvoiceTypeCode")
                    cbc_InvoiceTypeCode.set("name", "0100000") # Standard
                    if is_return == 0:
                        cbc_InvoiceTypeCode.text = "388"
                    elif is_return == 1:     # return items and simplified invoice
                        cbc_InvoiceTypeCode.text = "381" # Credit note
                    return invoice
            except Exception as e:
                    print(str(e))