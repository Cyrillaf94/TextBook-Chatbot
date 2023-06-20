from PyPDF2 import PdfReader, PdfWriter
import pdfplumber

def copy_pdf_section(pdf_path, start, end, name):
    page_numbers = list(range(start, end))
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    for page_number in page_numbers:
        page = reader.pages[page_number]
        writer.add_page(page)

    with open(f"data/raw/{name}.pdf", "wb") as output_pdf:
        writer.write(output_pdf)

def get_pdf_outline(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        outline = list(pdf.doc.get_outlines())
    return outline



if __name__ == '__main__':
    copy_pdf_section('data/raw/First Aid for the USMLE Step 1 2019.pdf', 373, 417, 'Gastrointestinal')
