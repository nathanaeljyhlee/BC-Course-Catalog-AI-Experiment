import requests
import base64
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_URL = "https://api.mistral.ai/v1/ocr"
API_KEY = os.getenv("MISTRAL_API_KEY")
PDF_PATH = "raw_pdfs/BC_2023-24_part_1.pdf"  # Replace with your actual PDF path

# Read and encode the PDF file
with open(PDF_PATH, "rb") as pdf_file:
    encoded_pdf = base64.b64encode(pdf_file.read()).decode("utf-8")

# Construct the JSON payload
payload = {
    "model": "mistral-ocr-latest",
    "document": {
        "type": "document_url",
        "document_url": f"data:application/pdf;base64,{encoded_pdf}"
    },
    "include_image_base64": False
}

# Set the headers
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Send the POST request
response = requests.post(API_URL, headers=headers, json=payload)

# Handle the response
if response.status_code == 200:
    os.makedirs("json_results", exist_ok=True)
    output_path = os.path.join("json_results", "output.json")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(response.text)
        print("Base64 size (MB):", len(encoded_pdf) / (1024 * 1024))
    print(f"Success! JSON saved to {output_path}")
else:
    print(f"Error {response.status_code}: {response.text}")
