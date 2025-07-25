from pathlib import Path
from typing import List, Union
import tempfile
import requests
import logging
logger = logging.getLogger(__name__)

from pdfminer.high_level import extract_text
from pypdf import PdfReader
from pdf2image import convert_from_path
import pytesseract

SourceType = Union[Path, str, bytes]

class PdfLoader:
    """
    Loads text from a PDF, page by page, with optional OCR fallback.
    Supports:
      - Local Path objects
      - HTTP/HTTPS URLs (as str)
      - Raw PDF bytes from a database
    """

    def __init__(
        self,
        source: SourceType,
        ocr_lang: str = "eng",
        ocr_dpi: int = 300,
    ):
        self.ocr_lang = ocr_lang
        self.ocr_dpi = ocr_dpi

        # Determine the source type and prepare a local file path
        if isinstance(source, Path):
            self.pdf_path = source
        elif isinstance(source, bytes):
            tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
            tmp.write(source)
            tmp.flush()
            self.pdf_path = Path(tmp.name)
        elif isinstance(source, str) and source.lower().startswith(("http://", "https://")):
            response = requests.get(source)
            response.raise_for_status()
            
            if not response.content.startswith(b"%PDF"):
                with open("downloaded_gdrive_response.html", "wb") as f:
                    f.write(response.content)
                raise ValueError("Downloaded file is not a valid PDF. Saved as downloaded_gdrive_response.html for inspection.")
            tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
            tmp.write(response.content)
            tmp.flush()
            self.pdf_path = Path(tmp.name)
            
        elif isinstance(source, str) and Path(source).exists():
            self.pdf_path = Path(source)
        else:
            raise ValueError(f"Unsupported source type: {type(source)}")


    def load(self) -> List[str]:
        logger.info(f"Extracting text from: {self.pdf_path}")
        reader = PdfReader(str(self.pdf_path))
        num_pages = len(reader.pages)
        logger.info(f"PDF has {num_pages} pages.")
        texts: List[str] = []

        for i in range(num_pages):
            page_text = extract_text(str(self.pdf_path), page_numbers=[i])
            if page_text and page_text.strip():
                logger.debug(f"Page {i} extracted with text (length={len(page_text)}).")
                texts.append(page_text)
            else:
                logger.warning(f"Page {i} is empty, fallback to OCR.")
                texts.append(self._ocr_page(i + 1))
        return texts



    def _ocr_page(self, page_number: int) -> str:
        """
        Convert one page to image and run Tesseract OCR.

        Parameters
        ----------
        page_number : int
            1-based page number (for pdf2image)

        Returns
        -------
        str
            Text extracted via OCR.
        """
        images = convert_from_path(
            str(self.pdf_path),
            dpi=self.ocr_dpi,
            first_page=page_number,
            last_page=page_number,
            fmt="jpeg",
        )
        if not images:
            return ""
        return pytesseract.image_to_string(images[0], lang=self.ocr_lang)
