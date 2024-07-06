import xml.etree.ElementTree as ET
import hashlib
import base64
import frappe
from datetime import datetime
import xml.dom.minidom as minidom
from lxml import etree
import json
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import binascii
import pyqrcode
from zatca_sa_phase2.zatca_sa_phase2.doctype.csr_settings.utils.get_values import get_zatca_settings


# Get the current date

def dateformat():
    current_date = datetime.now()
    # Format the current date as YYYYMMDD
    formatted_current_date = current_date.strftime("%Y%m%d")

    return formatted_current_date

def timeformat():
    # Get the current time
    current_time = datetime.now()

    # Format the current time to HHMMSS format
    current_time_string = current_time.strftime("%H%M%S")

    return current_time_string


def base_64_hash(data):
        sha256_hash = hashlib.sha256(data.encode('utf-8')).digest()

        # Convert hash to hexadecimal string
        hex_hash = sha256_hash.hex()

        # Encode the hexadecimal hash in base64
        base64_encoded_hash = base64.b64encode(hex_hash.encode('utf-8')).decode('utf-8')

        return base64_encoded_hash



def get_private_path():
    return  frappe.utils.get_files_path(is_private=True)


def xml_structuring(invoice,sales_invoice_doc):
            try:
                xml_declaration = "<?xml version='1.0' encoding='UTF-8'?>\n"
                tree = ET.ElementTree(invoice)
                with open(frappe.local.site + "/private/files/xml_files.xml", 'wb') as file:
                    tree.write(file, encoding='utf-8', xml_declaration=True)
                with open(frappe.local.site + "/private/files/xml_files.xml", 'r') as file:
                    xml_string = file.read()
                xml_dom = minidom.parseString(xml_string)
                pretty_xml_string = xml_dom.toprettyxml(indent="  ")   # created xml into formatted xml form 
                with open(frappe.local.site + "/private/files/finalzatcaxml.xml", 'w') as file:
                    file.write(pretty_xml_string)
                          # Attach the getting xml for each invoice
                try:
                    if frappe.db.exists("File",{ "attached_to_name": sales_invoice_doc.name, "attached_to_doctype": sales_invoice_doc.doctype }):
                        frappe.db.delete("File",{ "attached_to_name":sales_invoice_doc.name, "attached_to_doctype": sales_invoice_doc.doctype })
                except Exception as e:
                    frappe.throw(frappe.get_traceback())
                
                try:
                    fileX = frappe.get_doc(
                        {   "doctype": "File",        
                            "file_type": "xml",  
                            "file_name":  "E-invoice-" + sales_invoice_doc.name + ".xml",
                            "attached_to_doctype":sales_invoice_doc.doctype,
                            "attached_to_name":sales_invoice_doc.name, 
                            "content": pretty_xml_string,
                            "is_private": 1,})
                    fileX.save()
                except Exception as e:
                    frappe.throw(frappe.get_traceback())
                
                try:
                    frappe.db.get_value('File', {'attached_to_name':sales_invoice_doc.name, 'attached_to_doctype': sales_invoice_doc.doctype}, ['file_name'])
                except Exception as e:
                    frappe.throw(frappe.get_traceback())
            except Exception as e:
                    frappe.throw("Error occured in XML structuring and attach. Please contact your system administrator"+ str(e) )

def canonicalize_xml (tag_removed_xml):
                try:
                    #Code corrected by Farook K - ERPGulf
                    canonical_xml = etree.tostring(tag_removed_xml, method="c14n").decode()
                    return canonical_xml    
                except Exception as e:
                            frappe.throw(" error in canonicalise xml: "+ str(e) )


def getInvoiceHash(canonicalized_xml):
        try:
            #Code corrected by Farook K - ERPGulf
            hash_object = hashlib.sha256(canonicalized_xml.encode())
            hash_hex = hash_object.hexdigest()
            # print(hash_hex)
            hash_base64 = base64.b64encode(bytes.fromhex(hash_hex)).decode('utf-8')
            # base64_encoded = base64.b64encode(hash_hex.encode()).decode()
            return hash_hex,hash_base64
        except Exception as e:
                    frappe.throw(" error in Invoice hash of xml: "+ str(e) )


