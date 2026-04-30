# parser.py

import PyPDF2
import docx

def extract_text(file_path):
    text = ""

    try:
        # PDF
        if file_path.endswith(".pdf"):
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() or ""

        # DOCX
        elif file_path.endswith(".docx"):
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"

        else:
            return ""

    except Exception as e:
        print("Error reading file:", e)
        return ""

    return text.lower()
