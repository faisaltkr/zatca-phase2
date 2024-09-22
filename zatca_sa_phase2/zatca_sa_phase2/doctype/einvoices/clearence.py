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


def get_production_csid_for_company(basic_auth_production_data, company_name):
                    try:  
                        for entry in basic_auth_production_data.get("companies", []):
                            if entry.get("company") == company_name:
                                return entry.get("production_csid")
                        return None
                    except Exception as e:
                            frappe.throw("Error in getting production csid of company for api   " + str(e)) 

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


def clearance_API(uuid1,encoded_hash,signed_xmlfile_name,invoice_number,sales_invoice_doc):
                    try:
                        # frappe.msgprint("Clearance API")
                        key = frappe.get_all('CSR Settings', fields=['company_name','csid','secret'])
                        company =  key[0]['company_name']                              # company = settings.company
                        csid = key[0]['csid']
                        company_name = company
                        secret = key[0]['secret']

                        payload = json.dumps({
                        "invoiceHash": encoded_hash,
                        "uuid": uuid1,
                        "invoice": xml_base64_Decode(signed_xmlfile_name), })
                        # basic_auth_production = csid
                        print(signed_xmlfile_name)
                        print(xml_base64_Decode(signed_xmlfile_name),"dddddd")
                        print(payload)
                        # basic_auth_production_data = json.loads(basic_auth_production)
                        production_csid = csid
                        tk =   'VFVsSlJETnFRME5CTkZOblFYZEpRa0ZuU1ZSRlVVRkJUMEZRUmprd1FXcHpMM2hqV0hkQlFrRkJRVFJCZWtGTFFtZG5jV2hyYWs5UVVWRkVRV3BDYVUxU1ZYZEZkMWxMUTFwSmJXbGFVSGxNUjFGQ1IxSlpSbUpIT1dwWlYzZDRSWHBCVWtKbmIwcHJhV0ZLYXk5SmMxcEJSVnBHWjA1dVlqTlplRVo2UVZaQ1oyOUthMmxoU21zdlNYTmFRVVZhUm1ka2JHVklVbTVaV0hBd1RWSnpkMGRSV1VSV1VWRkVSWGhLVVZWc2NFWlRWVFZYVkRCc1JGSldUa1JSVkZGMFVUQkZkMGhvWTA1TmFsRjNUVlJGZUUxRWEzaFBWRTEzVjJoalRrMXFhM2ROVkVFMVRVUnJlRTlVVFhkWGFrSXhUVkZ6ZDBOUldVUldVVkZIUlhkS1ZGRlVSVzFOUTFGSFFURlZSVU5vVFdSVVYwWTBZVmN4TVdKVFFsUmpSMVpzV2tOQ1ZWcFhUbTlKUms0eFkwaENjMlZUUWsxV1JWRjRSbXBCVlVKblRsWkNRWE5VUkZaS2NHVlhSbXRoUTBKRFkyMUdkVmt5WjNoS2FrRnJRbWRPVmtKQlRWUklWbEpVVmtNd05FOUVXVEJOZWtWNFRrUlZkRTE2YXpWUFZHczFUMVJyTlU5VVFYZE5SRUY2VFVaWmQwVkJXVWhMYjFwSmVtb3dRMEZSV1VaTE5FVkZRVUZ2UkZGblFVVnZWME5MWVRCVFlUbEdTVVZ5VkU5Mk1IVkJhME14VmtsTFdIaFZPVzVRY0hneWRteG1OSGxvVFdWcWVUaGpNREpZU21Kc1JIRTNkRkI1Wkc4NGJYRXdZV2hQVFcxT2J6aG5kMjVwTjFoME1VdFVPVlZsUzA5RFFXZGpkMmRuU1VSTlNVZDBRbWRPVmtoU1JVVm5ZVlYzWjJGTGEyZGFPSGRuV25kNFQzcEJOVUpuVGxaQ1FWRk5UV3BGZEZaR1RsVm1SRWwwVmtaT1ZXWkVUWFJhVjFGNVRXMVplRnBFWjNSYVZGcG9UV2t3ZUUxVVJUUk1WR3hwVGxSbmRGcEViR2hQUjFsNFRWZFZNRTVFVm0xTlVqaDNTRkZaUzBOYVNXMXBXbEI1VEVkUlFrRlJkMUJOZW1zMVQxUnJOVTlVYXpWUFZFRjNUVVJCZWsxUk1IZERkMWxFVmxGUlRVUkJVWGhOVkVGM1RWSkZkMFIzV1VSV1VWRmhSRUZvVTFWc1NrVk5hbXQ1VDFSRllVMUNaMGRCTVZWRlJIZDNVbFV6Vm5kalIzZzFTVWRHYW1SSGJESmhXRkp3V2xoTmQwaFJXVVJXVWpCUFFrSlpSVVpGV0N0WmRtMXRkRzVaYjBSbU9VSkhZa3R2TjI5alZFdFpTekZOUWpoSFFURlZaRWwzVVZsTlFtRkJSa3AyUzNGeFRIUnRjWGR6YTBsR2VsWjJjRkF5VUhoVUt6bE9iazFJYzBkRFEzTkhRVkZWUmtKM1JVSkNSemgzWWxSQ2NrSm5aM0pDWjBWR1FsRmpkMEZ2V21aaFNGSXdZMFJ2ZGt3eVJuQlpWRkYxWlcxR01Ga3lSWFZhTWpreVRHNU9hRXd3VG14amJsSkdZbTVLZG1KSGQzWlZSa3BoVWxWc2RXUnRPWEJaTWxaVVVUQkZNRXh0VmpSa1IyUm9aVzVSZFZveU9USk1iWGgyV1RKR2MxZ3hRbE5YYTFaS1ZHeGFVRk5WVGtaVk1FNUNUa014UkZGVFozaExVelZxWTI1UmQwUm5XVVJXVWpCUVFWRklMMEpCVVVSQloyVkJUVVIzUjBOVGMwZEJVVkZDWjJwalZrSjNVWFpOUXpCSFNsTnpSMEZSVVVKbmFtTldRMGxIUjNGQ01rVXdVSE5UYUhVeVpFcEpaazhyZUc1VWQwWldiV2d2Y1d4YVdWaGFhRVEwUTBGWFVVTkJVa2wzU0ZGWlJGWlNNR3hDUWxsM1JrRlpTVXQzV1VKQ1VWVklRWGROUjBORGMwZEJVVlZHUW5kTlEwMURZMGREVTNOSFFWRlJRbWRxWTFaRFoxRmhUVUpuZDBObldVbExkMWxDUWxGVlNFRjNUWGREWjFsSlMzZFpRa0pSVlVoQmQwbDNRMmRaU1V0dldrbDZhakJGUVhkSlJGTkJRWGRTVVVsb1FVeEZMMmxqYUcxdVYxaERWVXRWWW1OaE0zbGphVGh2Y1hkaFRIWkdaRWhXYWxGeWRtVkpPWFZ4UVdKQmFVRTVhRU0wVFRocVowMUNRVVJRVTNwdFpESjFhVkJLUVRablMxSXpURVV3TTFVM05XVnhZa012Y2xoQlBUMD06Q2tZc0VYZlY4YzFnRkhBdEZXb1p2NzNwR012aC9ReW80THpLTTJoLzhIZz0='
                        # tk = "VFVsSlEwZHFRME5CWWl0blFYZEpRa0ZuU1VkQldrWlhiMlkzWjAxQmIwZERRM0ZIVTAwME9VSkJUVU5OUWxWNFJYcEJVa0puVGxaQ1FVMU5RMjFXU21KdVduWmhWMDV3WW0xamQwaG9ZMDVOYWxGM1QwUkZNVTFVVlhsTmFrVXpWMmhqVGsxcWEzZFBSRVV3VFdwRmQwMUVRWGRYYWtKcFRWRnpkME5SV1VSV1VWRkhSWGRLVkZGVVJWZE5RbEZIUVRGVlJVTjNkMDVWYld3MVdWZFNiMGxGU25sWlZ6VnFZVVJGVkUxQ1JVZEJNVlZGUTJkM1MxSllhSFppYlZWblZrZFdhbUZFUlcxTlExRkhRVEZWUlVGM2QyUldSazVWVEZSbk5FNXFVWHBOVkVVd1RsTXdlazlVYXpWUFZHczFUMVJyTlUxRVFYZE5SRTEzVm1wQlVVSm5ZM0ZvYTJwUFVGRkpRa0puVlhKblVWRkJRMmRPUTBGQlUzZEZSR2xSUnpnNGNEWnBTWG8wUkdwS2EwUlZVbXhyU2tKclppOURVbXh1WmtSWFJEbENNbTFFYWtrclNqUmpRMWhDYUN0WFEycFVLMU5qUTI1NGQwMWxjVXRYTkZKUFkyZDFVeTlvU1U4MlZsRkNXV1Z2TkVkM1RVbEhkRTFCZDBkQk1WVmtSWGRGUWk5M1VVTk5RVUYzWjFwM1IwRXhWV1JGVVZOQ2JFUkRRbXRoVTBKcWFrTkNhWHBGTjAxRWEwZEJNVlZGUWtGM2VVMVRNVlZWTVZJNFRXa3hWVlV4VWpoTmVURnNXa1JKZVZwcVJtdFBRekZzVG0xRmVVeFVSWGhOVkdkMFQxZEpNVTlETVd0UFYwVTBXbXBGZUZwVVVUQk9WMWw0U0hwQlpFSm5iMHByYVdGS2F5OUpjMXBCUlVKRVFUaDZUMVJyTlU5VWF6VlBWR3MxVFVSQmQwMUVUWGhFVkVGTVFtZE9Wa0pCZDAxQ1JFVjRUVVJCZUVSNlFVNUNaMDVXUWtKdlRVSnNTbkJsVjBacllVUkZURTFCYTBkQk1WVkZSSGQzUTFOV1VYZERaMWxKUzI5YVNYcHFNRVZCZDBsRVUxRkJkMUpuU1doQlRVSnpNR0pUTTJaTGJVZGtiMm9yYkN0NFVtdFdXbFZqY0RGUmRFcE1NMFJxZGtjM1FrOVlUbWw0UjBGcFJVRnpkVEZwT1U1MVJGVmpiMkptWW5GeWFrdFpPWGwzU1RsWlQzaDNZVEo0UVdaMmQwUk9lV05xUkhORlBRPT06dThzcGh1TWJWbjJYMFRYSFVvSnlxUG1PK25jRG54UGdDeFVjMVlCdVNPZz0="

                        # tk = 'VFVsSlJETnFRME5CTkZOblFYZEpRa0ZuU1ZSRlVVRkJUMEZRUmprd1FXcHpMM2hqV0hkQlFrRkJRVFJCZWtGTFFtZG5jV2hyYWs5UVVWRkVRV3BDYVUxU1ZYZEZkMWxMUTFwSmJXbGFVSGxNUjFGQ1IxSlpSbUpIT1dwWlYzZDRSWHBCVWtKbmIwcHJhV0ZLYXk5SmMxcEJSVnBHWjA1dVlqTlplRVo2UVZaQ1oyOUthMmxoU21zdlNYTmFRVVZhUm1ka2JHVklVbTVaV0hBd1RWSnpkMGRSV1VSV1VWRkVSWGhLVVZWc2NFWlRWVFZYVkRCc1JGSldUa1JSVkZGMFVUQkZkMGhvWTA1TmFsRjNUVlJGZUUxRWEzaFBWRTEzVjJoalRrMXFhM2ROVkVFMVRVUnJlRTlVVFhkWGFrSXhUVkZ6ZDBOUldVUldVVkZIUlhkS1ZGRlVSVzFOUTFGSFFURlZSVU5vVFdSVVYwWTBZVmN4TVdKVFFsUmpSMVpzV2tOQ1ZWcFhUbTlKUms0eFkwaENjMlZUUWsxV1JWRjRSbXBCVlVKblRsWkNRWE5VUkZaS2NHVlhSbXRoUTBKRFkyMUdkVmt5WjNoS2FrRnJRbWRPVmtKQlRWUklWbEpVVmtNd05FOUVXVEJOZWtWNFRrUlZkRTE2YXpWUFZHczFUMVJyTlU5VVFYZE5SRUY2VFVaWmQwVkJXVWhMYjFwSmVtb3dRMEZSV1VaTE5FVkZRVUZ2UkZGblFVVnZWME5MWVRCVFlUbEdTVVZ5VkU5Mk1IVkJhME14VmtsTFdIaFZPVzVRY0hneWRteG1OSGxvVFdWcWVUaGpNREpZU21Kc1JIRTNkRkI1Wkc4NGJYRXdZV2hQVFcxT2J6aG5kMjVwTjFoME1VdFVPVlZsUzA5RFFXZGpkMmRuU1VSTlNVZDBRbWRPVmtoU1JVVm5ZVlYzWjJGTGEyZGFPSGRuV25kNFQzcEJOVUpuVGxaQ1FWRk5UV3BGZEZaR1RsVm1SRWwwVmtaT1ZXWkVUWFJhVjFGNVRXMVplRnBFWjNSYVZGcG9UV2t3ZUUxVVJUUk1WR3hwVGxSbmRGcEViR2hQUjFsNFRWZFZNRTVFVm0xTlVqaDNTRkZaUzBOYVNXMXBXbEI1VEVkUlFrRlJkMUJOZW1zMVQxUnJOVTlVYXpWUFZFRjNUVVJCZWsxUk1IZERkMWxFVmxGUlRVUkJVWGhOVkVGM1RWSkZkMFIzV1VSV1VWRmhSRUZvVTFWc1NrVk5hbXQ1VDFSRllVMUNaMGRCTVZWRlJIZDNVbFV6Vm5kalIzZzFTVWRHYW1SSGJESmhXRkp3V2xoTmQwaFJXVVJXVWpCUFFrSlpSVVpGV0N0WmRtMXRkRzVaYjBSbU9VSkhZa3R2TjI5alZFdFpTekZOUWpoSFFURlZaRWwzVVZsTlFtRkJSa3AyUzNGeFRIUnRjWGR6YTBsR2VsWjJjRkF5VUhoVUt6bE9iazFJYzBkRFEzTkhRVkZWUmtKM1JVSkNSemgzWWxSQ2NrSm5aM0pDWjBWR1FsRmpkMEZ2V21aaFNGSXdZMFJ2ZGt3eVJuQlpWRkYxWlcxR01Ga3lSWFZhTWpreVRHNU9hRXd3VG14amJsSkdZbTVLZG1KSGQzWlZSa3BoVWxWc2RXUnRPWEJaTWxaVVVUQkZNRXh0VmpSa1IyUm9aVzVSZFZveU9USk1iWGgyV1RKR2MxZ3hRbE5YYTFaS1ZHeGFVRk5WVGtaVk1FNUNUa014UkZGVFozaExVelZxWTI1UmQwUm5XVVJXVWpCUVFWRklMMEpCVVVSQloyVkJUVVIzUjBOVGMwZEJVVkZDWjJwalZrSjNVWFpOUXpCSFNsTnpSMEZSVVVKbmFtTldRMGxIUjNGQ01rVXdVSE5UYUhVeVpFcEpaazhyZUc1VWQwWldiV2d2Y1d4YVdWaGFhRVEwUTBGWFVVTkJVa2wzU0ZGWlJGWlNNR3hDUWxsM1JrRlpTVXQzV1VKQ1VWVklRWGROUjBORGMwZEJVVlZHUW5kTlEwMURZMGREVTNOSFFWRlJRbWRxWTFaRFoxRmhUVUpuZDBObldVbExkMWxDUWxGVlNFRjNUWGREWjFsSlMzZFpRa0pSVlVoQmQwbDNRMmRaU1V0dldrbDZhakJGUVhkSlJGTkJRWGRTVVVsb1FVeEZMMmxqYUcxdVYxaERWVXRWWW1OaE0zbGphVGh2Y1hkaFRIWkdaRWhXYWxGeWRtVkpPWFZ4UVdKQmFVRTVhRU0wVFRocVowMUNRVVJRVTNwdFpESjFhVkJLUVRablMxSXpURVV3TTFVM05XVnhZa012Y2xoQlBUMD06Q2tZc0VYZlY4YzFnRkhBdEZXb1p2NzNwR012aC9ReW80THpLTTJoLzhIZz0='
                        if production_csid:
                            headers = {
                            'accept': 'application/json',
                            'accept-language': 'en',
                            'Clearance-Status': '1',
                            'Accept-Version': 'V2',
                            'Authorization': 'Basic ' +tk,
                            # 'Authorization': 'Basic' + settings.basic_auth,
                            'Content-Type': 'application/json',
                            'Cookie': 'TS0106293e=0132a679c03c628e6c49de86c0f6bb76390abb4416868d6368d6d7c05da619c8326266f5bc262b7c0c65a6863cd3b19081d64eee99' }
                        else:
                            frappe.throw("Production CSID for company {} not found".format(company_name))
                        response = requests.request("POST", url=get_API_url(url="invoices/clearance/single"), headers=headers, data=payload)
                        
                        
                        if response.status_code  in (400,405,406,409 ):
                            invoice_doc = frappe.get_doc('Sales Invoice' , invoice_number  )
                            invoice_doc.db_set('custom_uuid' , "Not Submitted" , commit=True  , update_modified=True)
                            invoice_doc.db_set('custom_zatca_status' , "Not Submitted" , commit=True  , update_modified=True)
                            
                           
                            frappe.throw("Error: The request you are sending to Zatca is in incorrect format. Please report to system administrator . Status code:  " + str(response.status_code) + "<br><br> " + response.text )            
                        
                        
                        if response.status_code  in (401,403,407,451 ):
                            invoice_doc = frappe.get_doc('Sales Invoice' , invoice_number  )
                            invoice_doc.db_set('custom_uuid' , "Not Submitted" , commit=True  , update_modified=True)
                            invoice_doc.db_set('custom_zatca_status' , "Not Submitted" , commit=True  , update_modified=True)

                           
                            frappe.throw("Error: Zatca Authentication failed. Your access token may be expired or not valid. Please contact your system administrator. Status code:  " + str(response.status_code) + "<br><br> " + response.text)            
                        
                        if response.status_code not in (200, 202):
                            invoice_doc = frappe.get_doc('Sales Invoice' , invoice_number  )
                            invoice_doc.db_set('custom_uuid' , "Not Submitted" , commit=True  , update_modified=True)
                            invoice_doc.db_set('custom_zatca_status' , "Not Submitted" , commit=True  , update_modified=True)

                            
                          
                          
                            
                            frappe.throw("Error: Zatca server busy or not responding. Try after sometime or contact your system administrator. Status code:  " + str(response.status_code))
                        
                        if response.status_code  in (200, 202):
                                if response.status_code == 202:
                                    msg = "CLEARED WITH WARNIGS: <br> <br> Please copy the below message and send it to your system administrator to fix this warnings before next submission <br>  <br><br> "
                                
                                if response.status_code == 200:
                                    msg = "SUCCESS: <br>   <br><br> "
                                
                                msg = msg + "Status Code: " + str(response.status_code) + "<br><br> "
                                msg = msg + "Zatca Response: " + response.text + "<br><br> "
                                frappe.msgprint(msg)
                                # pih_data = json.loads(settings.get("pih", "{}"))
                                # updated_pih_data = update_json_data_pih(pih_data, company_name,encoded_hash)
                                # settings.set("pih", json.dumps(updated_pih_data))
                                # settings.save(ignore_permissions=True)
                                
                                invoice_doc = frappe.get_doc('Sales Invoice' , invoice_number )
                                invoice_doc.db_set('custom_uuid' , uuid1 , commit=True  , update_modified=True)
                                invoice_doc.db_set('custom_zatca_status' , "CLEARED" , commit=True  , update_modified=True)
                                
                               
                                
                                data=json.loads(response.text)
                                base64_xml = data["clearedInvoice"] 
                                xml_cleared= base64.b64decode(base64_xml).decode('utf-8')
                                file = frappe.get_doc({                       #attaching the cleared xml
                                    "doctype": "File",
                                    "file_name": "Cleared xml file" + sales_invoice_doc.name,
                                    "attached_to_doctype": sales_invoice_doc.doctype,
                                    "attached_to_name": sales_invoice_doc.name,
                                    "content": xml_cleared
                                    
                                })
                                file.save(ignore_permissions=True)
                                # frappe.msgprint(xml_cleared)
                                # success_Log(response.text,uuid1, invoice_number)
                                return xml_cleared
                        else:
                                error_Log()
                            
                    except Exception as e:
                        frappe.throw("error in clearance api: jjjjjjjjj " + str(e) )

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
                    print(url,"kkkkkkkkkkkkkkkk")
                    return url 
                except Exception as e:
                    frappe.throw(" getting url failed"+ str(e) ) 

