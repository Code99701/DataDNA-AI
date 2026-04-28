"""
Text extraction service for PDF, DOCX, and TXT files.

Extracts text on a per-page basis. For formats without native page breaks
(DOCX, TXT), pages are synthesized using character limits or form-feed markers.
"""
import os
import logging
from typing import List

from app.config import PAGE_CHAR_LIMIT

logger = logging.getLogger(__name__)


def extract_text_by_pages(file_path: str, file_ext: str) -> List[str]:
    """
    Extract text from a file, split into pages.

    Args:
        file_path: Absolute path to the file on disk.
        file_ext: File extension (e.g. ".pdf", ".docx", ".txt").

    Returns:
        List of strings, one per page. Empty pages are excluded.
    """
    ext = file_ext.lower().strip(".")

    if ext == "pdf":
        return _extract_pdf(file_path)
    elif ext == "docx":
        return _extract_docx(file_path)
    elif ext == "txt":
        return _extract_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: .{ext}. Supported: pdf, docx, txt")


def _extract_pdf(file_path: str) -> List[str]:
    """Extract text page-by-page from a PDF file."""
    from PyPDF2 import PdfReader

    reader = PdfReader(file_path)
    pages = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        text = text.strip()
        if text:
            pages.append(text)
        else:
            logger.warning(f"PDF page {i + 1} produced no extractable text — skipped")

    if not pages:
        raise ValueError("No text could be extracted from the PDF file.")

    logger.info(f"Extracted {len(pages)} pages from PDF: {os.path.basename(file_path)}")
    return pages


def _extract_docx(file_path: str) -> List[str]:
    """
    Extract text from a DOCX file, split into synthetic pages.

    Uses form-feed characters (\\f) as page breaks if present,
    otherwise splits by character limit.
    """
    from docx import Document

    doc = Document(file_path)
    full_text = "\n".join(para.text for para in doc.paragraphs)

    if not full_text.strip():
        raise ValueError("No text could be extracted from the DOCX file.")

    pages = _split_into_pages(full_text)
    logger.info(
        f"Extracted {len(pages)} pages from DOCX: {os.path.basename(file_path)}"
    )
    return pages


def _extract_txt(file_path: str) -> List[str]:
    """
    Extract text from a plain text file, split into synthetic pages.

    Uses form-feed characters (\\f) as page breaks if present,
    otherwise splits by character limit.
    """
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        full_text = f.read()

    if not full_text.strip():
        raise ValueError("The text file is empty.")

    pages = _split_into_pages(full_text)
    logger.info(
        f"Extracted {len(pages)} pages from TXT: {os.path.basename(file_path)}"
    )
    return pages


def _split_into_pages(text: str) -> List[str]:
    """
    Split text into pages using form-feed characters or character limits.

    If the text contains \\f (form feed), split on those.
    Otherwise, split into chunks of PAGE_CHAR_LIMIT characters,
    breaking at paragraph boundaries when possible.
    """
    # Try form-feed split first
    if "\f" in text:
        pages = [page.strip() for page in text.split("\f") if page.strip()]
        if pages:
            return pages

    # Fall back to character-limit chunking
    paragraphs = text.split("\n")
    pages = []
    current_page = ""

    for para in paragraphs:
        # If adding this paragraph would exceed the limit, start a new page
        if current_page and len(current_page) + len(para) + 1 > PAGE_CHAR_LIMIT:
            pages.append(current_page.strip())
            current_page = para
        else:
            current_page = current_page + "\n" + para if current_page else para

    # Don't forget the last page
    if current_page.strip():
        pages.append(current_page.strip())

    return pages
