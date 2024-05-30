import os
import frappe
from lxml import etree
from frappe.utils import get_files_path

def generate_invoice_xml(doc, method):

    print(doc)
    # Define the namespaces as per ZATCA requirements
    nsmap = {
        'inv': "urn:oasis:names:specification:ubl:schema:xsd:Invoice-2",
        'cac': "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        'cbc': "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        'ext': "urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2",
        'sig': "urn:oasis:names:specification:ubl:schema:xsd:CommonSignatureComponents-2",
        'sac': "urn:oasis:names:specification:ubl:schema:xsd:SignatureAggregateComponents-2",
        'sbc': "urn:oasis:names:specification:ubl:schema:xsd:SignatureBasicComponents-2"
    }

    # Create the root element with namespaces
    root = etree.Element("{urn:oasis:names:specification:ubl:schema:xsd:Invoice-2}Invoice", nsmap=nsmap)

    # Add the UBLExtensions
    extensions = etree.SubElement(root, "{urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2}UBLExtensions")
    extension = etree.SubElement(extensions, "{urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2}UBLExtension")
    ext_content = etree.SubElement(extension, "{urn:oasis:names:specification:ubl:schema:xsd:CommonExtensionComponents-2}ExtensionContent")
    signatures = etree.SubElement(ext_content, "{urn:oasis:names:specification:ubl:schema:xsd:CommonSignatureComponents-2}UBLDocumentSignatures")
    signature_info = etree.SubElement(signatures, "{urn:oasis:names:specification:ubl:schema:xsd:SignatureAggregateComponents-2}SignatureInformation")
    signature_id = etree.SubElement(signature_info, "{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID")
    signature_id.text = "urn:oasis:names:specification:ubl:signature:1"
    # Add other signature elements as needed...

    # Add invoice basic details
    profile_id = etree.SubElement(root, "{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ProfileID")
    profile_id.text = "reporting:1.0"
    invoice_id_elem = etree.SubElement(root, "{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID")
    invoice_id_elem.text = doc.name
    issue_date = etree.SubElement(root, "{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}IssueDate")
    issue_date.text = str(doc.posting_date)
    issue_time = etree.SubElement(root, "{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}IssueTime")
    issue_time.text = str(doc.posting_time)
    currency_code = etree.SubElement(root, "{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}DocumentCurrencyCode")
    currency_code.text = doc.currency

    # Add Supplier and Customer information
    supplier_party = etree.SubElement(root, "{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}AccountingSupplierParty")
    supplier = etree.SubElement(supplier_party, "{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}Party")
    supplier_id = etree.SubElement(supplier, "{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PartyIdentification")
    supplier_id_value = etree.SubElement(supplier_id, "{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID", schemeID="VAT")
    supplier_id_value.text = doc.company_tax_id  # Supplier VAT ID

    # Add Customer information
    customer_party = etree.SubElement(root, "{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}AccountingCustomerParty")
    customer = etree.SubElement(customer_party, "{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}Party")
    customer_id = etree.SubElement(customer, "{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}PartyIdentification")
    customer_id_value = etree.SubElement(customer_id, "{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID", schemeID="VAT")
    customer_id_value.text = doc.tax_id  # Customer VAT ID

    # Add tax total
    tax_total = etree.SubElement(root, "{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}TaxTotal")
    tax_amount = etree.SubElement(tax_total, "{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}TaxAmount", currencyID=doc.currency)
    tax_amount.text = str(doc.total_taxes_and_charges)

    # Add LegalMonetaryTotal
    legal_monetary_total = etree.SubElement(root, "{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}LegalMonetaryTotal")
    line_extension_amount = etree.SubElement(legal_monetary_total, "{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}LineExtensionAmount", currencyID=doc.currency)
    line_extension_amount.text = str(doc.total)

    tax_inclusive_amount = etree.SubElement(legal_monetary_total, "{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}TaxInclusiveAmount", currencyID=doc.currency)
    tax_inclusive_amount.text = str(doc.grand_total)

    # Add Invoice Lines
    for item in doc.items:
        invoice_line = etree.SubElement(root, "{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}InvoiceLine")
        id_elem = etree.SubElement(invoice_line, "{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID")
        id_elem.text = str(item.idx)
        quantity = etree.SubElement(invoice_line, "{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}InvoicedQuantity", unitCode=item.uom)
        quantity.text = str(item.qty)
        line_extension_amount = etree.SubElement(invoice_line, "{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}LineExtensionAmount", currencyID=doc.currency)
        line_extension_amount.text = str(item.amount)
        item_name = etree.SubElement(invoice_line, "{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}Name")
        item_name.text = item.item_name

        # Add tax subtotal for each item
        tax_total = etree.SubElement(invoice_line, "{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}TaxTotal")
        tax_subtotal = etree.SubElement(tax_total, "{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}TaxSubtotal")
        tax_amount = etree.SubElement(tax_subtotal, "{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}TaxAmount", currencyID=doc.currency)
        tax_amount.text = str(item.amount)
        tax_category = etree.SubElement(tax_subtotal, "{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}TaxCategory")
        tax_scheme = etree.SubElement(tax_category, "{urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2}TaxScheme")
        tax_scheme_id = etree.SubElement(tax_scheme, "{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}ID")
        tax_scheme_id.text = "VAT"
        tax_scheme_name = etree.SubElement(tax_scheme, "{urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2}Name")
        tax_scheme_name.text = "VAT"

    # Convert the XML to string
    xml_string = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8")

    # Define the file path
    file_name = f"Invoice_{doc.name}.xml"
    file_path = os.path.join(get_files_path(is_private=True), file_name)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Save the XML to the file
    with open(file_path, "wb") as f:
        f.write(xml_string)

    # Optionally, attach the file to the Sales Invoice
    # frappe.get_doc({
    #     "doctype": "File",
    #     "file_name": file_name,
    #     "file_url": "/private/files/" + file_name,
    #     "attached_to_doctype": "Sales Invoice",
    #     "attached_to_name": doc.name
    # }).insert()

    frappe.msgprint(f"XML file for Sales Invoice {doc.name} has been created and saved at {file_path}")

# Example usage (this function will be automatically called via hooks)
# generate_and_save_invoice_xml("INV-0001")  # Replace with actual invoice ID
