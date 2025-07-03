# src/pdf_investor_summarizer/merger.py

from typing import List, Dict, Any
import logging
logger = logging.getLogger(__name__)

class Merger:
    """
    Merges a list of extractor outputs into a single summary JSON.
    Assumes all inputs are dicts with the same set of keys and values are lists.
    """

    def merge(self, extracted_chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Combine all extracted chunk outputs by concatenating lists for each key.

        Parameters
        ----------
        extracted_chunks : List[dict]
            List of outputs from Extractor.extract()

        Returns
        -------
        dict
            Merged summary, with lists from all chunks concatenated for each field.
        """
        logger.info(f"Merging {len(extracted_chunks)} chunk results.")
        if not extracted_chunks:
            return {}
        merged = {key: [] for key in extracted_chunks[0].keys()}
        for chunk in extracted_chunks:
            for key, value in chunk.items():
                if isinstance(value, list):
                    merged[key].extend(value)
        logger.info(f"Merged summary: {merged}")
        return merged
