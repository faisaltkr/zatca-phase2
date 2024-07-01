import frappe
import json
import base64
import requests



def get_production_csid_for_company(basic_auth_production_data, company_name):
                    try:  
                        for entry in basic_auth_production_data.get("companies", []):
                            if entry.get("company") == company_name:
                                return entry.get("production_csid")
                        return None
                    except Exception as e:
                            frappe.throw("Error in getting production csid of company for api   " + str(e)) 

def xml_base64_Decode(signed_xmlfile_name):
                    try:
                        with open(signed_xmlfile_name, "r") as file:
                                        xml = file.read().lstrip()
                                        base64_encoded = base64.b64encode(xml.encode("utf-8"))
                                        base64_decoded = base64_encoded.decode("utf-8")
                                        return base64_decoded
                    except Exception as e:
                        frappe.msgprint("Error in xml base64:  " + str(e) )

def get_API_url(url):
                try:
                    key = frappe.get_all('CSR Settings', fields=['select_environment'])
                    env =  key[0]['select_environment']                    
                    if env == "Sandbox":
                        url = f"https://gw-fatoora.zatca.gov.sa/e-invoicing/developer-portal/{url}"
                    elif env == "Simulation":
                        url = f"https://gw-fatoora.zatca.gov.sa/e-invoicing/simulation/{url}"
                    else:
                        url = f"https://gw-fatoora.zatca.gov.sa/e-invoicing/core/{url}"
                    print(url,"kkkkkk")
                    return url 
                except Exception as e:
                    frappe.throw(" getting url failed"+ str(e) )

def update_json_data_pih(existing_data, company_name, pih):
                    try:
                        company_exists = False
                        for entry in existing_data["data"]:
                            if entry["company"] == company_name:
                                # Update the PIH for the existing company
                                entry["pih"] = pih
                                company_exists = True
                                break
                        if not company_exists:
                            existing_data["data"].append({
                                "company": company_name,
                                "pih": pih
                            })
                        return existing_data
                    except Exception as e:
                                        frappe.throw("Error in json data of pih  " + str(e)) 

def success_Log(response,uuid1,invoice_number):
                    try:
                        current_time = frappe.utils.now()
                        frappe.get_doc({
                            "doctype": "Zatca ERPgulf Success Log",
                            "title": "Zatca invoice call done successfully",
                            "message": "This message by Zatca Compliance",
                            "uuid": uuid1,
                            "invoice_number": invoice_number,
                            "time": current_time,
                            "zatca_response": response  
                            
                        }).insert(ignore_permissions=True)
                    except Exception as e:
                        frappe.throw("Error in success log  " + str(e))

def error_Log():
                    try:
                        frappe.log_error(title='Zatca invoice call failed in clearance status',message=frappe.get_traceback())
                    except Exception as e:
                        frappe.throw("Error in error log  " + str(e))   


