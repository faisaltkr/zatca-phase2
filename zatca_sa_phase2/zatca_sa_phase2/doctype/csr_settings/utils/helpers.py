import datetime
import uuid
import os
import frappe
import json
from zatca_sa_phase2.zatca_sa_phase2.doctype.csr_settings.utils.get_values import get_additial_ids_zatca

def has_all_keys(dictionary, key_list):
    return all(key in dictionary for key in key_list)

@frappe.whitelist()
def helpers(name):
    current_dict = json.loads(name)
    print(current_dict,"dfdf")
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
                        # "select_invoice_type",
                    ]
    if not has_all_keys(current_dict, required_fields):
        return{
            "message":"Please add all mandatory fields."  
    
        } 
    get_additional_doc = get_additial_ids_zatca()
    print(get_additional_doc,"sdfjkhdkjfghkjdfhkjhdfjkgh")
    if not get_additional_doc:
        return {
            "message":"Additional Ids required."
        }
    # if all([get_additional_doc[0].get('id_name',False),get_additional_doc[0].get('type_code',False),get_additional_doc[0].get('valueid_number',False)]):
    #     return {
    #         "message":"all fields in the Additional Ids is required."
    #     }
                                                                                

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
        from .generate_keys import update_frappe_doc
        from .issuer import generate_issue_details
        status,p_path,pu_path,csr_path = generatekeys(current_dict.get('name'),config_dict,current_dict.get('business_unit'))

        with open(p_path, "r") as f:
            private_key = f.read()

            update_frappe_doc(current_dict.get('name'),'private_key',private_key)

        with open(pu_path, "r") as f:
            public_key = f.read()

            update_frappe_doc(current_dict.get('name'),'public_key',public_key)

        with open(csr_path,"r") as f:
            csr = f.read()
            update_frappe_doc(current_dict.get('name'),'csr',csr)

        issuer_name , s_no =  generate_issue_details(
        country=current_dict.get('country_code'),
        state=current_dict.get('country'),
        locality=current_dict.get('city'),
        on=current_dict.get('company_name'),
        cn=current_dict.get('common_name'),

        )
        update_frappe_doc(current_dict.get('name'),'issuer_name',issuer_name)
        update_frappe_doc(current_dict.get('name'),'issuer_serial_number',s_no)

        return {
            "message":"CSR Token Generated Successfully!",
            "key" : private_key,
            "public_key":public_key,
            "csr":csr,
            "issuer_name":issuer_name,
            "s_no":s_no
        }

    except Exception as e:
        return "failed to generate csr "+ str(e)
    



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
            "csid":csid[1],
            "csr":csid[3],
            'secret':csid[0],
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