def digital_signature(hash1):
                    try:
                        print("digital settings")
                        key = frappe.get_all('CSR Settings', fields=['private_key'])
                        key_file =  key[0]['private_key']
                        # settings = frappe.get_doc('CSR Settings')
                        print(key_file)
                        # company = "mycompany"
                        # company_name = frappe.db.get_value("", company, "abbr")
                        # company_name = "mycompany"
                        # basic_auth = settings.get("private_key", "{}")
                        # private_key_data   = json.loads(basic_auth)
                        # key_file = get_private_key_for_company(private_key_data, company_name)
                        # key_file = ""
                        private_key_bytes = key_file.encode('utf-8')
                        private_key = serialization.load_pem_private_key(private_key_bytes, password=None, backend=default_backend())
                        hash_bytes = bytes.fromhex(hash1)
                        signature = private_key.sign(hash_bytes, ec.ECDSA(hashes.SHA256()))
                        encoded_signature = base64.b64encode(signature).decode()
                        return encoded_signature
                    except Exception as e:
                             frappe.throw(" error in digital signature: "+ str(e) )

def get_private_key_for_company(private_key_data, company_name):
                    try:     
                        for entry in private_key_data.get("companies", []):
                            if entry.get("company") == company_name:
                                return entry.get("private_key_data")
                        return None
                    except Exception as e:
                        frappe.throw("Error in getting private key for company: " + str(e))


def get_certificate_for_company(certificate_content, company_name):
                    try:
                        for entry in certificate_content.get("data", []):
                            if entry.get("company") == company_name:
                                return entry.get("certificate")
                        return None
                    except Exception as e:
                        frappe.throw("Error in getting certificate for company: " + str(e))

def extract_certificate_details(customer_doc):
            try:    
                    # settings = frappe.get_doc('Zatca ERPgulf Setting')  
                    company_name = "mycompany"
                    key = frappe.get_all('CSR Settings', fields=['csid'])
                    certificate_content =  key[0]['csid']
                    # certificate_data_str = settings.get("certificate", "{}")
                    # try:
                    #     certificate_data = json.loads(certificate_data_str)
                    # except json.JSONDecodeError:
                    #     frappe.throw("Certificate field contains invalid JSON")
                    
                    # certificate_content = get_certificate_for_company(certificate_data, company_name)

                    if not certificate_content:
                        frappe.throw(f"No certificate found for company {company_name}")
                    formatted_certificate = "-----BEGIN CERTIFICATE-----\n"
                    formatted_certificate += "\n".join(certificate_content[i:i+64] for i in range(0, len(certificate_content), 64))
                    formatted_certificate += "\n-----END CERTIFICATE-----\n"
                    certificate_bytes = formatted_certificate.encode('utf-8')
                    cert = x509.load_pem_x509_certificate(certificate_bytes, default_backend())
                    formatted_issuer_name = cert.issuer.rfc4514_string()

                    if customer_doc.custom_b2c == 1:
                        company_details = get_zatca_settings()
                        issuer_name = company_details['issuer_name']
                        serial_number = company_details['issuer_serial_number']
                        # serial_number = cert.serial_number

                    else:
                        issuer_name = ", ".join([x.strip() for x in formatted_issuer_name.split(',')])
                        serial_number = cert.serial_number
                    return issuer_name, serial_number
            except Exception as e:
                             frappe.throw(" error in extracting certificate details: "+ str(e) )
    


def certificate_hash():
            
            try:
                # company_name = "mycompany"
                key = frappe.get_all('CSR Settings', fields=['csid'])
                certificate_data =  key[0]['csid']
                # settings = frappe.get_doc('Zatca ERPgulf Setting')
                # company = settings.company
                # company_name = frappe.db.get_value("Company", company, "abbr")
                # certificate_data_str = settings.get("certificate", "{}")
                # try:
                #         certificate_data = json.loads(certificate_data_str)
                # except json.JSONDecodeError:
                #         frappe.throw("Certificate field contains invalid JSON")   
                # certificate_data = get_certificate_for_company(certificate_data, company_name)
                # if not certificate_data:
                #         frappe.throw(f"No certificate found for company in certificate hash {company_name}")

                certificate_data_bytes = certificate_data.encode('utf-8')
                sha256_hash = hashlib.sha256(certificate_data_bytes).hexdigest()
                base64_encoded_hash = base64.b64encode(sha256_hash.encode('utf-8')).decode('utf-8')
                return base64_encoded_hash
            
            except Exception as e:
                    frappe.throw("error in obtaining certificate hash: "+ str(e) )


