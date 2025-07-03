# src/pdf_investor_summarizer/report_analyzer.py

import os
from pathlib import Path
from typing import Union, List, Dict, Any
import asyncio
import logging

logger = logging.getLogger(__name__)

from src.pdf_investor_summarizer.pdf_loader import PdfLoader
from src.pdf_investor_summarizer.text_cleaner import TextCleaner
from src.pdf_investor_summarizer.chunker import Chunker
from src.pdf_investor_summarizer.extractor import Extractor
from src.pdf_investor_summarizer.merger import Merger
from src.pdf_investor_summarizer.utils.cost import count_tokens

from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
pdf_url = os.getenv("PDF_SOURCE_URL")


def estimate_total_cost(prompt_tokens: int, completion_tokens: int, prompt_per_1k: float, completion_per_1k: float) -> float:
    """
    Estimate total cost in $ given prompt and completion tokens and prices per 1k tokens.
    """
    return (prompt_tokens / 1000) * prompt_per_1k + (completion_tokens / 1000) * completion_per_1k


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
        Synchronous version for backward compatibility.
        """
        pages = PdfLoader(source).load()
        cleaned_pages = self.cleaner.clean_pages(pages)
        full_text = "\n".join(cleaned_pages)
        chunks = Chunker(self.chunk_size, self.overlap).split(full_text)
        results: List[dict] = [self.extractor.extract(chunk) for chunk in chunks]
        summary = self.merger.merge(results)
        return summary

    async def analyze_async(self, source: Union[str, Path, bytes]) -> Dict[str, Any]:
        logger.info(f"PDF loading: {source} (type: {type(source)})")
        pages = PdfLoader(source).load()
        logger.info(f"Loaded {len(pages)} pages from PDF.")

        cleaned_pages = self.cleaner.clean_pages(pages)
        logger.info(f"Cleaned pages. Example [0]: {cleaned_pages[0][:200] if cleaned_pages else '<EMPTY>'}")

        full_text = "\n".join(cleaned_pages)
        logger.info(f"Full text length after cleaning: {len(full_text)}")

        chunks = Chunker(self.chunk_size, self.overlap).split(full_text)
        logger.info(f"Chunking complete: {len(chunks)} chunks.")
        for i, chunk in enumerate(chunks):
            logger.debug(f"Chunk[{i}] ({len(chunk)} chars): {repr(chunk[:250])}")

        # ---- TOKEN LOGGING ----
        total_prompt_tokens = sum(count_tokens(chunk) for chunk in chunks)
        total_completion_tokens = 0
        logger.info(f"Total prompt tokens sent: {total_prompt_tokens}")

        tasks = [self.extractor.aextract(chunk) for chunk in chunks]
        results: List[dict] = await asyncio.gather(*tasks)

        
        for i, res in enumerate(results):
            logger.info(f"LLM result[{i}]: {res}")
            if "usage" in res:
                usage = res["usage"]
                total_completion_tokens += usage.get("completion_tokens", 0)

        gpt35_prompt_per_1k = 0.002
        gpt35_completion_per_1k = 0.002
        gpt4_prompt_per_1k = 0.03
        gpt4_completion_per_1k = 0.06
        gpt4o_prompt_per_1k = 0.005
        gpt4o_completion_per_1k = 0.015  

        logger.info(f"Estimated cost (gpt-3.5-turbo): ${estimate_total_cost(total_prompt_tokens, total_completion_tokens, gpt35_prompt_per_1k, gpt35_completion_per_1k):.4f}")
        logger.info(f"Estimated cost (gpt-4): ${estimate_total_cost(total_prompt_tokens, total_completion_tokens, gpt4_prompt_per_1k, gpt4_completion_per_1k):.4f}")
        logger.info(f"Estimated cost (gpt-4o): ${estimate_total_cost(total_prompt_tokens, total_completion_tokens, gpt4o_prompt_per_1k, gpt4o_completion_per_1k):.4f}")

        summary = self.merger.merge(results)
        logger.info(f"Final summary: {summary}")

        usage = {
            "total_prompt_tokens": total_prompt_tokens,
            "total_completion_tokens": total_completion_tokens,
            "gpt3.5_estimated_cost": estimate_total_cost(
                total_prompt_tokens, total_completion_tokens, gpt35_prompt_per_1k, gpt35_completion_per_1k
            ),
            "gpt4_estimated_cost": estimate_total_cost(
                total_prompt_tokens, total_completion_tokens, gpt4_prompt_per_1k, gpt4_completion_per_1k
            ),
            "gpt4o_estimated_cost": estimate_total_cost(
                total_prompt_tokens, total_completion_tokens, gpt4o_prompt_per_1k, gpt4o_completion_per_1k
            ),
        }

        return {
            **summary,
            "usage": usage
        }

