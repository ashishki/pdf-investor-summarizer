from pypdf import PdfReader, PdfWriter

reader = PdfReader("tests/assets/company_report.pdf")
writer = PdfWriter()
for page_num in range(2):  
    writer.add_page(reader.pages[page_num])

with open("tests/assets/company_report_short.pdf", "wb") as f:
    writer.write(f)