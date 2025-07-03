# src/pdf_investor_summarizer/report_analyzer.py

from pathlib import Path
from typing import Union, List, Dict, Any

from src.pdf_investor_summarizer.pdf_loader import PdfLoader
from src.pdf_investor_summarizer.text_cleaner import TextCleaner
from src.pdf_investor_summarizer.chunker import Chunker
from src.pdf_investor_summarizer.extractor import Extractor
from src.pdf_investor_summarizer.merger import Merger

class ReportAnalyzer:
    """
    Full pipeline for extracting investment-relevant info from a company report PDF.
    """

    def __init__(
        self,
        chunk_size: int = 4000,
        overlap: int = 400,
        min_line_length: int = 10,
        extractor_kwargs: dict = None,
    ):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.cleaner = TextCleaner(min_line_length=min_line_length)
        self.extractor = Extractor(**(extractor_kwargs or {}))
        self.merger = Merger()

    def analyze(self, source: Union[str, Path, bytes]) -> Dict[str, Any]:
        """
        Run the full extraction pipeline on a PDF source.

        Returns
        -------
        dict
            Summary with all key fields.
        """
        # Step 1: Load pages (strings) from PDF
        pages = PdfLoader(source).load()

        # Step 2: Clean each page
        cleaned_pages = self.cleaner.clean_pages(pages)

        # Step 3: Concatenate cleaned text for chunking
        full_text = "\n".join(cleaned_pages)

        # Step 4: Split into overlapping chunks
        chunks = Chunker(self.chunk_size, self.overlap).split(full_text)

        # Step 5: Extract info from each chunk (with caching)
        results: List[dict] = [self.extractor.extract(chunk) for chunk in chunks]

        # Step 6: Merge all partial results into one summary
        summary = self.merger.merge(results)
        return summary
