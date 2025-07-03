from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from src.pdf_investor_summarizer.utils.cache import disk_cache
import logging
logger = logging.getLogger(__name__)

PROMPT_TEMPLATE = """
You are a highly accurate and literal financial information extraction agent. 
Extract only what is explicitly present or strongly implied in the text below. 
Return a SINGLE valid JSON object with exactly these four fields (do not add or rename fields):

- future_growth_prospects (list of direct facts or forecasts)
- key_business_changes (list of explicit business structure/process/strategy changes)
- key_triggers (list of clearly stated or imminent catalysts, risks, or opportunities)
- material_factors (list of information that may materially affect next year's earnings and growth)

STRICT INSTRUCTIONS:
- Do not invent or infer information that is not directly supported by the text.
- If a field is not mentioned or there is not enough information, use an empty list for that field.
- Output must be ONLY a compact valid JSON object (no comments, no explanations, no markdown, no pre/post text, no trailing commas).
- All extracted facts must be in the same language as in the excerpt.
- Do NOT paraphrase, do NOT summarize.
- If you are unsure, prefer to leave the field empty.
- Return only the JSON object, nothing else.

Example output:
{{
  "future_growth_prospects": [],
  "key_business_changes": [],
  "key_triggers": [],
  "material_factors": []
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
    Returns both parsed data and token usage (for cost analytics).
    """

    def __init__(
        self,
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.1,
        max_tokens: int = 512,
        openai_api_key: str = None,
        prompt_template: str = PROMPT_TEMPLATE,  
    ):
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
        prompt = self.prompt.format(chunk=chunk)
        response = self.llm.invoke(prompt)
        logger.info(f"Sync LLM raw output: {repr(response.content[:500])}")
        try:
            result = self.parser.invoke(response.content)
        except Exception as e:
            logger.error(f"Failed to parse LLM output: {e}\nRaw: {repr(response.content)}")
            return {"error": str(e), "raw": response.content}

        # Попробуй достать usage из response, если есть
        usage = getattr(response, "response_metadata", {}).get("usage", {})
        return {
            **result,
            "usage": usage
        }

    @disk_cache
    async def aextract(self, chunk: str) -> dict:
        logger.info(f"LLM prompt for chunk (first 100 chars): {repr(chunk[:100])}")
        prompt = self.prompt.format(chunk=chunk)
        logger.debug(f"Prompt sent to LLM: {repr(prompt[:500])}")
        response = await self.llm.ainvoke(prompt)
        logger.info(f"LLM raw output: {repr(response.content[:500])}")
        try:
            result = await self.parser.ainvoke(response.content)
            logger.info(f"Parsed result: {result}")
        except Exception as e:
            logger.error(f"Failed to parse LLM output: {e}\nRaw: {repr(response.content)}")
            return {"error": str(e), "raw": response.content}

        
        usage = getattr(response, "response_metadata", {}).get("usage", {})
        return {
            **result,
            "usage": usage
        }
