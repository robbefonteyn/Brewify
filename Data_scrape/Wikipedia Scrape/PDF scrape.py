from PyPDF2 import PdfReader
import pandas as pd


pdfname = "Lijst_van_Belgische_bieren.pdf"

def extract_text(pdf_path, page_nr=None):
    pdf_reader = PdfReader(pdf_path)
    text = ""
    if not page_nr:
        for page in pdf_reader.pages:
            text += page.extractText()
        return text

    else:
        page = pdf_reader.pages[page_nr]
        text += page.extractText()
        return text


text = extract_text(pdfname, 2)

data = []
for line in text.splitlines():
    data.append(line)
print(data)




