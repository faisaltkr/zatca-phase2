"""
class to create invoice standard and simplified
"""
import xml.etree.ElementTree as ET
from xml_tags import generate_xml_tags
from utils import base_64_hash
from invoice_detail import salesinvoice_data
from document_currency import currency_data

class SimplifiedInvoice:

    def __init__(self, cih, pih=None) -> None:
        """
        if invoice hash is not present then hash value of zero as pih
        """
        self.pih = pih
        self.cih = cih
        if not pih:
            self.pih = base_64_hash('0')
        

    def create_simplified_invoice(self):
        """
        invoice generate for simplified
        """
        xml_tags = generate_xml_tags()
        inv_data = salesinvoice_data(xml_tags)
        cur = currency_data(inv_data)
        return cur
    



simp =  SimplifiedInvoice(1,pih=123)
simp_inv = simp.create_simplified_invoice()
tree = ET.ElementTree(simp_inv)


tree.write("invoice_simple.xml", encoding="utf-8", xml_declaration=True)