from src.pdf_investor_summarizer.report_analyzer import ReportAnalyzer

def test_pipeline_on_dummy_text(monkeypatch):
    """
    Full pipeline integration test on a synthetic dummy PDF (string as input).
    """
    # Patch PdfLoader.__init__ to accept any source without error
    monkeypatch.setattr(
        "src.pdf_investor_summarizer.pdf_loader.PdfLoader.__init__",
        lambda self, source, ocr_lang='eng', ocr_dpi=300: None
    )
    # Patch PdfLoader.load to return predictable pages
    monkeypatch.setattr(
        "src.pdf_investor_summarizer.pdf_loader.PdfLoader.load",
        lambda self: [
            "Growth is strong.\nPage 1",
            "Key trigger: New product launch.\nPage 2"
        ]
    )
    analyzer = ReportAnalyzer(chunk_size=50, overlap=10)
    summary = analyzer.analyze("dummy.pdf")
    assert isinstance(summary, dict)
    for key in [
        "future_growth_prospects", "key_business_changes",
        "key_triggers", "material_factors", "evidence"
    ]:
        assert key in summary
