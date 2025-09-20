import sys
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_pdf.py <path_to_pdf>")
        sys.exit(1)

    pdf_file = sys.argv[1]
    extracted_text = extract_text_from_pdf(pdf_file)
    print("------EXTRACTED TEXT START------")
    print(extracted_text)
    print("-------EXTRACTED TEXT END-------")

