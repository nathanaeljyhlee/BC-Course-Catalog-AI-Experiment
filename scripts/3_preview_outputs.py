# Works well!

import json

with open("json_results/output.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for page in data["pages"][570:580]:
    print("\n--- Page", page["index"], "---\n")
    print(page["markdown"][:1000])  # Print first 1000 chars for preview
