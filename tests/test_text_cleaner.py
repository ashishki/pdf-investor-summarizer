# tests/test_text_cleaner.py

from src.pdf_investor_summarizer.text_cleaner import TextCleaner

RAW_PAGE = """
My Report Title
1

This is a valid line of content.
Short
123
Another     line    with   spaces
"""

def test_clean_removes_short_and_numeric_lines():
    """
    Ensure that lines shorter than min_line_length and page numbers are removed,
    whitespace is normalized, and valid lines are kept.
    """
    cleaner = TextCleaner(min_line_length=6)
    cleaned = cleaner.clean(RAW_PAGE)

    # 'My Report Title' length >=6, so it stays
    assert "My Report Title" in cleaned
    # 'This is a valid line of content.' remains
    assert "This is a valid line of content." in cleaned
    # 'Another     line    with   spaces' normalized to single spaces
    assert "Another line with spaces" in cleaned
    # 'Short' is shorter than 6 chars and should be removed
    assert "Short" not in cleaned
    # lines that are numeric-only are removed
    assert "123" not in cleaned
    # single number page number ("1") is also removed
    assert not any(part.strip() == "1" for part in cleaned.split())

def test_clean_pages_applies_to_each_page():
    """
    clean_pages should apply clean() to each page in a list.
    """
    pages = ["Line1\nLine2", "123\nValid content"]
    cleaner = TextCleaner(min_line_length=2)
    result = cleaner.clean_pages(pages)
    assert isinstance(result, list)
    assert result[0] == "Line1 Line2"
    assert result[1] == "Valid content"
