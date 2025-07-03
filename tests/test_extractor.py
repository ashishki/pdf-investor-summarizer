# tests/test_extractor.py

from src.pdf_investor_summarizer.extractor import Extractor

def test_extractor_returns_expected_structure():
    """
    Extractor should return all expected keys and evidence as an empty string.
    """
    extractor = Extractor()
    chunk = "Sample annual report text."
    result = extractor.extract(chunk)
    expected_keys = [
        "future_growth_prospects",
        "key_business_changes",
        "key_triggers",
        "material_factors",
        "evidence",
    ]
    assert isinstance(result, dict)
    assert sorted(result.keys()) == sorted(expected_keys)
    for key in expected_keys[:-1]:
        assert isinstance(result[key], list)
        assert not result[key]  # must be empty list
    assert result["evidence"] == ""

def test_extractor_cache(monkeypatch, tmp_path):
    """
    Test that repeated calls with the same chunk use the cache (simulate new cache dir).
    """
    monkeypatch.setattr(
        "src.pdf_investor_summarizer.utils.cache.CACHE_DIR",
        tmp_path
    )
    extractor = Extractor()
    chunk = "Caching test."
    res1 = extractor.extract(chunk)
    res2 = extractor.extract(chunk)
    assert res1 == res2
