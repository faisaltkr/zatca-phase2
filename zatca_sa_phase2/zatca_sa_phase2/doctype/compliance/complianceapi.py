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
                    key = frappe.get_all('CSR Settings', fields=['select_environment'])
                    env =  key[0]['select_environment']                    
                    if env == "Sandbox":
                        url = f"https://gw-fatoora.zatca.gov.sa/e-invoicing/developer-portal/{base_url}"
                    elif env == "Simulation":
                        url = f"https://gw-fatoora.zatca.gov.sa/e-invoicing/simulation/{base_url}"
                    else:
                        url = f"https://gw-fatoora.zatca.gov.sa/e-invoicing/core/{base_url}"
                    print(url,"kkkkkkkkkkkkkkkk")
                    return url 
                except Exception as e:
                    frappe.throw(" getting url failed"+ str(e) ) 


def compliance_api_call(uuid1,encoded_hash,signed_xmlfile_name):
                try:                        
                    key = frappe.get_all('CSR Settings', fields=['company_name','csid','secret'])
                    company =  key[0]['company_name']      
                    csid = key[0]['csid']
                    # print(type(csid),"csidddddd")
                    # settings = frappe.get_doc('Zatca ERPgulf Setting')
                    print(type(xml_base64_Decode(signed_xmlfile_name)))
                    print(signed_xmlfile_name,"mmmmm")
                    # print(type(encoded_hash))
                    payload = json.dumps({
                        "invoiceHash": str(encoded_hash),
                        "uuid": str(uuid1),
                        "invoice": xml_base64_Decode(str(signed_xmlfile_name)) })
                    
                    # print(payload)
                    company_name = frappe.db.get_value("Company", company, "abbr")
                    # print("ssss")
                    # basic_auth = settings.get("basic_auth", "{}")
                    # tk =   'VFVsSlJETnFRME5CTkZOblFYZEpRa0ZuU1ZSRlVVRkJUMEZRUmprd1FXcHpMM2hqV0hkQlFrRkJRVFJCZWtGTFFtZG5jV2hyYWs5UVVWRkVRV3BDYVUxU1ZYZEZkMWxMUTFwSmJXbGFVSGxNUjFGQ1IxSlpSbUpIT1dwWlYzZDRSWHBCVWtKbmIwcHJhV0ZLYXk5SmMxcEJSVnBHWjA1dVlqTlplRVo2UVZaQ1oyOUthMmxoU21zdlNYTmFRVVZhUm1ka2JHVklVbTVaV0hBd1RWSnpkMGRSV1VSV1VWRkVSWGhLVVZWc2NFWlRWVFZYVkRCc1JGSldUa1JSVkZGMFVUQkZkMGhvWTA1TmFsRjNUVlJGZUUxRWEzaFBWRTEzVjJoalRrMXFhM2ROVkVFMVRVUnJlRTlVVFhkWGFrSXhUVkZ6ZDBOUldVUldVVkZIUlhkS1ZGRlVSVzFOUTFGSFFURlZSVU5vVFdSVVYwWTBZVmN4TVdKVFFsUmpSMVpzV2tOQ1ZWcFhUbTlKUms0eFkwaENjMlZUUWsxV1JWRjRSbXBCVlVKblRsWkNRWE5VUkZaS2NHVlhSbXRoUTBKRFkyMUdkVmt5WjNoS2FrRnJRbWRPVmtKQlRWUklWbEpVVmtNd05FOUVXVEJOZWtWNFRrUlZkRTE2YXpWUFZHczFUMVJyTlU5VVFYZE5SRUY2VFVaWmQwVkJXVWhMYjFwSmVtb3dRMEZSV1VaTE5FVkZRVUZ2UkZGblFVVnZWME5MWVRCVFlUbEdTVVZ5VkU5Mk1IVkJhME14VmtsTFdIaFZPVzVRY0hneWRteG1OSGxvVFdWcWVUaGpNREpZU21Kc1JIRTNkRkI1Wkc4NGJYRXdZV2hQVFcxT2J6aG5kMjVwTjFoME1VdFVPVlZsUzA5RFFXZGpkMmRuU1VSTlNVZDBRbWRPVmtoU1JVVm5ZVlYzWjJGTGEyZGFPSGRuV25kNFQzcEJOVUpuVGxaQ1FWRk5UV3BGZEZaR1RsVm1SRWwwVmtaT1ZXWkVUWFJhVjFGNVRXMVplRnBFWjNSYVZGcG9UV2t3ZUUxVVJUUk1WR3hwVGxSbmRGcEViR2hQUjFsNFRWZFZNRTVFVm0xTlVqaDNTRkZaUzBOYVNXMXBXbEI1VEVkUlFrRlJkMUJOZW1zMVQxUnJOVTlVYXpWUFZFRjNUVVJCZWsxUk1IZERkMWxFVmxGUlRVUkJVWGhOVkVGM1RWSkZkMFIzV1VSV1VWRmhSRUZvVTFWc1NrVk5hbXQ1VDFSRllVMUNaMGRCTVZWRlJIZDNVbFV6Vm5kalIzZzFTVWRHYW1SSGJESmhXRkp3V2xoTmQwaFJXVVJXVWpCUFFrSlpSVVpGV0N0WmRtMXRkRzVaYjBSbU9VSkhZa3R2TjI5alZFdFpTekZOUWpoSFFURlZaRWwzVVZsTlFtRkJSa3AyUzNGeFRIUnRjWGR6YTBsR2VsWjJjRkF5VUhoVUt6bE9iazFJYzBkRFEzTkhRVkZWUmtKM1JVSkNSemgzWWxSQ2NrSm5aM0pDWjBWR1FsRmpkMEZ2V21aaFNGSXdZMFJ2ZGt3eVJuQlpWRkYxWlcxR01Ga3lSWFZhTWpreVRHNU9hRXd3VG14amJsSkdZbTVLZG1KSGQzWlZSa3BoVWxWc2RXUnRPWEJaTWxaVVVUQkZNRXh0VmpSa1IyUm9aVzVSZFZveU9USk1iWGgyV1RKR2MxZ3hRbE5YYTFaS1ZHeGFVRk5WVGtaVk1FNUNUa014UkZGVFozaExVelZxWTI1UmQwUm5XVVJXVWpCUVFWRklMMEpCVVVSQloyVkJUVVIzUjBOVGMwZEJVVkZDWjJwalZrSjNVWFpOUXpCSFNsTnpSMEZSVVVKbmFtTldRMGxIUjNGQ01rVXdVSE5UYUhVeVpFcEpaazhyZUc1VWQwWldiV2d2Y1d4YVdWaGFhRVEwUTBGWFVVTkJVa2wzU0ZGWlJGWlNNR3hDUWxsM1JrRlpTVXQzV1VKQ1VWVklRWGROUjBORGMwZEJVVlZHUW5kTlEwMURZMGREVTNOSFFWRlJRbWRxWTFaRFoxRmhUVUpuZDBObldVbExkMWxDUWxGVlNFRjNUWGREWjFsSlMzZFpRa0pSVlVoQmQwbDNRMmRaU1V0dldrbDZhakJGUVhkSlJGTkJRWGRTVVVsb1FVeEZMMmxqYUcxdVYxaERWVXRWWW1OaE0zbGphVGh2Y1hkaFRIWkdaRWhXYWxGeWRtVkpPWFZ4UVdKQmFVRTVhRU0wVFRocVowMUNRVVJRVTNwdFpESjFhVkJLUVRablMxSXpURVV3TTFVM05XVnhZa012Y2xoQlBUMD06Q2tZc0VYZlY4YzFnRkhBdEZXb1p2NzNwR012aC9ReW80THpLTTJoLzhIZz0='
                    # tk = 'TUlJQ1BEQ0NBZU9nQXdJQkFnSUdBWkZrNjBlck1Bb0dDQ3FHU000OUJBTUNNQlV4RXpBUkJnTlZCQU1NQ21WSmJuWnZhV05wYm1jd0hoY05NalF3T0RFNE1EazFOekF4V2hjTk1qa3dPREUzTWpFd01EQXdXakIxTVFzd0NRWURWUVFHRXdKVFFURVdNQlFHQTFVRUN3d05VbWw1WVdSb0lFSnlZVzVqYURFbU1DUUdBMVVFQ2d3ZFRXRjRhVzExYlNCVGNHVmxaQ0JVWldOb0lGTjFjSEJzZVNCTVZFUXhKakFrQmdOVkJBTU1IVlJUVkMwNE9EWTBNekV4TkRVdE16azVPVGs1T1RrNU9UQXdNREF6TUZZd0VBWUhLb1pJemowQ0FRWUZLNEVFQUFvRFFnQUVvV0NLYTBTYTlGSUVyVE92MHVBa0MxVklLWHhVOW5QcHgydmxmNHloTWVqeThjMDJYSmJsRHE3dFB5ZG84bXEwYWhPTW1Obzhnd25pN1h0MUtUOVVlS09Cd1RDQnZqQU1CZ05WSFJNQkFmOEVBakFBTUlHdEJnTlZIUkVFZ2FVd2dhS2tnWjh3Z1p3eE96QTVCZ05WQkFRTU1qRXRWRk5VZkRJdFZGTlVmRE10WldReU1tWXhaRGd0WlRaaE1pMHhNVEU0TFRsaU5UZ3RaRGxoT0dZeE1XVTBORFZtTVI4d0hRWUtDWkltaVpQeUxHUUJBUXdQTXprNU9UazVPVGs1T1RBd01EQXpNUTB3Q3dZRFZRUU1EQVF4TVRBd01SRXdEd1lEVlFRYURBaFNVbEpFTWpreU9URWFNQmdHQTFVRUR3d1JVM1Z3Y0d4NUlHRmpkR2wyYVhScFpYTXdDZ1lJS29aSXpqMEVBd0lEUndBd1JBSWdNa0x0UThUKzNFdS85c1AyOWUwNGNYbDMrd01nT1I2TG5iR0Y0c29qMDFzQ0lGM2VkK3dwOVdjVGdqR0hmblp2U3lrNWZRazE1MmJaajljYnJ6ZUxkbWgw'
                    # frappe.msgprint(basic_auth)
                    # basic_auth_data = json.loads(basic_auth)
                    # csid = get_csid_for_company(basic_auth_data, company_name)
                    # frappe.msgprint(csid)
                    tk = "VFVsSlEwZHFRME5CWWl0blFYZEpRa0ZuU1VkQldrWlhiMlkzWjAxQmIwZERRM0ZIVTAwME9VSkJUVU5OUWxWNFJYcEJVa0puVGxaQ1FVMU5RMjFXU21KdVduWmhWMDV3WW0xamQwaG9ZMDVOYWxGM1QwUkZNVTFVVlhsTmFrVXpWMmhqVGsxcWEzZFBSRVV3VFdwRmQwMUVRWGRYYWtKcFRWRnpkME5SV1VSV1VWRkhSWGRLVkZGVVJWZE5RbEZIUVRGVlJVTjNkMDVWYld3MVdWZFNiMGxGU25sWlZ6VnFZVVJGVkUxQ1JVZEJNVlZGUTJkM1MxSllhSFppYlZWblZrZFdhbUZFUlcxTlExRkhRVEZWUlVGM2QyUldSazVWVEZSbk5FNXFVWHBOVkVVd1RsTXdlazlVYXpWUFZHczFUMVJyTlUxRVFYZE5SRTEzVm1wQlVVSm5ZM0ZvYTJwUFVGRkpRa0puVlhKblVWRkJRMmRPUTBGQlUzZEZSR2xSUnpnNGNEWnBTWG8wUkdwS2EwUlZVbXhyU2tKclppOURVbXh1WmtSWFJEbENNbTFFYWtrclNqUmpRMWhDYUN0WFEycFVLMU5qUTI1NGQwMWxjVXRYTkZKUFkyZDFVeTlvU1U4MlZsRkNXV1Z2TkVkM1RVbEhkRTFCZDBkQk1WVmtSWGRGUWk5M1VVTk5RVUYzWjFwM1IwRXhWV1JGVVZOQ2JFUkRRbXRoVTBKcWFrTkNhWHBGTjAxRWEwZEJNVlZGUWtGM2VVMVRNVlZWTVZJNFRXa3hWVlV4VWpoTmVURnNXa1JKZVZwcVJtdFBRekZzVG0xRmVVeFVSWGhOVkdkMFQxZEpNVTlETVd0UFYwVTBXbXBGZUZwVVVUQk9WMWw0U0hwQlpFSm5iMHByYVdGS2F5OUpjMXBCUlVKRVFUaDZUMVJyTlU5VWF6VlBWR3MxVFVSQmQwMUVUWGhFVkVGTVFtZE9Wa0pCZDAxQ1JFVjRUVVJCZUVSNlFVNUNaMDVXUWtKdlRVSnNTbkJsVjBacllVUkZURTFCYTBkQk1WVkZSSGQzUTFOV1VYZERaMWxKUzI5YVNYcHFNRVZCZDBsRVUxRkJkMUpuU1doQlRVSnpNR0pUTTJaTGJVZGtiMm9yYkN0NFVtdFdXbFZqY0RGUmRFcE1NMFJxZGtjM1FrOVlUbWw0UjBGcFJVRnpkVEZwT1U1MVJGVmpiMkptWW5GeWFrdFpPWGwzU1RsWlQzaDNZVEo0UVdaMmQwUk9lV05xUkhORlBRPT06dThzcGh1TWJWbjJYMFRYSFVvSnlxUG1PK25jRG54UGdDeFVjMVlCdVNPZz0="
                    if csid:
                        headers = {
                            'accept': 'application/json',
                            'Accept-Language': 'en',
                            'Accept-Version': 'V2',
                            'Authorization': "Basic " + tk,
                            'Content-Type': 'application/json'
                        }
                    else:
                        frappe.throw("CSID for company {} not found".format(company_name))
                    try:
                        # frappe.throw("inside compliance api call2")
                        response = requests.request("POST", url=get_API_url(base_url="compliance/invoices"), headers=headers, data=payload)
                        frappe.msgprint(response.text)
                        print(response.status_code,response.text,"kkdfjkgkjfekgdkfjgkj")
                        # return response.text

                        if response.status_code != 200:

                            frappe.throw("Error in complaince: " + str(response.text))    
                    
                    except Exception as e:
                        frappe.msgprint(str(e))
                        return "error in compliance", "NOT ACCEPTED"
                except Exception as e:
                    frappe.throw("ERROR in clearance invoice ,zatca validation:  " + str(e) )