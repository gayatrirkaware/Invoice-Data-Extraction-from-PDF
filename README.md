# Invoice-Data-Extraction-from-PDF


This is a Flask-based API designed to handle invoice uploads, retrieval, and downloads. The application extracts invoice details from uploaded files, stores them in a database, and provides endpoints for querying and downloading invoices.

## Features

- Upload invoices and extract details
- Store invoice details in a database
- Retrieve invoices by client name or invoice number
- Download stored invoices

## Installation

1. Clone this repository:
   ```sh
   git clone https://github.com/gayatrirkaware/Invoice-Data-Extraction-from-PDF.git
   cd Invoice-Data-Extraction-from-PDF
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Set up the database and ensure the necessary collections are created.

4. Run the application:
   ```sh
   python main.py
   ```

## API Endpoints

### Home Page
- **`GET /`** - Renders the invoice dashboard.

### Upload Invoice
- **`POST /upload-invoice`**  
  - Upload an invoice file to extract details and store it in the database.
  - Expects form data containing the file (`invoice_file`).

### Retrieve Invoice by Client Name
- **`GET /get-invoices/<username>`**  
  - Retrieves invoice details for a specific client.
  - Returns invoice number and file name if the client exists.

### Retrieve Invoice by Invoice Number
- **`GET /invoice-details/<invoice_id>`**  
  - Returns detailed invoice information for a given invoice number.

### Download Invoice File
- **`GET /download-invoice/<invoice_id>`**  
  - Allows downloading of the original invoice file.

## Directory Structure

```
/uploads              # Directory to store uploaded invoice files
/app
   /database.py       # Handles database connections
/templates
   /invoice_dashboard.html  # Dashboard template
data_extraction.py    # Handles extraction of invoice details
app.py                # Main Flask application
requirements.txt      # Dependencies
```

## Dependencies

Ensure you have the following dependencies installed:

- Flask
- pymongo
- Other necessary libraries mentioned in `requirements.txt`

## Running the Application

Start the Flask application:
```sh
python main.py
```

By default, the application runs on `http://0.0.0.0:8082`.


