import os
from flask import Flask, render_template, request, redirect, url_for, flash
import PyPDF2
from transformers import pipeline
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

# Initialize the Hugging Face model for question answering
qa_pipeline = pipeline("question-answering")

# Dummy storage for uploaded documents and chat responses (In-memory, for demonstration purposes)
uploaded_documents = []  # To store uploaded documents
chat_history = []        # To store chat history

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    allowed_extensions = {'pdf', 'txt'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        report_name = request.form['report_name']
        additional_notes = request.form.get('additional_notes', '')  # Optional field
        document_file = request.files['document_file']
        document_type = request.form['document_type']  # New field

        if document_file and allowed_file(document_file.filename):
            # Save the file to a specific location
            file_path = os.path.join('uploads', document_file.filename)
            document_file.save(file_path)

            # Store document information
            uploaded_documents.append({
                'name': report_name,
                'notes': additional_notes,
                'file': document_file.filename,
                'type': document_type  # Store document type
            })
            return redirect(url_for('upload_success', report_name=report_name))
        else:
            flash('No document uploaded or invalid file type', 'danger')
    return render_template('upload.html')

@app.route('/upload_success')
def upload_success():
    report_name = request.args.get('report_name')
    return render_template('upload_success.html', report_name=report_name)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query']
        results = perform_search(query)
        return render_template('search_results.html', query=query, results=results)
    return render_template('search.html')

def perform_search(query):
    occurrences = {}
    for doc in uploaded_documents:
        pdf_path = os.path.join('uploads', doc['file'])  # Path to the uploaded file
        count_per_page = search_in_document(query, pdf_path)
        
        # Only add to occurrences if there are matches
        if count_per_page:
            occurrences[doc['name']] = count_per_page  # Use document name as a key

    return occurrences

def search_in_document(query, file_path):
    occurrences = {}
    if file_path.endswith('.pdf'):
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in range(len(pdf_reader.pages)):
                    text = pdf_reader.pages[page].extract_text()
                    if text:
                        count = text.lower().count(query.lower())
                        if count > 0:
                            occurrences[page + 1] = count  # Store page number (1-indexed)
        except PyPDF2.errors.PdfReadError as e:
            print(f"Error reading {file_path}: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
    elif file_path.endswith('.txt'):
        try:
            with open(file_path, 'r') as file:
                text = file.read()
                count = text.lower().count(query.lower())
                if count > 0:
                    occurrences[1] = count  # All text is in one 'page'
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    return occurrences

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    global chat_history  # Declare chat_history as global to modify it
    if request.method == 'POST':
        message = request.form['message']
        response = process_chat(message)
        chat_history.append((message, response))  # Store the chat history
        return render_template('chat.html', message=message, response=response, chat_history=chat_history)
    return render_template('chat.html', chat_history=chat_history)

def process_chat(message):
    # Check if a document has been uploaded
    if not uploaded_documents:
        return "Please upload a document first."

    # Load the latest uploaded PDF
    latest_doc = uploaded_documents[-1]['file']
    pdf_path = os.path.join('uploads', latest_doc)

    # Extract text from the latest uploaded PDF
    text = extract_text_from_pdf(pdf_path)

    # Use the Hugging Face model for question answering
    result = qa_pipeline(question=message, context=text)
    return result['answer'] if 'answer' in result else "I'm not sure about that."

def extract_text_from_pdf(pdf_path):
    """Extract text from the PDF."""
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page].extract_text() + " "  # Concatenate text from all pages
    return text

if __name__ == '__main__':
    app.run(debug=True)
