# As of 5/31 (once you install PyPDF2)... it works!

import PyPDF2

# input name and parameters
input_pdf = "raw_splits/BC_2023-24.pdf"
pages_per_split = 1000

reader = PyPDF2.PdfReader(input_pdf)
num_pages = len(reader.pages)
for i in range(0, num_pages, pages_per_split):
    writer = PyPDF2.PdfWriter()
    for j in range(i, min(i + pages_per_split, num_pages)):
        writer.add_page(reader.pages[j])
    split_num = i // pages_per_split + 1
    filename = f"{input_pdf}_part_{split_num}.pdf"
    with open(filename, "wb") as out_file:
        writer.write(out_file)
    print(f"Saved: {filename}")

print("PDF split complete.")
