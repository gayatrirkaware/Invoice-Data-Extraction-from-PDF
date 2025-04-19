import PyPDF2
import re
import os

class InvoicesDetails():
    def extract_text_from_pdf(self,pdf_file_path):
        with open(pdf_file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            self.text = ""
            for page in reader.pages:
                self.text += page.extract_text() + "\n"
        return self.text

    def extract_invoice_details(self,text):
        data = {}

        invoice_no_match = re.search(r'Invoice Number\s*:\s*(\S+)', self.text)
        if invoice_no_match:
            data['Invoice Number'] = invoice_no_match.group(1)

        invoice_date_match = re.search(r'Invoice Date\s*:\s*(\d{2}.\d{2}.\d{4})', self.text)
        if invoice_date_match:
            data['Invoice Date'] = invoice_date_match.group(1)

    
        client_name_match = re.search(r'Billing Address\s*:\s*(.*?)\n', self.text)
        if client_name_match:
            data['Client Name'] = client_name_match.group(1)

        
        amount_match = re.search(r'Invoice Value\s*:\s*([\d,.]+)', self.text)
        if amount_match:
            data['Total Amount'] = amount_match.group(1)

        
        tax_match = re.search(r'TOTAL:\s*₹([\d,.]+)', self.text)
        if tax_match:
            data['Tax Amount'] = tax_match.group(1)

        return data
    

    def get_invoice_details(self,pdf_file_path):
        res = self.extract_text_from_pdf(pdf_file_path)
        return self.extract_invoice_details(res)
        # print(self.extract_invoice_details(res))

# obj = InvoicesDetails()
# pdf_file_path = r"C:\Users\Tribhushan\Downloads\invoices.pdf"
# obj.get_invoice_details(pdf_file_path)