def signxml_modify(customer_doc):
                try:
                    encoded_certificate_hash= certificate_hash()
                    issuer_name, serial_number = extract_certificate_details(customer_doc=customer_doc)
                    original_invoice_xml = etree.parse(frappe.local.site + '/private/files/finalzatcaxml.xml')
                    root = original_invoice_xml.getroot()
                    namespaces = {
                    'ext': 'urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2',
                    'sig': 'urn:oasis:names:specification:ubl:schema:xsd:CommonSignatureComponents-2',
                    'sac':"urn:oasis:names:specification:ubl:schema:xsd:SignatureAggregateComponents-2", 
                    'xades': 'http://uri.etsi.org/01903/v1.3.2#',
                    'ds': 'http://www.w3.org/2000/09/xmldsig#'}
                    ubl_extensions_xpath = "//*[local-name()='Invoice']//*[local-name()='UBLExtensions']"
                    qr_xpath = "//*[local-name()='AdditionalDocumentReference'][cbc:ID[normalize-space(text()) = 'QR']]"
                    signature_xpath = "//*[local-name()='Invoice']//*[local-name()='Signature']"
                    xpath_dv = ("ext:UBLExtensions/ext:UBLExtension/ext:ExtensionContent/sig:UBLDocumentSignatures/sac:SignatureInformation/ds:Signature/ds:Object/xades:QualifyingProperties/xades:SignedProperties/xades:SignedSignatureProperties/xades:SigningCertificate/xades:Cert/xades:CertDigest/ds:DigestValue")
                    xpath_signTime = ("ext:UBLExtensions/ext:UBLExtension/ext:ExtensionContent/sig:UBLDocumentSignatures/sac:SignatureInformation/ds:Signature/ds:Object/xades:QualifyingProperties/xades:SignedProperties/xades:SignedSignatureProperties/xades:SigningTime")
                    xpath_issuerName = ("ext:UBLExtensions/ext:UBLExtension/ext:ExtensionContent/sig:UBLDocumentSignatures/sac:SignatureInformation/ds:Signature/ds:Object/xades:QualifyingProperties/xades:SignedProperties/xades:SignedSignatureProperties/xades:SigningCertificate/xades:Cert/xades:IssuerSerial/ds:X509IssuerName")
                    xpath_serialNum = ("ext:UBLExtensions/ext:UBLExtension/ext:ExtensionContent/sig:UBLDocumentSignatures/sac:SignatureInformation/ds:Signature/ds:Object/xades:QualifyingProperties/xades:SignedProperties//xades:SignedSignatureProperties/xades:SigningCertificate/xades:Cert/xades:IssuerSerial/ds:X509SerialNumber")
                    element_dv = root.find(xpath_dv, namespaces)
                    element_st = root.find(xpath_signTime, namespaces)
                    element_in = root.find(xpath_issuerName, namespaces)
                    element_sn = root.find(xpath_serialNum, namespaces)
                    element_dv.text = (encoded_certificate_hash)
                    element_st.text =  datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
                    signing_time =element_st.text
                    element_in.text = issuer_name
                    element_sn.text = str(serial_number)
                    with open(frappe.local.site + "/private/files/after_step_4.xml", 'wb') as file:
                        original_invoice_xml.write(file,encoding='utf-8',xml_declaration=True,)
                    return namespaces ,signing_time
                except Exception as e:
                    frappe.throw(" error in modification of xml sign part: "+ str(e) )



