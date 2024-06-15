import hashlib
import base64 

def getInvoiceHash(canonicalized_xml):
        """
        hash invoice data
        """
        try:
            hash_object = hashlib.sha256(canonicalized_xml.encode())
            hash_hex = hash_object.hexdigest()
            hash_base64 = base64.b64encode(bytes.fromhex(hash_hex)).decode('utf-8')
            return hash_hex,hash_base64
        except Exception as e:
            print(str(e))
