# tests/test_merger.py

from src.pdf_investor_summarizer.merger import Merger

def test_merger_combines_lists():
    """
    Merger should concatenate lists from all chunks for each key.
    """
    dummy_chunks = [
        {
            "future_growth_prospects": ["Growth1"],
            "key_business_changes": [],
            "key_triggers": ["Trigger1"],
            "material_factors": [],
            "evidence": "Chunk1"
        },
        {
            "future_growth_prospects": [],
            "key_business_changes": ["ChangeA"],
            "key_triggers": [],
            "material_factors": ["FactorZ"],
            "evidence": "Chunk2"
        }
    ]
    merger = Merger()
    result = merger.merge(dummy_chunks)
    assert result["future_growth_prospects"] == ["Growth1"]
    assert result["key_business_changes"] == ["ChangeA"]
    assert result["key_triggers"] == ["Trigger1"]
    assert result["material_factors"] == ["FactorZ"]
    # Evidence should be empty string (not merged), as per design
    assert result["evidence"] == ""

def test_merger_empty_input():
    merger = Merger()
    assert merger.merge([]) == {}
