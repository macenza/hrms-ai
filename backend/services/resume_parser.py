import fitz
from docx import Document


def extract_pdf_text(file_path):
    text = ""

    pdf = fitz.open(file_path)

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text


def extract_docx_text(file_path):
    doc = Document(file_path)

    text = "\n".join([para.text for para in doc.paragraphs])

    return text


def extract_text(file_path):
    if file_path.endswith(".pdf"):
        return extract_pdf_text(file_path)

    elif file_path.endswith(".docx"):
        return extract_docx_text(file_path)

    else:
        raise ValueError("Unsupported file format")