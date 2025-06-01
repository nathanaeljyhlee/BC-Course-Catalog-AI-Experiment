# As of 5/31 (once you install PyPDF2)... it works!

import PyPDF2

# Prompt user for school/year prefix
prefix = input("Enter school and year (e.g., BC_2023-24): ").strip()

input_pdf = "raw_pdfs/First_Catalog.pdf"
pages_per_split = 1000

reader = PyPDF2.PdfReader(input_pdf)
num_pages = len(reader.pages)
for i in range(0, num_pages, pages_per_split):
    writer = PyPDF2.PdfWriter()
    for j in range(i, min(i + pages_per_split, num_pages)):
        writer.add_page(reader.pages[j])
    split_num = i // pages_per_split + 1
    filename = f"{prefix}_part_{split_num}.pdf"
    with open(filename, "wb") as out_file:
        writer.write(out_file)
    print(f"Saved: {filename}")

print("PDF split complete.")
