from flask import Flask, jsonify, request, render_template, send_file
from app.database import get_db
from data_extraction import InvoicesDetails
import os

app = Flask(__name__)
invObj = InvoicesDetails()
collection = get_db()

@app.route('/')
def home():
    return render_template('invoice_dashboard.html')

@app.route('/upload-invoice', methods=['POST'])
def upload_invoice():
    file = request.files['invoice_file']
    file_name = file.filename
    file_path = os.path.join('uploads', file_name)  
    file.save(file_path)

    result = invObj.get_invoice_details(file_path)
    result["File Name"] = file_name  

    response = collection.find_one({"Invoice Number": result["Invoice Number"]})
    
    if not response:
        collection.insert_one(result)
        return jsonify({"status": 'Success', "message": "Invoice stored successfully"})
    else:
        return jsonify({"status": 'Error', "message": "Invoice already exists"})

@app.route('/get-invoices/<username>', methods=['GET'])
def get_invoice(username):
    response = collection.find_one({"Client Name": username})
    
    if not response:
        return jsonify({"status": 'Error', "message": f"{username} doesn't exist"})
    else:
        return jsonify({
            "status": 'Success',
            "message": f"{username} exists",
            "invoice_id": response.get("Invoice Number", ""),
            "file_name": response.get("File Name", "")  
        })


@app.route('/invoice-details/<invoice_id>', methods=['GET'])
def get_invoice_id(invoice_id):
    invoice = collection.find_one({"Invoice Number": invoice_id})
    
    if not invoice:
        return jsonify({"status": 'Failed', "message": "Invoice ID not found"}), 404
    
    invoice['_id'] = str(invoice['_id'])
    return jsonify({
        "status": 'Success',
        "message": "Invoice found successfully",
        "invoice": {
            "_id": invoice.get("_id", ""),
            "Invoice Number": invoice.get("Invoice Number", ""),
            "Invoice Date": invoice.get("Invoice Date", ""),
            "Client Name": invoice.get("Client Name", ""),
            "Total Amount": invoice.get("Total Amount", ""),
            "Tax Amount": invoice.get("Tax Amount", ""),
            "File Name": invoice.get("File Name", "")  
        }
    }), 200

@app.route('/download-invoice/<invoice_id>', methods=['GET'])
def download_invoice(invoice_id):
    invoice = collection.find_one({"Invoice Number": invoice_id})
    
    if not invoice:
        return jsonify({"status": 'Failed', "message": "Invoice not found"})

    file_name = invoice.get("File Name", "")  
    file_path = os.path.join("uploads", file_name)

    if not os.path.exists(file_path):
        return jsonify({"status": 'Failed', "message": "File not found"})

    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082, debug=True)
