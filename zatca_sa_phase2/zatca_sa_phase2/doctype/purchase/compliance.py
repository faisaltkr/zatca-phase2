import frappe
import json
import base64
import requests


def xml_base64_Decode(signed_xmlfile_name):
                    try:
                        with open(signed_xmlfile_name, "r") as file:
                                        xml = file.read().lstrip()
                                        base64_encoded = base64.b64encode(xml.encode("utf-8"))
                                        base64_decoded = base64_encoded.decode("utf-8")
                                        return base64_decoded
                    except Exception as e:
                        frappe.msgprint("Error in xml base64:  " + str(e) )

def get_csid_for_company(basic_auth_data, company_name):
                    try:     
                        for entry in basic_auth_data.get("data", []):
                            if entry.get("company") == company_name:
                                return entry.get("csid")
                        return None
                    except Exception as e:
                        frappe.throw("Error in getting csid for company:  " + str(e) )
                        
def get_API_url(base_url):
                try:
                    settings =  frappe.get_doc('Zatca ERPgulf Setting')
                    if settings.select == "Sandbox":
                        url = settings.sandbox_url + base_url
                    elif settings.select == "Simulation":
                        url = settings.simulation_url + base_url
                    else:
                        url = settings.production_url + base_url
                    return url 
                except Exception as e:
                    frappe.throw(" getting url failed"+ str(e) ) 

def compliance_api_call(uuid1,encoded_hash,signed_xmlfile_name):
                try:
                    settings = frappe.get_doc('Zatca ERPgulf Setting')
                    payload = json.dumps({
                        "invoiceHash": encoded_hash,
                        "uuid": uuid1,
                        "invoice": xml_base64_Decode(signed_xmlfile_name) })
                    company = settings.company
                    company_name = frappe.db.get_value("Company", company, "abbr")
                    basic_auth = settings.get("basic_auth", "{}")
                    # frappe.msgprint(basic_auth)
                    basic_auth_data = json.loads(basic_auth)
                    csid = get_csid_for_company(basic_auth_data, company_name)
                    # frappe.msgprint(csid)
                    if csid:
                        headers = {
                            'accept': 'application/json',
                            'Accept-Language': 'en',
                            'Accept-Version': 'V2',
                            'Authorization': "Basic " + csid,
                            'Content-Type': 'application/json'
                        }
                    else:
                        frappe.throw("CSID for company {} not found".format(company_name))
                    try:
                        # frappe.throw("inside compliance api call2")
                        response = requests.request("POST", url=get_API_url(base_url="compliance/invoices"), headers=headers, data=payload)
                        frappe.msgprint(response.text)

                        # return response.text

                        if response.status_code != 200:
                            frappe.throw("Error in complaince: " + str(response.text))    
                    
                    except Exception as e:
                        frappe.msgprint(str(e))
                        return "error in compliance", "NOT ACCEPTED"
                except Exception as e:
                    frappe.throw("ERROR in clearance invoice ,zatca validation:  " + str(e) )