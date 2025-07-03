# src/pdf_investor_summarizer/merger.py

from typing import List, Dict, Any

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
        if not extracted_chunks:
            return {}
        merged = {key: [] for key in extracted_chunks[0].keys()}
        for chunk in extracted_chunks:
            for key, value in chunk.items():
                if isinstance(value, list):
                    merged[key].extend(value)
                else:
                    # For fields like "evidence" (if present), just ignore or keep empty
                    pass
        # For "evidence", you could collect all evidences if needed
        if "evidence" in merged:
            merged["evidence"] = ""  # or optionally join all
        return merged
