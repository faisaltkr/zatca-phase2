import frappe
from frappe import _
from frappe.utils.pdf import get_pdf
import base64
from io import BytesIO
import pikepdf

@frappe.whitelist()
def generate_sales_invoice_a3_pdf(docname):
    try:
        # Get the Sales Invoice document
        doc = frappe.get_doc("Sales Invoice", docname)
        qr_attachment = None
        qr_files = frappe.get_all('File', filters={
            'attached_to_doctype': 'Sales Invoice',
            'attached_to_name': doc.name,
            'file_name': ('like', 'QR%')  # Assuming QR file has 'QR' in its name
        })

        # If no QR file is attached, raise an error
        if not qr_files:
            frappe.throw(_("No QR code attached to the Sales Invoice."))

        # Read the QR code image
        qr_attachment = qr_files[0]  # Assume there is only one QR file
        qr_file_doc = frappe.get_doc("File", qr_attachment['name'])

        # Read the QR code image content
        with open(qr_file_doc.get_full_path(), "rb") as qr_file:
            qr_image = qr_file.read()
        xml_attachment = None
        attached_files = frappe.get_all('File', filters={
            'attached_to_doctype': 'Sales Invoice',
            'attached_to_name': doc.name,
            'file_name': ('like', '%xml')  # Filter files with '.xml' extension
        })

        # If no XML file is attached, raise an error
        if not attached_files:
            frappe.throw(_("No XML file attached to the Sales Invoice."))
        print(attached_files)
        # Read the XML content from the file
        xml_attachment = attached_files[0]  # Assume there is only one XML file
        file_doc = frappe.get_doc("File", xml_attachment['name'])
        
        
        # Read the XML file content
        with open(file_doc.get_full_path(), "rb") as xml_file:
            xml_content = xml_file.read()
        

        # Get company address (optional)
        company_address = frappe.get_doc("Address", 
            frappe.get_value("Dynamic Link", 
                {"link_doctype": "Company", "link_name": doc.company}, "parent"))
        
        # Prepare template data
        template_data = {
            "doc": doc,
            "company_address": company_address.address_line1,  # Adjust as necessary
            "print_date": frappe.utils.now_datetime(),  # Or any date format you prefer
            "qr_image_data": base64.b64encode(qr_image).decode('utf-8')  # Pass QR image as base64

        }

        # Get HTML content from the template
        html = frappe.get_template("templates/sales_invoice_a3.html").render(template_data)

        # A3 PDF options
        options = {
            'page-size': 'A3',  # Set to A3
            'orientation': 'Portrait',  # or 'Landscape' if needed
            'margin-top': '20mm',
            'margin-right': '20mm',
            'margin-bottom': '20mm',
            'margin-left': '20mm',
            'encoding': 'UTF-8',
            'no-outline': None,
            'enable-local-file-access': None,
            'zoom': 1.0,  # Adjust zoom level if needed
            'dpi': 300,  # Higher DPI for better quality
            'print-media-type': None,
            'enable-javascript': None,
            'javascript-delay': 1000,
            'enable-smart-shrinking': None
        }

        # Generate PDF from the HTML content
        pdf = get_pdf(html, options)
        pdf_stream = BytesIO(pdf)

        # Open the generated PDF with pikepdf
        pdf_with_xml = pikepdf.Pdf.open(pdf_stream)

        # Attach the XML content as an embedded file in the PDF
        pdf_with_xml.attachments["invoice.xml"] = xml_content

        # Save the PDF with XML attached
        output_pdf_stream = BytesIO()
        pdf_with_xml.save(output_pdf_stream)

        # Get the PDF as bytes to return
        pdf_with_xml_bytes = output_pdf_stream.getvalue()
        # Check if the PDF is generated successfully
        if not pdf:
            frappe.throw(_("Failed to generate the PDF."))

        # Set the response headers for the PDF file download
        frappe.local.response.filename = f"{doc.name}_A3.pdf"  # Set PDF filename
        frappe.local.response.filecontent = pdf  # The actual PDF binary content
        frappe.local.response["Content-Type"] = "application/pdf"  # Set the content type to PDF
        frappe.local.response["Content-Disposition"] = f"attachment; filename={doc.name}_A3.pdf"  # This triggers the download
        frappe.local.response.skip_log = True  # Prevent logging the file content
        pdf_base64 = base64.b64encode(pdf_with_xml_bytes).decode('utf-8')

        # Return the PDF binary content to the frontend
        return pdf_base64  # Return the binary PDF content directly

    except Exception as e:
        # Log the error and show a message to the user
        frappe.log_error(message=f"Error generating A3 PDF: {str(e)}", 
                         title="Sales Invoice A3 PDF Generation Error")
        frappe.throw(_("Error generating A3 PDF. Please check error logs."))
