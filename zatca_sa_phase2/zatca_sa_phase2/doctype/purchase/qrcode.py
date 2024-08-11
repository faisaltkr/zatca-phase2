import base64
# import qrcode
import frappe
from zatca_sa_phase2.zatca_sa_phase2.doctype.csr_settings.utils.get_values import get_zatca_settings
from datetime import datetime, timezone

# Get current UTC time

# Format the time in ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)
def get_tlv(tag_num, tag_value):
    tag_buf = bytes([tag_num])
    tag_value_len_buf = bytes([len(tag_value)])
    tag_value_buf = tag_value.encode('utf-8')
    return tag_buf + tag_value_len_buf + tag_value_buf

def generate_qr_code_base_64(invoice_number):
    purchase_invoice = frappe.get_doc('Purchase Invoice' ,invoice_number)
    print(purchase_invoice,"sdfjdhfgbdkfgbb")
    company_details = get_zatca_settings()
    seller_name = company_details['company_name']
    vat_registration_number = company_details['vat_registration_number']
    current_time = datetime.now(timezone.utc)
    invoice_date = current_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    print("posting data",invoice_date)
    invoice_total = str(purchase_invoice.total)
    vat_total = str(purchase_invoice.total_taxes_and_charges)
    total_with_vat = str(purchase_invoice.outstanding_amount)  # Total Invoice Amount including VAT

    tlv_data = b''.join([
        get_tlv(1, seller_name),
        get_tlv(2, vat_registration_number),
        get_tlv(3, invoice_date),
        get_tlv(4, invoice_total),
        get_tlv(5, vat_total),
        get_tlv(6, total_with_vat)  # Add total_with_vat as tag 6
    ])
    qr_code_data = base64.b64encode(tlv_data).decode('utf-8')
    print(qr_code_data,"dkjfhdkkfgkj")
    return qr_code_data