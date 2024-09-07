import xml.etree.ElementTree as ET
# from .utils import invoice_Typecode_Compliance, doc_Reference
# from .company_details import company_Data
# from .customer_details import customer_Data
# from .invoice_detail import salesinvoice_data
# from .invoice_type import invoice_Typecode_Simplified,invoice_Typecode_Standard
# from .invoice_pay_means import delivery_And_PaymentMeans
# from .invoice_pay_means_cmp import delivery_And_PaymentMeans_for_Compliance
import frappe

def xml_tags(is_b2c):
            try: 
                invoice = ET.Element("Invoice", xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2" )
                invoice.set("xmlns:cac", "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2")
                invoice.set("xmlns:cbc", "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2")
                invoice.set("xmlns:ext", "urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2")   
                ubl_extensions = ET.SubElement(invoice, "ext:UBLExtensions")
                ubl_extension = ET.SubElement(ubl_extensions, "ext:UBLExtension")
                extension_uri = ET.SubElement(ubl_extension, "ext:ExtensionURI")
                extension_uri.text = "urn:oasis:names:specification:ubl:dsig:enveloped:xades"
                extension_content = ET.SubElement(ubl_extension, "ext:ExtensionContent")
                UBL_Document_Signatures = ET.SubElement(extension_content , "sig:UBLDocumentSignatures"    )
                UBL_Document_Signatures.set("xmlns:sig" , "urn:oasis:names:specification:ubl:schema:xsd:CommonSignatureComponents-2")
                UBL_Document_Signatures.set("xmlns:sac" , "urn:oasis:names:specification:ubl:schema:xsd:SignatureAggregateComponents-2")
                UBL_Document_Signatures.set("xmlns:sbc" , "urn:oasis:names:specification:ubl:schema:xsd:SignatureBasicComponents-2")
                Signature_Information = ET.SubElement(UBL_Document_Signatures , "sac:SignatureInformation"  )
                id = ET.SubElement(Signature_Information , "cbc:ID"  )
                id.text = "urn:oasis:names:specification:ubl:signature:1"
                Referenced_SignatureID = ET.SubElement(Signature_Information , "sbc:ReferencedSignatureID"  )
                Referenced_SignatureID.text = "urn:oasis:names:specification:ubl:signature:Invoice"
                Signature = ET.SubElement(Signature_Information , "ds:Signature"  )
                Signature.set("Id" , "signature" )
                Signature.set("xmlns:ds" , "http://www.w3.org/2000/09/xmldsig#" )
                Signed_Info = ET.SubElement(Signature , "ds:SignedInfo"  )
                Canonicalization_Method = ET.SubElement(Signed_Info , "ds:CanonicalizationMethod"  )
                Canonicalization_Method.set("Algorithm" , "http://www.w3.org/2006/12/xml-c14n11"  )
                Signature_Method = ET.SubElement(Signed_Info , "ds:SignatureMethod"  )
                Signature_Method.set("Algorithm" , "http://www.w3.org/2001/04/xmldsig-more#ecdsa-sha256"  )
                Reference = ET.SubElement(Signed_Info , "ds:Reference"  )
                Reference.set("Id"  , "invoiceSignedData")
                Reference.set("URI"  , "")
                Transforms = ET.SubElement(Reference , "ds:Transforms" )
                Transform = ET.SubElement(Transforms , "ds:Transform" )
                Transform.set("Algorithm" , "http://www.w3.org/TR/1999/REC-xpath-19991116")
                XPath = ET.SubElement(Transform , "ds:XPath" )
                XPath.text = "not(//ancestor-or-self::ext:UBLExtensions)"
                Transform2 = ET.SubElement(Transforms , "ds:Transform" )
                Transform2.set("Algorithm" , "http://www.w3.org/TR/1999/REC-xpath-19991116")
                XPath2 = ET.SubElement(Transform2 , "ds:XPath" )
                XPath2.text = "not(//ancestor-or-self::cac:Signature)"
                Transform3 = ET.SubElement(Transforms , "ds:Transform" )
                Transform3.set("Algorithm" , "http://www.w3.org/TR/1999/REC-xpath-19991116")
                XPath3 = ET.SubElement(Transform3 , "ds:XPath" )
                XPath3.text = "not(//ancestor-or-self::cac:AdditionalDocumentReference[cbc:ID='QR'])"
                Transform4 = ET.SubElement(Transforms , "ds:Transform" )
                Transform4.set("Algorithm" , "http://www.w3.org/2006/12/xml-c14n11")
                Diges_Method = ET.SubElement(Reference , "ds:DigestMethod" )
                Diges_Method.set("Algorithm" , "http://www.w3.org/2001/04/xmlenc#sha256")
                Diges_value = ET.SubElement(Reference , "ds:DigestValue" )
                Diges_value.text = "O/vEnAxjLAlw8kQUy8nq/5n8IEZ0YeIyBFvdQA8+iFM="
                Reference2 = ET.SubElement(Signed_Info , "ds:Reference"  )
                Reference2.set("URI" , "#xadesSignedProperties")
                Reference2.set("Type" , "http://www.w3.org/2000/09/xmldsig#SignatureProperties")
                Digest_Method1 = ET.SubElement(Reference2 , "ds:DigestMethod"  )
                Digest_Method1.set("Algorithm" , "http://www.w3.org/2001/04/xmlenc#sha256")
                Digest_value1 = ET.SubElement(Reference2 , "ds:DigestValue"  )
                Digest_value1.text="YjQwZmEyMjM2NDU1YjQwNjM5MTFmYmVkODc4NjM2NTc0N2E3OGFmZjVlMzA1ODAwYWE5Y2ZmYmFjZjRiNjQxNg=="
                Signature_Value = ET.SubElement(Signature , "ds:SignatureValue"  )
                Signature_Value.text = "MEQCIDGBRHiPo6yhXIQ9df6pMEkufcGnoqYaS+O8Jn0xagBiAiBtoxpbrwfEJHhUGQHTqzD1ORX5+Z/tumM0wLfZ4cuYRg=="
                KeyInfo = ET.SubElement(Signature , "ds:KeyInfo"  )
                X509Data = ET.SubElement(KeyInfo , "ds:X509Data"  )
                X509Certificate = ET.SubElement(X509Data , "ds:X509Certificate"  )
                X509Certificate.text = "MIID6TCCA5CgAwIBAgITbwAAf8tem6jngr16DwABAAB/yzAKBggqhkjOPQQDAjBjMRUwEwYKCZImiZPyLGQBGRYFbG9jYWwxEzARBgoJkiaJk/IsZAEZFgNnb3YxFzAVBgoJkiaJk/IsZAEZFgdleHRnYXp0MRwwGgYDVQQDExNUU1pFSU5WT0lDRS1TdWJDQS0xMB4XDTIyMDkxNDEzMjYwNFoXDTI0MDkxMzEzMjYwNFowTjELMAkGA1UEBhMCU0ExEzARBgNVBAoTCjMxMTExMTExMTExDDAKBgNVBAsTA1RTVDEcMBoGA1UEAxMTVFNULTMxMTExMTExMTEwMTExMzBWMBAGByqGSM49AgEGBSuBBAAKA0IABGGDDKDmhWAITDv7LXqLX2cmr6+qddUkpcLCvWs5rC2O29W/hS4ajAK4Qdnahym6MaijX75Cg3j4aao7ouYXJ9GjggI5MIICNTCBmgYDVR0RBIGSMIGPpIGMMIGJMTswOQYDVQQEDDIxLVRTVHwyLVRTVHwzLWE4NjZiMTQyLWFjOWMtNDI0MS1iZjhlLTdmNzg3YTI2MmNlMjEfMB0GCgmSJomT8ixkAQEMDzMxMTExMTExMTEwMTExMzENMAsGA1UEDAwEMTEwMDEMMAoGA1UEGgwDVFNUMQwwCgYDVQQPDANUU1QwHQYDVR0OBBYEFDuWYlOzWpFN3no1WtyNktQdrA8JMB8GA1UdIwQYMBaAFHZgjPsGoKxnVzWdz5qspyuZNbUvME4GA1UdHwRHMEUwQ6BBoD+GPWh0dHA6Ly90c3RjcmwuemF0Y2EuZ292LnNhL0NlcnRFbnJvbGwvVFNaRUlOVk9JQ0UtU3ViQ0EtMS5jcmwwga0GCCsGAQUFBwEBBIGgMIGdMG4GCCsGAQUFBzABhmJodHRwOi8vdHN0Y3JsLnphdGNhLmdvdi5zYS9DZXJ0RW5yb2xsL1RTWkVpbnZvaWNlU0NBMS5leHRnYXp0Lmdvdi5sb2NhbF9UU1pFSU5WT0lDRS1TdWJDQS0xKDEpLmNydDArBggrBgEFBQcwAYYfaHR0cDovL3RzdGNybC56YXRjYS5nb3Yuc2Evb2NzcDAOBgNVHQ8BAf8EBAMCB4AwHQYDVR0lBBYwFAYIKwYBBQUHAwIGCCsGAQUFBwMDMCcGCSsGAQQBgjcVCgQaMBgwCgYIKwYBBQUHAwIwCgYIKwYBBQUHAwMwCgYIKoZIzj0EAwIDRwAwRAIgOgjNPJW017lsIijmVQVkP7GzFO2KQKd9GHaukLgIWFsCIFJF9uwKhTMxDjWbN+1awsnFI7RLBRxA/6hZ+F1wtaqU"
                Object = ET.SubElement(Signature , "ds:Object"  )
                QualifyingProperties = ET.SubElement(Object , "xades:QualifyingProperties"  )
                QualifyingProperties.set("Target" , "signature")
                QualifyingProperties.set("xmlns:xades" , "http://uri.etsi.org/01903/v1.3.2#")
                SignedProperties = ET.SubElement(QualifyingProperties , "xades:SignedProperties"  )
                SignedProperties.set("Id" , "xadesSignedProperties")
                SignedSignatureProperties = ET.SubElement(SignedProperties , "xades:SignedSignatureProperties"  )
                SigningTime = ET.SubElement(SignedSignatureProperties , "xades:SigningTime"  )
                SigningTime.text = "2024-01-24T11:36:34Z"
                SigningCertificate = ET.SubElement(SignedSignatureProperties , "xades:SigningCertificate"  )
                Cert = ET.SubElement(SigningCertificate , "xades:Cert"  )
                CertDigest = ET.SubElement(Cert , "xades:CertDigest"  )
                Digest_Method2 = ET.SubElement(CertDigest , "ds:DigestMethod"  )
                Digest_Value2 = ET.SubElement(CertDigest , "ds:DigestValue"  )
                Digest_Method2.set("Algorithm" , "http://www.w3.org/2001/04/xmlenc#sha256")
                Digest_Value2.text = "YTJkM2JhYTcwZTBhZTAxOGYwODMyNzY3NTdkZDM3YzhjY2IxOTIyZDZhM2RlZGJiMGY0NDUzZWJhYWI4MDhmYg=="
                IssuerSerial = ET.SubElement(Cert , "xades:IssuerSerial"  )
                X509IssuerName = ET.SubElement(IssuerSerial , "ds:X509IssuerName"  )
                X509SerialNumber = ET.SubElement(IssuerSerial , "ds:X509SerialNumber"  )
                if not is_b2c:
                    X509IssuerName.text = "CN=PRZEINVOICESCA4-CA, DC=extgazt, DC=gov, DC=local"
                else:
                    X509IssuerName.text  =  'CN=TSZEINVOICE-SubCA-1, DC=extgazt, DC=gov, DC=local'
                # X509IssuerName.text = "CN=TSZEINVOICE-SubCA-1, DC=extgazt, DC=gov, DC=local"
                X509SerialNumber.text = "2475382886904809774818644480820936050208702411"
                return invoice
            except Exception as e:
                    frappe.throw("error in xml tags formation:  "+ str(e) )

# print(generate_xml_tags().__dict__)

# inv = invoice_Typecode_Compliance(generate_xml_tags())
# cmp=company_Data(generate_xml_tags())
# cst = customer_Data(cmp)
# inv_det = salesinvoice_data(cst)
# in_stan = invoice_Typecode_Standard(inv_det)
# in_smp = invoice_Typecode_Simplified(in_stan)
# in_p = delivery_And_PaymentMeans(in_smp)
# in_p_c = delivery_And_PaymentMeans_for_Compliance(in_p)
# doc_ref = doc_Reference(inv)

# tree = ET.ElementTree(in_p_c)


# tree.write("invoice.xml", encoding="utf-8", xml_declaration=True)
