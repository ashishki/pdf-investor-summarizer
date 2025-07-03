from src.pdf_investor_summarizer.merger import Merger

def test_merger_deduplicates_and_filters_short():
    merger = Merger()
    results = [
        {
            "future_growth_prospects": ["  Growth 20%  ", "Growth 20%", "Ok", "  "],
            "key_business_changes": ["Acquisition of X", "Acquisition of X"],
            "key_triggers": ["Recovery"],
            "material_factors": ["", "  "]
        },
        {
            "future_growth_prospects": ["Growth 20%", "Expansion", "Ok"],
            "key_business_changes": ["New CEO"],
            "key_triggers": ["Recovery", "Demand"],
            "material_factors": ["Revenue up"]
        }
    ]
    merged = merger.merge(results)
    
    assert "Ok" not in merged["future_growth_prospects"]  
    assert merged["future_growth_prospects"].count("Growth 20%") == 1  
    assert "Acquisition of X" in merged["key_business_changes"]
    assert len(merged["material_factors"]) == 1  
