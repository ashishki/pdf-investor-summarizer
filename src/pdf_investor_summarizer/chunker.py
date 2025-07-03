"""Chunk text into overlapping segments."""

from typing import List
import logging
logger = logging.getLogger(__name__)

class Chunker:
    """Splits text into fixed-size chunks with overlap.

    Parameters
    ----------
    chunk_size : int
        Maximum characters per chunk.
    overlap : int
        Overlap size between consecutive chunks.
    """

    def __init__(self, chunk_size: int = 4000, overlap: int = 400) -> None:
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split(self, text: str) -> List[str]:
        chunks: List[str] = []
        start = 0
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunks.append(text[start:end])
            logger.debug(f"Chunk {len(chunks)-1}: {repr(text[start:end][:100])} ...")
            if end == len(text):
                break
            step = self.chunk_size - self.overlap
            if step < 1:
                step = 1
            start += step
        return chunks

