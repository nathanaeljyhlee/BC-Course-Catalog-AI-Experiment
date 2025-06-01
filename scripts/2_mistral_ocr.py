import sys
import requests
import os
import base64
import json
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
    part_number = input("🔢 Enter part number (e.g., 1): ").strip()
else:
    part_number = sys.argv[1]

base_name = f"BC_2023-24_part_{part_number}"
pdf_filename = f"{base_name}.pdf"
pdf_path = os.path.join("raw_splits", pdf_filename)
output_path = os.path.join("json_results", f"{base_name}.json")

print(f"📁 Loading file: {pdf_path}")
if not os.path.exists(pdf_path):
    print(f"❌ File not found: {pdf_path}")
    sys.exit(1)

# === Encode PDF to base64 ===
try:
    with open(pdf_path, "rb") as f:
        encoded_pdf = base64.b64encode(f.read()).decode("utf-8")
except Exception as e:
    print(f"❌ Failed to read or encode PDF: {e}")
    sys.exit(1)

# === Prepare JSON payload ===
payload = {
    "model": "mistral-ocr-latest",
    "document": {
        "type": "document_url",
        "document_url": f"data:application/pdf;base64,{encoded_pdf}"
    },
    "include_image_base64": False
}

# === Send OCR request ===
print(f"📤 Sending OCR request for: {pdf_filename}")
try:
    response = requests.post(
        API_URL,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=500
    )
except Exception as e:
    print(f"❌ Exception during request: {e}")
    sys.exit(1)

# === Handle response ===
print(f"📥 Response status code: {response.status_code}")
if response.status_code == 200:
    os.makedirs("json_results", exist_ok=True)
    try:
        result_json = response.json()
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result_json, f, ensure_ascii=False, indent=2)
        print(f"✅ OCR successful — saved to: {output_path}")
    except Exception as e:
        print(f"❌ Failed to parse or write JSON: {e}")
        sys.exit(1)
else:
    print(f"❌ OCR failed for {pdf_filename}")
    print(f"🔎 Response body: {response.text}")
    sys.exit(1)