import hashlib
import base64
from lxml import etree

from xml.etree import ElementTree


def generate_xml_hash(invoice):

    xml_string = ElementTree.tostring(invoice, encoding='utf8')
    tree = etree.fromstring(xml_string.encode('utf-8'))

    # Remove specified elements
    for element in tree.xpath('//ext:UBLExtensions | //cac:Signature | //cac:AdditionalDocumentReference[cbc:ID="QR"]', namespaces=tree.nsmap):
        element.getparent().remove(element)

    # Canonicalize the XML
    canonicalized_xml = etree.tostring(tree, method="c14n", exclusive=True, with_comments=False)

    # Compute the SHA-256 hash
    sha256_hash = hashlib.sha256(canonicalized_xml).digest()

    # Encode the hash in Base64
    base64_encoded_hash = base64.b64encode(sha256_hash).decode('utf-8')

    print(base64_encoded_hash, "sdfljsldflsdflsdlf")

    return base64_encoded_hash