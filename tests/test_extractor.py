import pytest

class DummyLLM:
    def invoke(self, prompt):
        class DummyResponse:
            content = '{"future_growth_prospects":["A"],"key_business_changes":[],"key_triggers":[],"material_factors":[]}'
            response_metadata = {"usage": {"prompt_tokens": 5, "completion_tokens": 2}}
        return DummyResponse()

@pytest.fixture
def dummy_extractor(monkeypatch):
    from src.pdf_investor_summarizer.extractor import Extractor
    ext = Extractor()
    ext.llm = DummyLLM()  
    return ext

def test_extractor_returns_usage(dummy_extractor):
    res = dummy_extractor.extract("Test chunk")
    assert "usage" in res
    assert isinstance(res["usage"]["prompt_tokens"], int)
    assert res["future_growth_prospects"] == ["A"]
