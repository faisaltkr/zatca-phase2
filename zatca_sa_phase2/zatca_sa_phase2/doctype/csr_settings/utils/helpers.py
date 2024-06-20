import datetime
import uuid
import os
import frappe
import json
from .generate_keys import update_frappe_doc

def has_all_keys(dictionary, key_list):
    return all(key in dictionary for key in key_list)

@frappe.whitelist()
def helpers(name):
    current_dict = json.loads(name)
    required_fields = [
                        "name",
                        "company_name",
                        "business_unit",
                        "egs_unit_serial",
                        "company_category",
                        "country",
                        "country_code",
                        "common_name",
                        "currency_code",
                        "street",
                        "building_number",
                        "city",
                        "district",
                        "postal_code",
                        "business_transaction_type",
                        "company_namearabic",
                        "vat_registration_number",
                        "select_environment",
                        "select_invoice_type",
                    ]
    if not has_all_keys(current_dict, required_fields):
        return "Please add all mandatory fields."  
    
    config_dict = {
    "oid_section": "OIDS",
    "OIDS": {
        "certificateTemplateName": "1.3.6.1.4.1.311.20.2"
    },
    "req": {
        "default_bits": "2048",
        "emailAddress": "zatca@example.com",
        "req_extensions": "v3_req",
        "x509_extensions": "v3_Ca",
        "prompt": "no",
        "default_md": "sha256",
        "req_extensions": "req_ext",
        "distinguished_name": "req_distinguished_name"
    },
    "req_distinguished_name": {
        "C": current_dict.get('country_code'),
        "OU": current_dict.get('business_unit'),
        "O": current_dict.get('company_name'),
        "CN": current_dict.get('common_name')
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
        "SN": current_dict.get('egs_unit_serial'), #egs
        "UID": current_dict.get('vat_registration_number'), #vat registration number
        "title": "1100", # invoice type
        "registeredAddress":  current_dict.get('city'),
        "businessCategory":  current_dict.get('company_category')
        }
    }   

    print(config_dict)

    try:
        from .generate_keys import generatekeys
        keys,p_path = generatekeys(current_dict.get('name'),config_dict,current_dict.get('business_unit'))

        with open(p_path, "r") as f:
            private_key = f.read()
            update_frappe_doc(name,'csid',decoded_token)



        return "CSR Token Generated Successfully!"

    except Exception as e:
        return "failed to generate csr "+ str(e)
    
    return config_dict



@frappe.whitelist()
def csid(dict):
    current_dict = json.loads(dict)
    from .generate_keys import get_csid
    # name = 
    try:
        env = current_dict.get('select_environment')
        csid = get_csid(current_dict.get('business_unit'),current_dict.get('name'),current_dict.get('enter_otp'))

    
        return {
            'message':"CSID generated sucessfully",
            "compliance_request_id":csid[2],
            "csr":csid[1],
            "private_key":csid[0]
        }

    except Exception as e:
        return "failed to generate csid "+ str(e)

def get_uuid():
    """
    return uuid string
    """
    return str(uuid.uuid4())


def get_date():
    """
    return date string
    """
    return str(datetime.datetime.utcnow(
    ).strftime("%Y-%m-%d"))


def get_time():
    """
    return time string
    """
    return str(datetime.datetime.utcnow().strftime("%H:%M:%S"))


def get_home_dir():
    """
    return home dir
    """
    return os.path.expanduser("~")


def get_fatoora_base_url(current_env="sanbox"):
    """
    get current base url
    """
    current_env=current_env.lower()
    if current_env == "sandbox":
        return 'https://gw-fatoora.zatca.gov.sa/e-invoicing/developer-portal/'
    elif current_env == "simulation":
        return "https://gw-fatoora.zatca.gov.sa/e-invoicing/simulation/"

    return "https://gw-fatoora.zatca.gov.sa/e-invoicing/core/"

