#  PDF Investor Summarizer

**PDF Investor Summarizer** is a Python tool for automatically extracting key investor insights from company PDF reports using GPT (LLM).  
Ready to run in Google Colab: the sample PDF is auto-loaded, and user uploads are supported.

---

##  Quick Start in Google Colab

1. **Clone the repository and install dependencies:**
    ```python
    !git clone https://github.com/ashishki/pdf-investor-summarizer.git
    %cd pdf-investor-summarizer
    !pip install .
    %cd /
    ```

2. **Import modules and load the sample PDF:**
    ```python
    import importlib.util
    from pathlib import Path
    import shutil

    spec = importlib.util.find_spec("pdf_investor_summarizer")
    package_dir = Path(spec.origin).parent
    sample_pdf = package_dir / "assets" / "company_report.pdf"
    dst = Path("company_report.pdf")

    if not dst.exists():
        shutil.copy(sample_pdf, dst)
        print(f"Sample PDF copied to: {dst}")
    else:
        print("Sample PDF already exists.")
    PDF_SOURCE = dst
    ```

3. **(Optional) Upload your own PDF (Colab UI):**
    ```python
    try:
        from google.colab import files
        uploaded = files.upload()
        if uploaded:
            PDF_SOURCE = Path(list(uploaded.keys())[0])
            print(f"Using uploaded PDF: {PDF_SOURCE}")
        else:
            print(f"No upload detected, using sample PDF: {PDF_SOURCE}")
    except ImportError:
        print("Not running in Colab, skipping upload.")
    ```

4. **Run the analyzer and get a structured summary:**
    ```python
    import asyncio
    from pdf_investor_summarizer.report_analyzer import ReportAnalyzer
    import json

    analyzer = ReportAnalyzer(chunk_size=2000, overlap=200)
    result = await analyzer.analyze_async(PDF_SOURCE)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    ```

---

##  Features

- LLM-powered extraction of investment-relevant data from PDF reports
- Automatic structuring of key business factors:
    - Future Growth Prospects
    - Key Business Changes
    - Key Triggers
    - Material Factors
- Ready-to-use demo with bundled sample PDF
- User PDF upload supported

---

##  Notes

- Requires Python 3.11+ (Colab is supported)
- Requires OpenAI API key (`OPENAI_API_KEY`)
- For OCR support (scanned PDFs):  
  `!apt-get install tesseract-ocr`

---

**Feedback, issues, or suggestions? Open an issue or contact the author!**

---
