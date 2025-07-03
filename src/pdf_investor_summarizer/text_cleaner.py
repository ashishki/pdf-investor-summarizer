# src/pdf_investor_summarizer/text_cleaner.py

import re
from typing import List

class TextCleaner:
    """
    Cleans raw page text by removing headers, footers, short lines, and normalizing whitespace.
    """

    def __init__(self, min_line_length: int = 10):
        """
        Parameters
        ----------
        min_line_length : int
            Minimum length of a line (in characters) to keep.
        """
        self.min_line_length = min_line_length
        self.page_number_pattern = re.compile(r"^\s*\d+\s*$")

    def clean(self, text: str) -> str:
        """
        Clean a single page's text.

        Steps:
        1. Split into lines.
        2. Remove empty lines.
        3. Remove lines shorter than min_line_length.
        4. Remove lines that contain only page numbers.
        5. Collapse multiple spaces into one.
        6. Join all remaining lines into one string separated by a space.
        """
        lines = text.splitlines()
        cleaned_lines: List[str] = []
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            if self.page_number_pattern.match(stripped):
                continue
            if len(stripped) < self.min_line_length:
                continue
            normalized = re.sub(r"\s+", " ", stripped)
            cleaned_lines.append(normalized)
        return " ".join(cleaned_lines)

    def clean_pages(self, pages: List[str]) -> List[str]:
        """
        Apply clean() to a list of page texts.
        Returns a new list of cleaned page texts.
        """
        return [self.clean(page) for page in pages]

