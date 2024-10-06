
import frappe
import json
import requests
from .generate_keys import update_frappe_doc

@frappe.whitelist()
def generate_pcsid(data):
    data = json.loads(data)
    name = data.get('name')
    pcsid_resp = generate(data, name)
    if not pcsid_resp:
        return {
                "message":"production csid generated",
                "success": 'false',
                "token": pcsid_resp
            }
    return {
        "message":"production csid generated",
        "success": 'true'
    }

def generate(data, name):
    tk = "VFVsSlEwZHFRME5CWWl0blFYZEpRa0ZuU1VkQldrWlhiMlkzWjAxQmIwZERRM0ZIVTAwME9VSkJUVU5OUWxWNFJYcEJVa0puVGxaQ1FVMU5RMjFXU21KdVduWmhWMDV3WW0xamQwaG9ZMDVOYWxGM1QwUkZNVTFVVlhsTmFrVXpWMmhqVGsxcWEzZFBSRVV3VFdwRmQwMUVRWGRYYWtKcFRWRnpkME5SV1VSV1VWRkhSWGRLVkZGVVJWZE5RbEZIUVRGVlJVTjNkMDVWYld3MVdWZFNiMGxGU25sWlZ6VnFZVVJGVkUxQ1JVZEJNVlZGUTJkM1MxSllhSFppYlZWblZrZFdhbUZFUlcxTlExRkhRVEZWUlVGM2QyUldSazVWVEZSbk5FNXFVWHBOVkVVd1RsTXdlazlVYXpWUFZHczFUMVJyTlUxRVFYZE5SRTEzVm1wQlVVSm5ZM0ZvYTJwUFVGRkpRa0puVlhKblVWRkJRMmRPUTBGQlUzZEZSR2xSUnpnNGNEWnBTWG8wUkdwS2EwUlZVbXhyU2tKclppOURVbXh1WmtSWFJEbENNbTFFYWtrclNqUmpRMWhDYUN0WFEycFVLMU5qUTI1NGQwMWxjVXRYTkZKUFkyZDFVeTlvU1U4MlZsRkNXV1Z2TkVkM1RVbEhkRTFCZDBkQk1WVmtSWGRGUWk5M1VVTk5RVUYzWjFwM1IwRXhWV1JGVVZOQ2JFUkRRbXRoVTBKcWFrTkNhWHBGTjAxRWEwZEJNVlZGUWtGM2VVMVRNVlZWTVZJNFRXa3hWVlV4VWpoTmVURnNXa1JKZVZwcVJtdFBRekZzVG0xRmVVeFVSWGhOVkdkMFQxZEpNVTlETVd0UFYwVTBXbXBGZUZwVVVUQk9WMWw0U0hwQlpFSm5iMHByYVdGS2F5OUpjMXBCUlVKRVFUaDZUMVJyTlU5VWF6VlBWR3MxVFVSQmQwMUVUWGhFVkVGTVFtZE9Wa0pCZDAxQ1JFVjRUVVJCZUVSNlFVNUNaMDVXUWtKdlRVSnNTbkJsVjBacllVUkZURTFCYTBkQk1WVkZSSGQzUTFOV1VYZERaMWxKUzI5YVNYcHFNRVZCZDBsRVUxRkJkMUpuU1doQlRVSnpNR0pUTTJaTGJVZGtiMm9yYkN0NFVtdFdXbFZqY0RGUmRFcE1NMFJxZGtjM1FrOVlUbWw0UjBGcFJVRnpkVEZwT1U1MVJGVmpiMkptWW5GeWFrdFpPWGwzU1RsWlQzaDNZVEo0UVdaMmQwUk9lV05xUkhORlBRPT06dThzcGh1TWJWbjJYMFRYSFVvSnlxUG1PK25jRG54UGdDeFVjMVlCdVNPZz0="
    headers = {
        'accept': 'application/json',
        'Accept-Language': 'en',
        'Accept-Version': 'V2',
        'Authorization': "Basic " + tk,
        'Content-Type': 'application/json'
    }

    payload = {
    "compliance_request_id": data.get('compliance_request_id')
    }
    env = data.get('select_environment')

    current_env = get_fatoora_base_url(current_env=env)

    url = f"{current_env}production/csids"


    response = requests.post(url, json=payload, headers=headers)

# Check the response status and content
    if response.status_code == 200:
        print("Success:", response.json()) 
        update_frappe_doc(name,'production_csid',response.json()['binarySecurityToken'])
        return response.json()['binarySecurityToken'] # Assuming the response is JSON
    else:
        print("Error:", response.status_code, response.text)
        return False


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

