import base64
import subprocess
import os
from .config import get_config
import requests
import base64
from .helpers import get_fatoora_base_url
import frappe

openssl_dir = "/usr/bin"


def generatekeys(path,config_dict,name):
    # Generate private key
        name = f"keys_{name}"
        os.makedirs(name, exist_ok=True) 
        subprocess.run([os.path.join(openssl_dir, 'openssl'), 'ecparam',
                        '-name', 'secp256k1', '-genkey', '-noout', '-out', f'{name}/{path}_PrivateKey.pem'])

        # Generate public key from private key
        subprocess.run([os.path.join(openssl_dir, 'openssl'), 'ec',
                        '-in', f'{name}/{path}_PrivateKey.pem', '-pubout', '-out', f'{name}/{path}_publickey.pem'])
        
        public_key_path = f'{name}/{path}_publickey.pem'

        # Generate CSR (Configuration file assumed to be present)
        subprocess.run([os.path.join(openssl_dir, 'openssl'), 'req', '-new', '-sha256', '-key', f'{name}/{path}_PrivateKey.pem', '-extensions', 'v3_req',
                        '-config', get_config(config_dict=config_dict), '-out', f'{name}/{path}_.csr'])
    
        private_key_path = f'{name}/{path}_PrivateKey.pem'
        return True , private_key_path, public_key_path


def get_csid(unit,name,otp):
    try:
        with open(f"keys_{unit}/{name}_.csr", "r") as f:
            csr_contents = f.read()
    except Exception as e:
        print(str(e))

    csr = base64.b64encode(csr_contents.encode("utf-8")).decode("utf-8")
    headers = {
        'accept': 'application/json',
        'OTP': str(otp),
        'Accept-Version': 'V2',
        'Content-Type': 'application/json',
    }

    json_data = {
        'csr': '000',
    }
    json_data['csr'] = csr
    response = requests.post(
        get_fatoora_base_url(current_env="sandbox")+'compliance',
        headers=headers,
        json=json_data,
    )
    if response.status_code == 200:
        csid = response.json()
        binarySecurityToken = response.json()['binarySecurityToken']
        decoded_token = base64.b64decode(binarySecurityToken).decode('utf-8')
        secret = response.json()['secret']
        update_frappe_doc(name,'compliance_request_id', response.json()['requestID'])

        with open(f'keys_{unit}/{name}_certificate.txt', 'w') as f:
            f.write(decoded_token)
            # update_frappe_doc(name,'csr',decoded_token)
        print('certificate.txt'+' saved')

        with open(f'keys_{unit}/{name}_binarySecurityToken.txt', 'w') as f:
            f.write(binarySecurityToken)
            update_frappe_doc(name,'csid',decoded_token)
            update_frappe_doc(name,'csr',csr)


        print('binarySecurityToken.txt'+' saved')

        with open(f'keys_{unit}/{name}_secret.txt', 'w') as f:
            f.write(secret)
            update_frappe_doc(name,'secret',secret)

        print('secret.txt'+' saved')
    else:
        print(
            f"Error: received {response.status_code} status code with message {response.json()['dispositionMessage']}")

    return secret,decoded_token,response.json()['requestID'],csr

def update_frappe_doc(docname, fieldname, value):
    try:
        # Get the document
        doctype = 'CSR Settings'
        print("hhhhhhhhhh")
        doc = frappe.get_doc(doctype, docname)
        
        # Set the field value
        doc.set(fieldname, value)
        
        # Save the document
        doc.save()
        
        # Commit the transaction
        frappe.db.commit()
        
        return True
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), 'update_frappe_doc Error')
        return False
