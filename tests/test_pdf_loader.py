import pytest
from pathlib import Path

from src.pdf_investor_summarizer.pdf_loader import PdfLoader


class FakePage:
    pass


class FakeReader:
    def __init__(self, path):
        # Simulate a PDF with 2 pages
        self.pages = [FakePage(), FakePage()]


@pytest.fixture(autouse=True)
def patch_pdf_reader(monkeypatch):
    """
    Stub out PdfReader so every PDF has 2 pages.
    """
    monkeypatch.setattr(
        'src.pdf_investor_summarizer.pdf_loader.PdfReader',
        FakeReader
    )
    return monkeypatch


def test_loader_from_path(monkeypatch, tmp_path):
    # Create a dummy PDF file (contents ignored by stubbed PdfReader)
    pdf_file = tmp_path / 'test.pdf'
    pdf_file.write_bytes(b'%PDF-1.4 dummy')

    # Stub native text extraction to return page-specific text
    monkeypatch.setattr(
        'src.pdf_investor_summarizer.pdf_loader.extract_text',
        lambda path, page_numbers=None: f"text{page_numbers[0]}"
    )

    loader = PdfLoader(pdf_file)
    pages = loader.load()

    assert pages == ['text0', 'text1']


def test_loader_from_url(monkeypatch):
    # Prepare fake HTTP response with PDF bytes
    fake_pdf = b'%PDF-1.4 dummy'
    class FakeResponse:
        def __init__(self):
            self.content = fake_pdf
        def raise_for_status(self):
            pass

    # Stub requests.get to return our fake response
    monkeypatch.setattr(
        'src.pdf_investor_summarizer.pdf_loader.requests.get',
        lambda url: FakeResponse()
    )

    # Stub extract_text to return empty, forcing OCR fallback
    monkeypatch.setattr(
        'src.pdf_investor_summarizer.pdf_loader.extract_text',
        lambda path, page_numbers=None: ""
    )
    # Stub OCR method to return predictable text
    monkeypatch.setattr(
        'src.pdf_investor_summarizer.pdf_loader.PdfLoader._ocr_page',
        lambda self, pg: f"ocr{pg}"
    )

    loader = PdfLoader('http://example.com/report.pdf')
    pages = loader.load()

    assert pages == ['ocr1', 'ocr2']


def test_loader_from_bytes(monkeypatch):
    # Raw PDF bytes input
    data = b'%PDF-1.4 dummy'

    # Stub extract_text to always return non-empty
    monkeypatch.setattr(
        'src.pdf_investor_summarizer.pdf_loader.extract_text',
        lambda path, page_numbers=None: 'hello'
    )

    loader = PdfLoader(data)
    pages = loader.load()

    assert pages == ['hello', 'hello']
