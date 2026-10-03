from pathlib import Path
import re

from pypdf import PdfReader
from docx import Document


def clean_extracted_text(text):
    """Clean and normalize extracted resume text."""

    if not text:
        return ""

    # Normalize line breaks
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove excessive spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Remove spaces around lines
    lines = [line.strip() for line in text.split("\n")]

    # Remove empty lines
    lines = [line for line in lines if line]

    return "\n".join(lines).strip()


def extract_text_from_pdf(file_path):
    """Extract text from a PDF resume."""

    reader = PdfReader(file_path)

    text = []

    for page_number, page in enumerate(reader.pages, start=1):

        try:
            page_text = page.extract_text()

            if page_text:
                text.append(page_text)

        except Exception as e:
            print(
                f"Warning: Could not extract page "
                f"{page_number}: {e}"
            )

    extracted_text = "\n".join(text)

    return clean_extracted_text(extracted_text)


def extract_text_from_docx(file_path):
    """Extract text from a DOCX resume."""

    document = Document(file_path)

    text = []

    # Extract normal paragraphs
    for paragraph in document.paragraphs:

        paragraph_text = paragraph.text.strip()

        if paragraph_text:
            text.append(paragraph_text)

    # Extract text from tables
    for table in document.tables:

        for row in table.rows:

            row_text = []

            for cell in row.cells:

                cell_text = cell.text.strip()

                if cell_text:
                    row_text.append(cell_text)

            if row_text:
                text.append(" | ".join(row_text))

    extracted_text = "\n".join(text)

    return clean_extracted_text(extracted_text)


def extract_resume_text(file_path):
    """Extract and clean resume text based on file type."""

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    if file_path.stat().st_size == 0:
        raise ValueError(
            "The uploaded resume file is empty."
        )

    extension = file_path.suffix.lower()

    if extension == ".pdf":

        text = extract_text_from_pdf(file_path)

    elif extension == ".docx":

        text = extract_text_from_docx(file_path)

    else:

        raise ValueError(
            "Unsupported file type. Please use PDF or DOCX."
        )

    # Make sure extraction actually produced text
    if not text.strip():

        raise ValueError(
            "Could not extract readable text from this resume. "
            "The PDF may be scanned/image-based or the document "
            "may contain unsupported formatting."
        )

    return text