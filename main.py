import subprocess

scripts = [
    "1_pdf_split.py",
    "2_mistral_ocr.py",
    "3_preview_outputs.py",
    "4_parse_json.py"
]

for script in scripts:
    print(f"▶️ Running: {script}")
    result = subprocess.run(["python3", script])
    if result.returncode != 0:
        print(f"❌ Error in {script}. Halting pipeline.")
        break
else:
    print("✅ All steps completed successfully.")
