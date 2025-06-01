import sys
import requests
import os
from dotenv import load_dotenv

# === Load API key ===
load_dotenv()
API_KEY = os.getenv("MISTRAL_API_KEY")
API_URL = "https://api.mistral.ai/v1/ocr"

if not API_KEY:
    print("❌ MISTRAL_API_KEY not found in .env.")
    sys.exit(1)

# === Handle CLI argument ===
if len(sys.argv) < 2:
    print("❌ Usage: python 2_mistral_ocr.py <PDF_FILENAME>")
    sys.exit(1)

filename = sys.argv[1]
pdf_path = os.path.join("raw_splits", filename)
output_path = os.path.join("json_results", filename.replace(".pdf", ".json"))

print(f"📁 Loading file: {pdf_path}")
if not os.path.exists(pdf_path):
    print(f"❌ File not found: {pdf_path}")
    sys.exit(1)

# === Send request ===
print(f"📤 Sending OCR request for: {filename}")
try:
    with open(pdf_path, "rb") as f:
        response = requests.post(
            API_URL,
            headers={"Authorization": f"Bearer {API_KEY}"},
            files={"document": f},
            data=[
                ("model", "mistral-ocr-latest"),
                ("include_image_base64", "false")
            ]
        )
except Exception as e:
    print(f"❌ Exception during request: {e}")
    sys.exit(1)

# === Handle response ===
print(f"📥 Response status code: {response.status_code}")
if response.status_code == 200:
    os.makedirs("json_results", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(response.text)
    print(f"✅ OCR successful — saved to: {output_path}")
else:
    print(f"❌ OCR failed for {filename}")
    print(f"🔎 Response body: {response.text}")
    sys.exit(1)
