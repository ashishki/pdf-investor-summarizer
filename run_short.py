import logging
import asyncio
from src.pdf_investor_summarizer.report_analyzer import ReportAnalyzer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

analyzer = ReportAnalyzer(chunk_size=2000, overlap=200)
result = asyncio.run(analyzer.analyze_async("tests/assets/company_report.pdf"))

import json
print(json.dumps(result, indent=2, ensure_ascii=False))