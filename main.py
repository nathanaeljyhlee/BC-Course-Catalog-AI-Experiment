import subprocess
import os

# Step 1 skipped — already done

# Step 2: Loop over PDFs for OCR
pdf_dir = "raw_splits"
ocr_script = "scripts/2_mistral_ocr.py"
pdf_files = sorted(f for f in os.listdir(pdf_dir) if f.endswith(".pdf"))
skip_file="BC_2023-24_part_1.pdf"

for i, pdf_file in enumerate(pdf_files, 1):
    if pdf_file == skip_file:
        print(f"⏭️ Skipping already processed file: {pdf_file}")
        continue
    print(f"\n▶️ [Step 2.{i}] OCR for {pdf_file}")
    result = subprocess.run(["python3", ocr_script, pdf_file])
    if result.returncode != 0:
        print(f"❌ Error during OCR for {pdf_file}. Halting pipeline.")
        break
else:
    # Step 3: Preview outputs
    print("\n▶️ Running: scripts/3_preview_outputs.py")
    result = subprocess.run(["python3", "scripts/3_preview_outputs.py"])
    if result.returncode != 0:
        print("❌ Error in preview step. Halting pipeline.")
    else:
        # Step 4: Parse JSON
        print("\n▶️ Running: scripts/4_parse_json.py")
        result = subprocess.run(["python3", "scripts/4_parse_json.py"])
        if result.returncode != 0:
            print("❌ Error in parsing step.")
        else:
            print("\n✅ All steps completed successfully.")