def reporting_API(uuid1,encoded_hash,signed_xmlfile_name,invoice_number,sales_invoice_doc):
                    try:
                        # settings = frappe.get_doc('Zatca ERPgulf Setting')
                        # company = settings.company
                        # company_name = frappe.db.get_value("Company", company, "abbr")

                        key = frappe.get_all('CSR Settings', fields=['company_name','csid','secret'])
                        company_name =  key[0]['company_name']   
                        payload = json.dumps({
                        "invoiceHash": encoded_hash,
                        "uuid": uuid1,
                        "invoice": xml_base64_Decode(signed_xmlfile_name),
                        })
                        # basic_auth_production = settings.get("basic_auth_production", "{}")
                        # basic_auth_production_data = json.loads(basic_auth_production)
                        # production_csid = get_production_csid_for_company(basic_auth_production_data, company_name)
                        production_csid = 'VFVsSlJETnFRME5CTkZOblFYZEpRa0ZuU1ZSRlVVRkJUMEZRUmprd1FXcHpMM2hqV0hkQlFrRkJRVFJCZWtGTFFtZG5jV2hyYWs5UVVWRkVRV3BDYVUxU1ZYZEZkMWxMUTFwSmJXbGFVSGxNUjFGQ1IxSlpSbUpIT1dwWlYzZDRSWHBCVWtKbmIwcHJhV0ZLYXk5SmMxcEJSVnBHWjA1dVlqTlplRVo2UVZaQ1oyOUthMmxoU21zdlNYTmFRVVZhUm1ka2JHVklVbTVaV0hBd1RWSnpkMGRSV1VSV1VWRkVSWGhLVVZWc2NFWlRWVFZYVkRCc1JGSldUa1JSVkZGMFVUQkZkMGhvWTA1TmFsRjNUVlJGZUUxRWEzaFBWRTEzVjJoalRrMXFhM2ROVkVFMVRVUnJlRTlVVFhkWGFrSXhUVkZ6ZDBOUldVUldVVkZIUlhkS1ZGRlVSVzFOUTFGSFFURlZSVU5vVFdSVVYwWTBZVmN4TVdKVFFsUmpSMVpzV2tOQ1ZWcFhUbTlKUms0eFkwaENjMlZUUWsxV1JWRjRSbXBCVlVKblRsWkNRWE5VUkZaS2NHVlhSbXRoUTBKRFkyMUdkVmt5WjNoS2FrRnJRbWRPVmtKQlRWUklWbEpVVmtNd05FOUVXVEJOZWtWNFRrUlZkRTE2YXpWUFZHczFUMVJyTlU5VVFYZE5SRUY2VFVaWmQwVkJXVWhMYjFwSmVtb3dRMEZSV1VaTE5FVkZRVUZ2UkZGblFVVnZWME5MWVRCVFlUbEdTVVZ5VkU5Mk1IVkJhME14VmtsTFdIaFZPVzVRY0hneWRteG1OSGxvVFdWcWVUaGpNREpZU21Kc1JIRTNkRkI1Wkc4NGJYRXdZV2hQVFcxT2J6aG5kMjVwTjFoME1VdFVPVlZsUzA5RFFXZGpkMmRuU1VSTlNVZDBRbWRPVmtoU1JVVm5ZVlYzWjJGTGEyZGFPSGRuV25kNFQzcEJOVUpuVGxaQ1FWRk5UV3BGZEZaR1RsVm1SRWwwVmtaT1ZXWkVUWFJhVjFGNVRXMVplRnBFWjNSYVZGcG9UV2t3ZUUxVVJUUk1WR3hwVGxSbmRGcEViR2hQUjFsNFRWZFZNRTVFVm0xTlVqaDNTRkZaUzBOYVNXMXBXbEI1VEVkUlFrRlJkMUJOZW1zMVQxUnJOVTlVYXpWUFZFRjNUVVJCZWsxUk1IZERkMWxFVmxGUlRVUkJVWGhOVkVGM1RWSkZkMFIzV1VSV1VWRmhSRUZvVTFWc1NrVk5hbXQ1VDFSRllVMUNaMGRCTVZWRlJIZDNVbFV6Vm5kalIzZzFTVWRHYW1SSGJESmhXRkp3V2xoTmQwaFJXVVJXVWpCUFFrSlpSVVpGV0N0WmRtMXRkRzVaYjBSbU9VSkhZa3R2TjI5alZFdFpTekZOUWpoSFFURlZaRWwzVVZsTlFtRkJSa3AyUzNGeFRIUnRjWGR6YTBsR2VsWjJjRkF5VUhoVUt6bE9iazFJYzBkRFEzTkhRVkZWUmtKM1JVSkNSemgzWWxSQ2NrSm5aM0pDWjBWR1FsRmpkMEZ2V21aaFNGSXdZMFJ2ZGt3eVJuQlpWRkYxWlcxR01Ga3lSWFZhTWpreVRHNU9hRXd3VG14amJsSkdZbTVLZG1KSGQzWlZSa3BoVWxWc2RXUnRPWEJaTWxaVVVUQkZNRXh0VmpSa1IyUm9aVzVSZFZveU9USk1iWGgyV1RKR2MxZ3hRbE5YYTFaS1ZHeGFVRk5WVGtaVk1FNUNUa014UkZGVFozaExVelZxWTI1UmQwUm5XVVJXVWpCUVFWRklMMEpCVVVSQloyVkJUVVIzUjBOVGMwZEJVVkZDWjJwalZrSjNVWFpOUXpCSFNsTnpSMEZSVVVKbmFtTldRMGxIUjNGQ01rVXdVSE5UYUhVeVpFcEpaazhyZUc1VWQwWldiV2d2Y1d4YVdWaGFhRVEwUTBGWFVVTkJVa2wzU0ZGWlJGWlNNR3hDUWxsM1JrRlpTVXQzV1VKQ1VWVklRWGROUjBORGMwZEJVVlZHUW5kTlEwMURZMGREVTNOSFFWRlJRbWRxWTFaRFoxRmhUVUpuZDBObldVbExkMWxDUWxGVlNFRjNUWGREWjFsSlMzZFpRa0pSVlVoQmQwbDNRMmRaU1V0dldrbDZhakJGUVhkSlJGTkJRWGRTVVVsb1FVeEZMMmxqYUcxdVYxaERWVXRWWW1OaE0zbGphVGh2Y1hkaFRIWkdaRWhXYWxGeWRtVkpPWFZ4UVdKQmFVRTVhRU0wVFRocVowMUNRVVJRVTNwdFpESjFhVkJLUVRablMxSXpURVV3TTFVM05XVnhZa012Y2xoQlBUMD06Q2tZc0VYZlY4YzFnRkhBdEZXb1p2NzNwR012aC9ReW80THpLTTJoLzhIZz0='

                        if production_csid:
                            headers = {
                                'accept': 'application/json',
                                    'accept-language': 'en',
                                    'Clearance-Status': '0',
                                    'Accept-Version': 'V2',
                                    # 'Authorization': "Basic VFVsSlJESjZRME5CTkVOblFYZEpRa0ZuU1ZSaWQwRkJaSEZFYlVsb2NYTnFjRzAxUTNkQlFrRkJRakp2UkVGTFFtZG5jV2hyYWs5UVVWRkVRV3BDYWsxU1ZYZEZkMWxMUTFwSmJXbGFVSGxNUjFGQ1IxSlpSbUpIT1dwWlYzZDRSWHBCVWtKbmIwcHJhV0ZLYXk5SmMxcEJSVnBHWjA1dVlqTlplRVo2UVZaQ1oyOUthMmxoU21zdlNYTmFRVVZhUm1ka2JHVklVbTVaV0hBd1RWSjNkMGRuV1VSV1VWRkVSWGhPVlZVeGNFWlRWVFZYVkRCc1JGSlRNVlJrVjBwRVVWTXdlRTFDTkZoRVZFbDVUVVJOZVU5RVJURk9SRmw2VFd4dldFUlVTWGxOUkUxNlRVUkZNVTVFV1hwTmJHOTNWRlJGVEUxQmEwZEJNVlZGUW1oTlExVXdSWGhFYWtGTlFtZE9Wa0pCYjFSQ1ZYQm9ZMjFzZVUxU2IzZEhRVmxFVmxGUlRFVjRSa3RhVjFKcldWZG5aMUZ1U21oaWJVNXZUVlJKZWs1RVJWTk5Ra0ZIUVRGVlJVRjRUVXBOVkVrelRHcEJkVTFETkhoTlJsbDNSVUZaU0V0dldrbDZhakJEUVZGWlJrczBSVVZCUVc5RVVXZEJSVVF2ZDJJeWJHaENka0pKUXpoRGJtNWFkbTkxYnpaUGVsSjViWGx0VlRsT1YxSm9TWGxoVFdoSFVrVkNRMFZhUWpSRlFWWnlRblZXTW5oWWFYaFpOSEZDV1dZNVpHUmxjbnByVnpsRWQyUnZNMGxzU0dkeFQwTkJhVzkzWjJkSmJVMUpSMHhDWjA1V1NGSkZSV2RaVFhkbldVTnJabXBDT0UxU2QzZEhaMWxFVmxGUlJVUkNUWGxOYWtsNVRXcE5lVTVFVVRCTmVsRjZZVzFhYlU1RVRYbE5VamgzU0ZGWlMwTmFTVzFwV2xCNVRFZFJRa0ZSZDFCTmVrVjNUVlJqTVUxNmF6Tk9SRUYzVFVSQmVrMVJNSGREZDFsRVZsRlJUVVJCVVhoTlJFVjRUVkpGZDBSM1dVUldVVkZoUkVGb1ZGbFhNWGRpUjFWblVsUkZXazFDWTBkQk1WVkZSSGQzVVZVeVJuUmpSM2hzU1VWS01XTXpUbkJpYlZaNlkzcEJaRUpuVGxaSVVUUkZSbWRSVldoWFkzTmlZa3BvYWtRMVdsZFBhM2RDU1V4REszZE9WbVpMV1hkSWQxbEVWbEl3YWtKQ1ozZEdiMEZWWkcxRFRTdDNZV2R5UjJSWVRsb3pVRzF4ZVc1TE5Xc3hkRk00ZDFSbldVUldVakJtUWtWamQxSlVRa1J2UlVkblVEUlpPV0ZJVWpCalJHOTJURE5TZW1SSFRubGlRelUyV1ZoU2FsbFROVzVpTTFsMVl6SkZkbEV5Vm5sa1JWWjFZMjA1YzJKRE9WVlZNWEJHVTFVMVYxUXdiRVJTVXpGVVpGZEtSRkZUTUhoTWJVNTVZa1JEUW5KUldVbExkMWxDUWxGVlNFRlJSVVZuWVVGM1oxb3dkMkpuV1VsTGQxbENRbEZWU0UxQlIwZFpiV2d3WkVoQk5reDVPVEJqTTFKcVkyMTNkV1Z0UmpCWk1rVjFXakk1TWt4dVRtaE1NRTVzWTI1U1JtSnVTblppUjNkMlZrWk9ZVkpYYkhWa2JUbHdXVEpXVkZFd1JYaE1iVlkwWkVka2FHVnVVWFZhTWpreVRHMTRkbGt5Um5OWU1WSlVWMnRXU2xSc1dsQlRWVTVHVEZaT01WbHJUa0pNVkVWdlRWTnJkVmt6U2pCTlEzTkhRME56UjBGUlZVWkNla0ZDYUdnNWIyUklVbmRQYVRoMlpFaE9NRmt6U25OTWJuQm9aRWRPYUV4dFpIWmthVFY2V1ZNNWRsa3pUbmROUVRSSFFURlZaRVIzUlVJdmQxRkZRWGRKU0dkRVFXUkNaMDVXU0ZOVlJVWnFRVlZDWjJkeVFtZEZSa0pSWTBSQloxbEpTM2RaUWtKUlZVaEJkMDEzU25kWlNrdDNXVUpDUVVkRFRuaFZTMEpDYjNkSFJFRkxRbWRuY2tKblJVWkNVV05FUVdwQlMwSm5aM0pDWjBWR1FsRmpSRUY2UVV0Q1oyZHhhR3RxVDFCUlVVUkJaMDVLUVVSQ1IwRnBSVUY1VG1oNVkxRXpZazVzVEVaa1QxQnNjVmxVTmxKV1VWUlhaMjVMTVVkb01FNUlaR05UV1RSUVprTXdRMGxSUTFOQmRHaFlkblkzZEdWMFZVdzJPVmRxY0RoQ2VHNU1URTEzWlhKNFdtaENibVYzYnk5blJqTkZTa0U5UFE9PTpmOVlSaG9wTi9HN3gwVEVDT1k2bktTQ0hMTllsYjVyaUFIU0ZQSUNvNHF3PQ==" ,
                                    # 'Authorization': "Basic VFVsSlJESjZRME5CTkVOblFYZEpRa0ZuU1ZSaWQwRkJaSEZFYlVsb2NYTnFjRzAxUTNkQlFrRkJRakp2UkVGTFFtZG5jV2hyYWs5UVVWRkVRV3BDYWsxU1ZYZEZkMWxMUTFwSmJXbGFVSGxNUjFGQ1IxSlpSbUpIT1dwWlYzZDRSWHBCVWtKbmIwcHJhV0ZLYXk5SmMxcEJSVnBHWjA1dVlqTlplRVo2UVZaQ1oyOUthMmxoU21zdlNYTmFRVVZhUm1ka2JHVklVbTVaV0hBd1RWSjNkMGRuV1VSV1VWRkVSWGhPVlZVeGNFWlRWVFZYVkRCc1JGSlRNVlJrVjBwRVVWTXdlRTFDTkZoRVZFbDVUVVJOZVU5RVJURk9SRmw2VFd4dldFUlVTWGxOUkUxNlRVUkZNVTVFV1hwTmJHOTNWRlJGVEUxQmEwZEJNVlZGUW1oTlExVXdSWGhFYWtGTlFtZE9Wa0pCYjFSQ1ZYQm9ZMjFzZVUxU2IzZEhRVmxFVmxGUlRFVjRSa3RhVjFKcldWZG5aMUZ1U21oaWJVNXZUVlJKZWs1RVJWTk5Ra0ZIUVRGVlJVRjRUVXBOVkVrelRHcEJkVTFETkhoTlJsbDNSVUZaU0V0dldrbDZhakJEUVZGWlJrczBSVVZCUVc5RVVXZEJSVVF2ZDJJeWJHaENka0pKUXpoRGJtNWFkbTkxYnpaUGVsSjViWGx0VlRsT1YxSm9TWGxoVFdoSFVrVkNRMFZhUWpSRlFWWnlRblZXTW5oWWFYaFpOSEZDV1dZNVpHUmxjbnByVnpsRWQyUnZNMGxzU0dkeFQwTkJhVzkzWjJkSmJVMUpSMHhDWjA1V1NGSkZSV2RaVFhkbldVTnJabXBDT0UxU2QzZEhaMWxFVmxGUlJVUkNUWGxOYWtsNVRXcE5lVTVFVVRCTmVsRjZZVzFhYlU1RVRYbE5VamgzU0ZGWlMwTmFTVzFwV2xCNVRFZFJRa0ZSZDFCTmVrVjNUVlJqTVUxNmF6Tk9SRUYzVFVSQmVrMVJNSGREZDFsRVZsRlJUVVJCVVhoTlJFVjRUVkpGZDBSM1dVUldVVkZoUkVGb1ZGbFhNWGRpUjFWblVsUkZXazFDWTBkQk1WVkZSSGQzVVZVeVJuUmpSM2hzU1VWS01XTXpUbkJpYlZaNlkzcEJaRUpuVGxaSVVUUkZSbWRSVldoWFkzTmlZa3BvYWtRMVdsZFBhM2RDU1V4REszZE9WbVpMV1hkSWQxbEVWbEl3YWtKQ1ozZEdiMEZWWkcxRFRTdDNZV2R5UjJSWVRsb3pVRzF4ZVc1TE5Xc3hkRk00ZDFSbldVUldVakJtUWtWamQxSlVRa1J2UlVkblVEUlpPV0ZJVWpCalJHOTJURE5TZW1SSFRubGlRelUyV1ZoU2FsbFROVzVpTTFsMVl6SkZkbEV5Vm5sa1JWWjFZMjA1YzJKRE9WVlZNWEJHVTFVMVYxUXdiRVJTVXpGVVpGZEtSRkZUTUhoTWJVNTVZa1JEUW5KUldVbExkMWxDUWxGVlNFRlJSVVZuWVVGM1oxb3dkMkpuV1VsTGQxbENRbEZWU0UxQlIwZFpiV2d3WkVoQk5reDVPVEJqTTFKcVkyMTNkV1Z0UmpCWk1rVjFXakk1TWt4dVRtaE1NRTVzWTI1U1JtSnVTblppUjNkMlZrWk9ZVkpYYkhWa2JUbHdXVEpXVkZFd1JYaE1iVlkwWkVka2FHVnVVWFZhTWpreVRHMTRkbGt5Um5OWU1WSlVWMnRXU2xSc1dsQlRWVTVHVEZaT01WbHJUa0pNVkVWdlRWTnJkVmt6U2pCTlEzTkhRME56UjBGUlZVWkNla0ZDYUdnNWIyUklVbmRQYVRoMlpFaE9NRmt6U25OTWJuQm9aRWRPYUV4dFpIWmthVFY2V1ZNNWRsa3pUbmROUVRSSFFURlZaRVIzUlVJdmQxRkZRWGRKU0dkRVFXUkNaMDVXU0ZOVlJVWnFRVlZDWjJkeVFtZEZSa0pSWTBSQloxbEpTM2RaUWtKUlZVaEJkMDEzU25kWlNrdDNXVUpDUVVkRFRuaFZTMEpDYjNkSFJFRkxRbWRuY2tKblJVWkNVV05FUVdwQlMwSm5aM0pDWjBWR1FsRmpSRUY2UVV0Q1oyZHhhR3RxVDFCUlVVUkJaMDVLUVVSQ1IwRnBSVUY1VG1oNVkxRXpZazVzVEVaa1QxQnNjVmxVTmxKV1VWUlhaMjVMTVVkb01FNUlaR05UV1RSUVprTXdRMGxSUTFOQmRHaFlkblkzZEdWMFZVdzJPVmRxY0RoQ2VHNU1URTEzWlhKNFdtaENibVYzYnk5blJqTkZTa0U5UFE9PTpmOVlSaG9wTi9HN3gwVEVDT1k2bktTQ0hMTllsYjVyaUFIU0ZQSUNvNHF3PQ==",
                                    # 'Authorization': 'Basic' + settings.basic_auth_production,
                                    'Authorization': 'Basic' + production_csid,
                                    'Content-Type': 'application/json',
                                    'Cookie': 'TS0106293e=0132a679c0639d13d069bcba831384623a2ca6da47fac8d91bef610c47c7119dcdd3b817f963ec301682dae864351c67ee3a402866'
                                    }    
                        else:
                            frappe.throw("Production CSID for company {} not found".format(company_name))
                        try:
                            response = requests.request("POST", url=get_API_url(url="invoices/reporting/single"), headers=headers, data=payload)
                            print(response.text)
                            print(response.status_code,"ResposeCode")
                            if response.status_code  in (400,405,406,409 ):
                                invoice_doc = frappe.get_doc('Sales Invoice' , invoice_number )
                                invoice_doc.db_set('custom_uuid' , 'Not Submitted' , commit=True  , update_modified=True)
                                invoice_doc.db_set('custom_zatca_status' , 'Not Submitted' , commit=True  , update_modified=True)

                                frappe.throw("Error: The request you are sending to Zatca is in incorrect format. Please report to system administrator . Status code:  " + str(response.status_code) + "<br><br> " + response.text )            
                            
                            
                            if response.status_code  in (401,403,407,451 ):
                                invoice_doc = frappe.get_doc('Sales Invoice' , invoice_number  )
                                invoice_doc.db_set('custom_uuid' , 'Not Submitted' , commit=True  , update_modified=True)
                                invoice_doc.db_set('custom_zatca_status' , 'Not Submitted' , commit=True  , update_modified=True)

                              
                                frappe.throw("Error: Zatca Authentication failed. Your access token may be expired or not valid. Please contact your system administrator. Status code:  " + str(response.status_code) + "<br><br> " + response.text)            
                            
                            if response.status_code not in (200, 202):
                                invoice_doc = frappe.get_doc('Sales Invoice' , invoice_number  )
                                invoice_doc.db_set('custom_uuid' , 'Not Submitted' , commit=True  , update_modified=True)
                                invoice_doc.db_set('custom_zatca_status' , 'Not Submitted' , commit=True  , update_modified=True)
                                
                               
                                frappe.throw("Error: Zatca server busy or not responding. Try after sometime or contact your system administrator. Status code:  " + str(response.status_code)+ "<br><br> " + response.text )
                            
                            
                            
                            if response.status_code  in (200, 202):
                                if response.status_code == 202:
                                    msg = "REPORTED WITH WARNIGS: <br> <br> Please copy the below message and send it to your system administrator to fix this warnings before next submission <br>  <br><br> "
                                
                                if response.status_code == 200:
                                    msg = "SUCCESS: <br>   <br><br> "
                                
                                msg = msg + "Status Code: " + str(response.status_code) + "<br><br> "
                                msg = msg + "Zatca Response: " + response.text + "<br><br> "
                                frappe.msgprint(msg)
                                # pih_data = json.loads(settings.get("pih", "{}"))
                                # updated_pih_data = update_json_data_pih(pih_data, company_name, encoded_hash)
                                # settings.set("pih", json.dumps(updated_pih_data))
                                # settings.save(ignore_permissions=True)
                                
                                invoice_doc = frappe.get_doc('Sales Invoice' , invoice_number )
                                invoice_doc.db_set('custom_uuid' , uuid1 , commit=True  , update_modified=True)
                                invoice_doc.db_set('custom_zatca_status' , 'REPORTED' , commit=True  , update_modified=True)

                               
                                # frappe.msgprint(xml_cleared)
                                # success_Log(response.text,uuid1, invoice_number)
                                
                            else:
                                error_Log()
                        except Exception as e:
                            frappe.throw("Error in reporting api-2:  " + str(e) )
    
                    except Exception as e:
                        frappe.throw("Error in reporting api-1:  " + str(e) )