import xml.etree.ElementTree as ET


def delivery_And_PaymentMeans(invoice,is_return=1):
            try:
                cac_Delivery = ET.SubElement(invoice, "cac:Delivery")
                cbc_ActualDeliveryDate = ET.SubElement(cac_Delivery, "cbc:ActualDeliveryDate")
                cbc_ActualDeliveryDate.text = "1234"
                cac_PaymentMeans = ET.SubElement(invoice, "cac:PaymentMeans")
                cbc_PaymentMeansCode = ET.SubElement(cac_PaymentMeans, "cbc:PaymentMeansCode")
                cbc_PaymentMeansCode.text = "30"
                
                if is_return == 1:
                    cbc_InstructionNote = ET.SubElement(cac_PaymentMeans, "cbc:InstructionNote")
                    cbc_InstructionNote.text = "Cancellation"    
                return invoice
            except Exception as e:
                    print(str(e))