def generate_Signed_Properties_Hash(signing_time,issuer_name,serial_number,encoded_certificate_hash):
            try:
                xml_string = '''<xades:SignedProperties xmlns:xades="http://uri.etsi.org/01903/v1.3.2#" Id="xadesSignedProperties">
                                    <xades:SignedSignatureProperties>
                                        <xades:SigningTime>{signing_time}</xades:SigningTime>
                                        <xades:SigningCertificate>
                                            <xades:Cert>
                                                <xades:CertDigest>
                                                    <ds:DigestMethod xmlns:ds="http://www.w3.org/2000/09/xmldsig#" Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"/>
                                                    <ds:DigestValue xmlns:ds="http://www.w3.org/2000/09/xmldsig#">{certificate_hash}</ds:DigestValue>
                                                </xades:CertDigest>
                                                <xades:IssuerSerial>
                                                    <ds:X509IssuerName xmlns:ds="http://www.w3.org/2000/09/xmldsig#">{issuer_name}</ds:X509IssuerName>
                                                    <ds:X509SerialNumber xmlns:ds="http://www.w3.org/2000/09/xmldsig#">{serial_number}</ds:X509SerialNumber>
                                                </xades:IssuerSerial>
                                            </xades:Cert>
                                        </xades:SigningCertificate>
                                    </xades:SignedSignatureProperties>
                                </xades:SignedProperties>'''
                xml_string_rendered = xml_string.format(signing_time=signing_time, certificate_hash=encoded_certificate_hash, issuer_name=issuer_name, serial_number=str(serial_number))
                utf8_bytes = xml_string_rendered.encode('utf-8')
                hash_object = hashlib.sha256(utf8_bytes)
                hex_sha256 = hash_object.hexdigest()
                # print(hex_sha256)
                signed_properties_base64=  base64.b64encode(hex_sha256.encode('utf-8')).decode('utf-8')
                # print(signed_properties_base64)
                return signed_properties_base64
            except Exception as e:
                    frappe.throw(" error in generating signed properties hash: "+ str(e) )


def populate_The_UBL_Extensions_Output(encoded_signature,namespaces,signed_properties_base64,encoded_hash):
        try:
            
            updated_invoice_xml = etree.parse(frappe.local.site + '/private/files/after_step_4.xml')
            root3 = updated_invoice_xml.getroot()
            company_name = "mycompany"
            key = frappe.get_all('CSR Settings', fields=['csid'])
            content =  key[0]['csid']
            # settings = frappe.get_doc('Zatca ERPgulf Setting')
            # company = settings.company
            # company_name = frappe.db.get_value("Company", company, "abbr")
            # certificate_data_str = settings.get("certificate", "{}")
            # try:
            #     certificate_data = json.loads(certificate_data_str)
            # except json.JSONDecodeError:
            #     frappe.throw("Certificate field contains invalid JSON")
            
            # content= get_certificate_for_company(certificate_data, company_name)
            # if not content:
            #     frappe.throw(f"No certificate found for company in ubl extension output {company_name}")
            xpath_signvalue = ("ext:UBLExtensions/ext:UBLExtension/ext:ExtensionContent/sig:UBLDocumentSignatures/sac:SignatureInformation/ds:Signature/ds:SignatureValue")
            xpath_x509certi = ("ext:UBLExtensions/ext:UBLExtension/ext:ExtensionContent/sig:UBLDocumentSignatures/sac:SignatureInformation/ds:Signature/ds:KeyInfo/ds:X509Data/ds:X509Certificate")
            xpath_digvalue = ("ext:UBLExtensions/ext:UBLExtension/ext:ExtensionContent/sig:UBLDocumentSignatures/sac:SignatureInformation/ds:Signature/ds:SignedInfo/ds:Reference[@URI='#xadesSignedProperties']/ds:DigestValue")
            xpath_digvalue2 = ("ext:UBLExtensions/ext:UBLExtension/ext:ExtensionContent/sig:UBLDocumentSignatures/sac:SignatureInformation/ds:Signature/ds:SignedInfo/ds:Reference[@Id='invoiceSignedData']/ds:DigestValue")
            signValue6 = root3.find(xpath_signvalue , namespaces)
            x509Certificate6 = root3.find(xpath_x509certi , namespaces)
            digestvalue6 = root3.find(xpath_digvalue , namespaces)
            digestvalue6_2 = root3.find(xpath_digvalue2 , namespaces)
            signValue6.text = (encoded_signature)
            x509Certificate6.text = content
            digestvalue6.text = (signed_properties_base64)
            digestvalue6_2.text =(encoded_hash)
            with open(frappe.local.site + "/private/files/final_xml_after_sign.xml", 'wb') as file:
                updated_invoice_xml.write(file,encoding='utf-8',xml_declaration=True,)
        except Exception as e:
                    frappe.throw(" error in populate ubl extension output: "+ str(e) )



