# Knowledge-Based Search and Retrieval System

## Project Description
This project is a **Knowledge-Based Search and Retrieval System** that allows users to upload PDF and TXT documents, search for specific terms, and explore document content. Built using **Flask** and **Hugging Face Transformers**, it processes documents to make them searchable and interactive.

## Features
- **Document Upload**: Users can upload PDF files.
- **Search Functionality**: Allows users to search for terms in uploaded documents and returns the relevant pages.
- - **Chat Functionality**: Users can interact with the system through a chat interface, asking questions about the content of the uploaded documents, which are processed using a language model for responses.


## Setup Instructions

### 1. Clone the Repository
First, clone the repository to your local machine:
```bash
git clone https://github.com/YelavarthiLalitya/Knowledge-Based-Search-Retrieval-System.git
cd Knowledge-Based-Search-Retrieval-System
```

### 2. Create a Virtual Environment
Set up a virtual environment to isolate the dependencies:
```bash
python -m venv venv
source venv/bin/activate   # For Linux/MacOS
venv\Scripts\activate      # For Windows
```

### 3. Install Dependencies
Install the required dependencies listed in the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the root directory of your project to store environment variables like the OpenAI API key.

Your `.env` file should look like this:
```
OPENAI_API_KEY=your_openai_api_key_here
```

This key is required for the interaction with Hugging Face and OpenAI’s language models.

### 5. Run the App
To start the Flask application, run the following command:
```bash
python app.py
```

After running the app, navigate to `http://127.0.0.1:5000/` in your browser to use the system.

## Environment Variables
- **OPENAI_API_KEY**: You need to add your OpenAI API key in the `.env` file. This key will allow the system to access Hugging Face models via the transformers library.

## Technologies Used
- **Flask**: For the backend server.
- **Hugging Face Transformers**: For NLP tasks like text processing and search.
- **PyPDF2**: For extracting text from PDF files.
- **Python-dotenv**: To load environment variables from the `.env` file.
```
