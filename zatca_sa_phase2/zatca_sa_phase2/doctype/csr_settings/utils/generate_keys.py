import base64
import subprocess
import os
from .config import get_config
import requests
import base64
from .helpers import get_fatoora_base_url

openssl_dir = "/usr/bin"


config_dict = {
    "oid_section": "OIDS",
    "OIDS": {
        "certificateTemplateName": "1.3.6.1.4.1.311.20.2"
    },
    "req": {
        "default_bits": "2048",
        "emailAddress": "myemail@gmail.com",
        "req_extensions": "v3_req",
        "x509_extensions": "v3_Ca",
        "prompt": "no",
        "default_md": "sha256",
        "req_extensions": "req_ext",
        "distinguished_name": "req_distinguished_name"
    },
    "req_distinguished_name": {
        "C": "SA",
        "OU": "example co.",
        "O": "Zatca",
        "CN": "127.0.0.1"
    },
    "v3_req": {
        "basicConstraints": "CA:FALSE",
        "keyUsage": "nonRepudiation, digitalSignature, keyEncipherment"
    },
    "req_ext": {
        "certificateTemplateName": "ASN1:PRINTABLESTRING:PREZATCA-code-Signing",
        "subjectAltName": "dirName:alt_names"
    },
    "alt_names": {
        "SN": "1-Device|2-234|3-exampl",
        "UID": "310094010300003",
        "title": "1000",
        "registeredAddress": "Riyadh",
        "businessCategory": "construction"
    }
}


def generatekeys(config_dict=config_dict):
    # Generate private key
    # Generate private key
    private_key_process = subprocess.run([os.path.join(openssl_dir, 'openssl'), 'ecparam',
                                      '-name', 'secp256k1', '-genkey', '-noout', '-text'], capture_output=True, text=True)

    # Extract private key from the process output
    private_key = private_key_process.stdout

    # Generate public key from private key
    public_key_process = subprocess.run([os.path.join(openssl_dir, 'openssl'), 'ec',
                                     '-pubout', '-text'], input=private_key, capture_output=True, text=True)

    # Extract public key from the process output
    public_key = public_key_process.stdout

    # Generate CSR (Configuration file assumed to be present)
    csr_process = subprocess.run([os.path.join(openssl_dir, 'openssl'), 'req', '-new', '-sha256', '-key', 'stdin',
                              '-extensions', 'v3_req', '-config', get_config(config_dict=config_dict)], input=private_key, capture_output=True, text=True)

    # Extract CSR from the process output
    csr = csr_process.stdout


    


def get_csid():
    try:
        with open("taxpayer.csr", "r") as f:
            csr_contents = f.read()
    except Exception as e:
        print(str(e))

    csr = base64.b64encode(csr_contents.encode("utf-8")).decode("utf-8")

    headers = {
        'accept': 'application/json',
        'OTP': '123345',
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
        print(csid)
        binarySecurityToken = response.json()['binarySecurityToken']
        decoded_token = base64.b64decode(binarySecurityToken).decode('utf-8')
        secret = response.json()['secret']

        with open('certificate.txt', 'w') as f:
            f.write(decoded_token)
        print('certificate.txt'+' saved')

        with open('binarySecurityToken.txt', 'w') as f:
            f.write(binarySecurityToken)
        print('binarySecurityToken.txt'+' saved')

        with open('secret.txt', 'w') as f:
            f.write(secret)
        print('secret.txt'+' saved')
    else:
        print(
            f"Error: received {response.status_code} status code with message {response.json()['dispositionMessage']}")