def update_json_data_public_key(existing_data, company_name, public_key):
                try:
                    if "data" not in existing_data:
                        existing_data["data"] = []

                    company_exists = False
                    for entry in existing_data["data"]:
                        if entry["company"] == company_name:
                            entry["public_key_data"] = public_key
                            company_exists = True
                            break
                    if not company_exists:
                        existing_data["data"].append({
                            "company": company_name,
                            "public_key_data": public_key
                        })

                    return existing_data
                except Exception as e:
                    frappe.throw("Error updating JSON data for public key: " + str(e))

def create_public_key():
                try:
                    # settings = frappe.get_doc('Zatca ERPgulf Setting')
                    # company = settings.company
                    # company_name = frappe.db.get_value("Company", company, "abbr")
                    # certificate_data_str = settings.get("certificate", "{}")
                    company_name = "mycompany"
                    key = frappe.get_all('CSR Settings', fields=['csid','public_key'])
                    base_64 =  key[0]['csid']
                    # base_64 =  key[0]['public_key']
                    # print(public_key)
                    # TODO public key
                    # try:
                    #     certificate_data = json.loads(certificate_data_str)
                    # except json.JSONDecodeError:
                    #     frappe.throw("Certificate field contains invalid JSON")
                    
                    # base_64 = get_certificate_for_company(certificate_data, company_name)
                    if not base_64:
                        frappe.throw(f"No certificate found for company in public key creation{company_name}")
                    cert_base64 = """
                    -----BEGIN CERTIFICATE-----
                    {base_64}
                    -----END CERTIFICATE-----
                    """.format(base_64=base_64)
                    cert = x509.load_pem_x509_certificate(cert_base64.encode(), default_backend())
                    public_key = cert.public_key()
                    public_key_pem = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo).decode()  # Convert bytes to string
                            
                    # if not settings.public_key:
                    #     settings.public_key = {}
                    
                    # if isinstance(settings.public_key, str):
                    #     settings.public_key = json.loads(settings.public_key)
                    
                    # updated_data = update_json_data_public_key(public_key, company_name, public_key_pem)
                    # public_key = json.dumps(updated_data)
                    # settings.save(ignore_permissions=True)
                except Exception as e:
                    frappe.throw(" error in public key creation: "+ str(e))

def get_public_key_for_company(data, company_name):
            try:
                for entry in data.get("data", []):
                    if entry.get("company") == company_name:
                        return entry.get("public_key_data")
                return None
            except Exception as e:
                frappe.throw("Error in getting public key for company: " + str(e))

def extract_public_key_data():
            try:
                # settings = frappe.get_doc('Zatca ERPgulf Setting')
                # company = settings.company
                # company_name = frappe.db.get_value("Company", company, "abbr")
                # public_key_data_str = settings.get("public_key", "{}")
                company_name = "mycompany"
                key = frappe.get_all('CSR Settings', fields=['csid','public_key'])
                base_64 =  key[0]['csid']
                public_key_data_str =  key[0]['public_key']
        
                # try:
                #     public_key_data = json.loads(public_key_data_str)
                # except json.JSONDecodeError:
                #     frappe.throw("Public key field contains invalid JSON")
                # public_key_pem = get_public_key_for_company(public_key_data, company_name)
                # if not public_key_pem:
                #     frappe.throw(f"No public key found for company {company_name}")
                lines = public_key_data_str.splitlines()
                key_data = ''.join(lines[1:-1])
                key_data = key_data.replace('-----BEGIN PUBLIC KEY-----', '').replace('-----END PUBLIC KEY-----', '')
                key_data = key_data.replace(' ', '').replace('\n', '')
                
                return key_data
            except Exception as e:
                    frappe.throw(" error in extracting public key data: "+ str(e) )

def tag8_publickey():
                    try:
                        create_public_key()
                        base64_encoded = extract_public_key_data() 
                        
                        byte_data = base64.b64decode(base64_encoded)
                        hex_data = binascii.hexlify(byte_data).decode('utf-8')
                        chunks = [hex_data[i:i + 2] for i in range(0, len(hex_data), 2)]
                        value = ''.join(chunks)
                        binary_data = bytes.fromhex(value)
                        
                        base64_encoded1 = base64.b64encode(binary_data).decode('utf-8')
                        return binary_data
                    except Exception as e: 
                        frappe.throw(" error in tag 8 from public key: "+ str(e) )


