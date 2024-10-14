
import PyPDF2
import os

def extract_text_from_pdf(pdf_path):
    text = {}
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in range(len(pdf_reader.pages)):
            text[page + 1] = pdf_reader.pages[page].extract_text() or ""
    return text

def search_in_document(term, pdf_path):
    occurrences = {}
    text = extract_text_from_pdf(pdf_path)
    
    for page, content in text.items():
        count = content.lower().count(term.lower())
        if count > 0:
            occurrences[page] = count
    
    return occurrences

def highlight_term_in_pdf(pdf_path, term, output_path):
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from PyPDF2 import PdfWriter, PdfReader

    temp_pdf = "temp.pdf"
    c = canvas.Canvas(temp_pdf, pagesize=letter)

    with open(pdf_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        pdf_writer = PdfWriter()

        for page in range(len(pdf_reader.pages)):
            pdf_page = pdf_reader.pages[page]
            pdf_writer.add_page(pdf_page)

            # Extract text and highlight occurrences
            text = pdf_page.extract_text()
            if term.lower() in text.lower():
                # Highlight logic (this can be adjusted for precise positioning)
                y_position = 750  # Starting Y position for highlights (you may adjust this based on layout)
                for line in text.split('\n'):
                    if term.lower() in line.lower():
                        start_index = line.lower().find(term.lower())
                        c.setFillColorRGB(1, 1, 0)  # Highlight color (yellow)
                        c.rect(72 + start_index * 7, y_position, len(term) * 7, 15, fill=True)  # Basic highlight rectangle
                        c.setFillColorRGB(0, 0, 0)  # Reset color
                    y_position -= 15  # Move down for the next line

            c.showPage()  # Save the current page

        c.save()
    
    with open(temp_pdf, 'rb') as f:
        temp_reader = PdfReader(f)
        for page in range(len(temp_reader.pages)):
            pdf_writer.add_page(temp_reader.pages[page])
    
    with open(output_path, 'wb') as f:
        pdf_writer.write(f)
    
    # Remove temporary file
    os.remove(temp_pdf)
