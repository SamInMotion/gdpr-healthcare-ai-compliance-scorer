import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """
    Extract all text from a PDF file using PyMuPDF.
    
    Args:
        pdf_path (str): Path to the PDF file.
        
    Returns:
        str: Extracted text from all pages.
    """
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Example usage
if __name__ == "__main__":
    pdf_file = "test_docs/sample.pdf"  # Replace with your test PDF
    extracted_text = extract_text_from_pdf(pdf_file)
    print(extracted_text)