def tag9_signature_ecdsa():
            try:

                # settings = frappe.get_doc('Zatca ERPgulf Setting')
                # company = settings.company
                # company_name = frappe.db.get_value("Company", company, "abbr")
                # certificate_data_str = settings.get("certificate", "{}")
                company_name = "mycompany"
                key = frappe.get_all('CSR Settings', fields=['csid'])
                certificate_content =  key[0]['csid']
                # try:
                #     certificate_data = json.loads(certificate_data_str)
                # except json.JSONDecodeError:
                #     frappe.throw("Certificate field contains invalid JSON")
                
                # Get the certificate for the specific company
                # certificate_content= get_certificate_for_company(certificate_data, company_name)
                if not certificate_content:
                    frappe.throw(f"No certificate found for company in tag9 {company_name}")
                formatted_certificate = "-----BEGIN CERTIFICATE-----\n"
                formatted_certificate += "\n".join(certificate_content[i:i+64] for i in range(0, len(certificate_content), 64))
                formatted_certificate += "\n-----END CERTIFICATE-----\n"
                # print(formatted_certificate)
                certificate_bytes = formatted_certificate.encode('utf-8')
                cert = x509.load_pem_x509_certificate(certificate_bytes, default_backend())
                signature = cert.signature
                signature_hex = "".join("{:02x}".format(byte) for byte in signature)
                signature_bytes = bytes.fromhex(signature_hex)
                signature_base64 = base64.b64encode(signature_bytes).decode()

                return signature_bytes
            except Exception as e:
                    frappe.throw(" error in tag 9 (signaturetag): "+ str(e) )

def generate_tlv_xml():
                    try:
                            with open(frappe.local.site + "/private/files/final_xml_after_sign.xml", 'rb') as file:
                                xml_data = file.read()
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
                            issue_date_xpath = "/ubl:Invoice/cbc:IssueDate"
                            issue_time_xpath = "/ubl:Invoice/cbc:IssueTime"
                            issue_date_results = root.xpath(issue_date_xpath, namespaces=namespaces)
                            issue_time_results = root.xpath(issue_time_xpath, namespaces=namespaces)
                            issue_date = issue_date_results[0].text.strip() if issue_date_results else 'Missing Data'
                            issue_time = issue_time_results[0].text.strip() if issue_time_results else 'Missing Data'
                            issue_date_time = issue_date + 'T' + issue_time 
                            tags_xpaths = [
                                (1, "/ubl:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PartyLegalEntity/cbc:RegistrationName"),
                                (2, "/ubl:Invoice/cac:AccountingSupplierParty/cac:Party/cac:PartyTaxScheme/cbc:CompanyID"),
                                (3, None),  
                                (4, "/ubl:Invoice/cac:LegalMonetaryTotal/cbc:TaxInclusiveAmount"),
                                (5, "/ubl:Invoice/cac:TaxTotal/cbc:TaxAmount"),
                                (6, "/ubl:Invoice/ext:UBLExtensions/ext:UBLExtension/ext:ExtensionContent/sig:UBLDocumentSignatures/sac:SignatureInformation/ds:Signature/ds:SignedInfo/ds:Reference/ds:DigestValue"),
                                (7, "/ubl:Invoice/ext:UBLExtensions/ext:UBLExtension/ext:ExtensionContent/sig:UBLDocumentSignatures/sac:SignatureInformation/ds:Signature/ds:SignatureValue"),
                                (8, None), 
                                (9, None) ,
                            ]
                            result_dict = {}
                            for tag, xpath in tags_xpaths:
                                if isinstance(xpath, str):  
                                    elements = root.xpath(xpath, namespaces=namespaces)
                                    if elements:
                                        value = elements[0].text if isinstance(elements[0], etree._Element) else elements[0]
                                        result_dict[tag] = value
                                    else:
                                        result_dict[tag] = 'Not found'
                                else:
                                    result_dict[tag] = xpath  
                            
                            result_dict[3] = issue_date_time
                            result_dict[8] = tag8_publickey()
                            
                            result_dict[9] = tag9_signature_ecdsa()
                            
                            return result_dict
                    except Exception as e:
                        frappe.throw(" error in getting the entire tlv data: "+ str(e) )


