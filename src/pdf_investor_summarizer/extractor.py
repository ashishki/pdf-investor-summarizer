from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pdf_investor_summarizer.utils.cache import disk_cache

PROMPT_TEMPLATE = """
You are an expert financial analyst. Your task is to extract only actionable, investor-relevant information from company reports.

For the following text, return a JSON object with EXACTLY these fields:
- future_growth_prospects: (list of facts or forecasts)
- key_business_changes: (list of significant changes)
- key_triggers: (list of potential catalysts, risks, or opportunities)
- material_factors: (list of information that may materially affect next year's earnings and growth)

Respond ONLY with valid, minified JSON (no markdown, no comments, no explanations, no trailing commas).

Example output:
{{
  "future_growth_prospects": ["Company plans to expand into Asia in 2025."],
  "key_business_changes": ["Restructured management team in Q4."],
  "key_triggers": ["Upcoming product launch in September."],
  "material_factors": ["Pending litigation over patent dispute."]
}}

Company report excerpt:
<<<BEGIN>>>
{chunk}
<<<END>>>
"""

class Extractor:
    """
    Extracts investment-relevant information from a text chunk using an LLM via LangChain.
    Supports both synchronous and asynchronous extraction.
    """

    def __init__(
        self,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.1,
        max_tokens: int = 512,
        openai_api_key: str = None,
        prompt_template: str = PROMPT_TEMPLATE,
    ):
        """
        Parameters
        ----------
        model : str
            LLM model name.
        temperature : float
            Sampling temperature.
        max_tokens : int
            Maximum tokens to generate.
        openai_api_key : str, optional
            API key (if not set in env).
        prompt_template : str
            Prompt text for the LLM.
        """
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            openai_api_key=openai_api_key,
        )
        self.prompt = PromptTemplate.from_template(prompt_template)
        self.parser = JsonOutputParser()

    @disk_cache
    def extract(self, chunk: str) -> dict:
        """
        Run LLM extraction on chunk, return strict JSON.
        """
        prompt = self.prompt.format(chunk=chunk)
        response = self.llm.invoke(prompt)
        return self.parser.invoke(response.content)

    @disk_cache
    async def aextract(self, chunk: str) -> dict:
        """
        Async version of extract. Recommended for batch processing.
        """
        prompt = self.prompt.format(chunk=chunk)
        response = await self.llm.ainvoke(prompt)
        return await self.parser.ainvoke(response.content)

