from io import BytesIO

import docx
import PyPDF2


def extract_pdf_text(file_obj):
    reader = PyPDF2.PdfReader(file_obj)
    chunks = []
    for page in reader.pages:
        content = page.extract_text()
        if content:
            chunks.append(content)
    return "\n".join(chunks)


def extract_docx_text(file_obj):
    document = docx.Document(file_obj)
    return "\n".join(paragraph.text for paragraph in document.paragraphs)


def extract_text_from_upload(uploaded_file):
    try:
        file_name = uploaded_file.name.lower()
        file_bytes = uploaded_file.getvalue()
        file_obj = BytesIO(file_bytes)

        if file_name.endswith(".pdf"):
            text = extract_pdf_text(file_obj)
        elif file_name.endswith(".docx"):
            text = extract_docx_text(file_obj)
        else:
            return "", "Unsupported file type. Upload a PDF or DOCX resume."

        if not text.strip():
            return "", "Could not extract text from this resume. Try a text-based PDF or DOCX file."

        return text.lower(), ""
    except Exception as exc:
        return "", f"Could not read the resume file: {exc}"


def extract_text(file_path):
    try:
        with open(file_path, "rb") as file_obj:
            if file_path.lower().endswith(".pdf"):
                return extract_pdf_text(file_obj).lower()
            if file_path.lower().endswith(".docx"):
                return extract_docx_text(file_obj).lower()
    except Exception as exc:
        print("Error:", exc)
    return ""