def get_tlv_for_value(tag_num, tag_value):
                try:
                    tag_num_buf = bytes([tag_num])
                    if isinstance(tag_value, str):
                        if len(tag_value) < 256:
                            tag_value_len_buf = bytes([len(tag_value)])
                        else:
                            tag_value_len_buf = bytes([0xFF, (len(tag_value) >> 8) & 0xFF, len(tag_value) & 0xFF])
                        tag_value = tag_value.encode('utf-8')
                    else:
                        tag_value_len_buf = bytes([len(tag_value)])
                    return tag_num_buf + tag_value_len_buf + tag_value
                except Exception as e:
                    frappe.throw(" error in getting the tlv data value: "+ str(e) )



def update_Qr_toXml(qrCodeB64):
                    try:
                        xml_file_path = frappe.local.site + "/private/files/final_xml_after_sign.xml"
                        xml_tree = etree.parse(xml_file_path)
                        qr_code_element = xml_tree.find('.//cac:AdditionalDocumentReference[cbc:ID="QR"]/cac:Attachment/cbc:EmbeddedDocumentBinaryObject', namespaces={'cac': 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2', 'cbc': 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2'})
                        if qr_code_element is not None:
                            qr_code_element.text =qrCodeB64
                        else:
                            frappe.msgprint("QR code element not found")

                        xml_tree.write(xml_file_path, encoding="UTF-8", xml_declaration=True)
                    except Exception as e:
                            frappe.throw(" error in saving tlv data to xml: "+ str(e) )

def structuring_signedxml():
                try:
                    with open(frappe.local.site + '/private/files/final_xml_after_sign.xml', 'r') as file:
                        xml_content = file.readlines()
                    indentations = {
                        29: ['<xades:QualifyingProperties xmlns:xades="http://uri.etsi.org/01903/v1.3.2#" Target="signature">','</xades:QualifyingProperties>'],
                        33: ['<xades:SignedProperties Id="xadesSignedProperties">', '</xades:SignedProperties>'],
                        37: ['<xades:SignedSignatureProperties>','</xades:SignedSignatureProperties>'],
                        41: ['<xades:SigningTime>', '<xades:SigningCertificate>','</xades:SigningCertificate>'],
                        45: ['<xades:Cert>','</xades:Cert>'],
                        49: ['<xades:CertDigest>', '<xades:IssuerSerial>', '</xades:CertDigest>', '</xades:IssuerSerial>'],
                        53: ['<ds:DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"/>', '<ds:DigestValue>', '<ds:X509IssuerName>', '<ds:X509SerialNumber>']
                    }
                    def adjust_indentation(line):
                        for col, tags in indentations.items():
                            for tag in tags:
                                if line.strip().startswith(tag):
                                    return ' ' * (col - 1) + line.lstrip()
                        return line
                    adjusted_xml_content = [adjust_indentation(line) for line in xml_content]
                    with open(frappe.local.site + '/private/files/final_xml_after_indent.xml', 'w') as file:
                        file.writelines(adjusted_xml_content)
                    signed_xmlfile_name = frappe.local.site + '/private/files/final_xml_after_indent.xml'
                    return signed_xmlfile_name
                except Exception as e:
                    frappe.throw(" error in structuring signed xml: "+ str(e) )


def attach_QR_Image(qrCodeB64,sales_invoice_doc):
                    try:
                        qr = pyqrcode.create(qrCodeB64)
                        print(qrCodeB64,"qr code ")
                        temp_file_path = "qr_code.png"
                        qr_image=qr.png(temp_file_path, scale=5)
                        print(frappe.get_doc({
                            "doctype": "File",
                            "file_name": f"QR_image_{sales_invoice_doc.name}.png",
                            "attached_to_doctype": sales_invoice_doc.doctype,
                            "attached_to_name": sales_invoice_doc.name,
                            "content": open(temp_file_path, "rb").read()
                           
                        }))
                        file = frappe.get_doc({
                            "doctype": "File",
                            "file_name": f"QR_image_{sales_invoice_doc.name}.png",
                            "attached_to_doctype": sales_invoice_doc.doctype,
                            "attached_to_name": sales_invoice_doc.name,
                            "content": open(temp_file_path, "rb").read()
                           
                        })
                        file.save(ignore_permissions=True)
                    except Exception as e:
                        frappe.throw("error in qrcode from xml:  " + str(e) )