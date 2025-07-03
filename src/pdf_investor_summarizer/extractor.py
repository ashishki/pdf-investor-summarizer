# src/pdf_investor_summarizer/extractor.py

from src.pdf_investor_summarizer.utils.cache import disk_cache

class Extractor:
    """
    Extracts investment-relevant information from a text chunk.
    Designed to work with LLMs (e.g., OpenAI GPT) and supports caching,
    evidence tracking, and cost monitoring (future extension).
    """

    def __init__(
        self,
        prompt: str = None,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.1,
        max_tokens: int = 512,
    ):
        """
        Parameters
        ----------
        prompt : str, optional
            System/user prompt for the LLM.
        model : str
            LLM model name.
        temperature : float
            Sampling temperature for the LLM.
        max_tokens : int
            Maximum number of tokens to generate.
        """
        self.prompt = prompt or "Extract key investment information as JSON."
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    @disk_cache
    def extract(self, chunk: str) -> dict:
        """
        Extract investment-relevant info from a given chunk.
        Currently returns a dummy structure; replace with LLM call for production.

        Returns
        -------
        dict
            Structured output with four info fields and evidence.
        """
        return {
            "future_growth_prospects": [],
            "key_business_changes": [],
            "key_triggers": [],
            "material_factors": [],
            "evidence": "",  # for traceability/explainability
        }
