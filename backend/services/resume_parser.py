import os

from pypdf import PdfReader


def extract_resume_text(file_path: str) -> str:

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            "Resume file not found"
        )

    reader = PdfReader(file_path)

    text = []

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text.append(page_text)

    final_text = "\n".join(text)

    if not final_text.strip():
        raise ValueError(
            "Could not extract text from this PDF"
        )

    return final_text.strip()