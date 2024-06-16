import frappe
import json
import base64

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
                        settings = frappe.get_doc('Zatca ERPgulf Setting')
                        company = settings.company
                        company_name = frappe.db.get_value("Company", company, "abbr")
                        payload = json.dumps({
                        "invoiceHash": encoded_hash,
                        "uuid": uuid1,
                        "invoice": xml_base64_Decode(signed_xmlfile_name), })
                        basic_auth_production = settings.get("basic_auth_production", "{}")
                        basic_auth_production_data = json.loads(basic_auth_production)
                        production_csid = get_production_csid_for_company(basic_auth_production_data, company_name)

                        if production_csid:
                            headers = {
                            'accept': 'application/json',
                            'accept-language': 'en',
                            'Clearance-Status': '1',
                            'Accept-Version': 'V2',
                            'Authorization': 'Basic' + production_csid,
                            # 'Authorization': 'Basic' + settings.basic_auth,
                            'Content-Type': 'application/json',
                            'Cookie': 'TS0106293e=0132a679c03c628e6c49de86c0f6bb76390abb4416868d6368d6d7c05da619c8326266f5bc262b7c0c65a6863cd3b19081d64eee99' }
                        else:
                            frappe.throw("Production CSID for company {} not found".format(company_name))
                        response = requests.request("POST", url=get_API_url(base_url="invoices/clearance/single"), headers=headers, data=payload)
                        
                        # response.status_code = 400
                        
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
                                pih_data = json.loads(settings.get("pih", "{}"))
                                updated_pih_data = update_json_data_pih(pih_data, company_name,encoded_hash)
                                settings.set("pih", json.dumps(updated_pih_data))
                                settings.save(ignore_permissions=True)
                                
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
                                success_Log(response.text,uuid1, invoice_number)
                                return xml_cleared
                        else:
                                error_Log()
                            
                    except Exception as e:
                        frappe.throw("error in clearance api:  " + str(e) )

