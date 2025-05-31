import PyPDF2

input_pdf = "catalog.pdf"
pages_per_split = 1000

reader = PyPDF2.PdfReader(input_pdf)
num_pages = len(reader.pages)
for i in range(0, num_pages, pages_per_split):
    writer = PyPDF2.PdfWriter()
    for j in range(i, min(i + pages_per_split, num_pages)):
        writer.add_page(reader.pages[j])
    with open(f"catalog_part_{i//pages_per_split + 1}.pdf", "wb") as out_file:
        writer.write(out_file)
print("PDF split complete.")
