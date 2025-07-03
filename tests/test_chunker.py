from src.pdf_investor_summarizer.chunker import Chunker


def test_overlap():
    sample = "A" * 1050
    ch = Chunker(chunk_size=500, overlap=100)
    chunks = ch.split(sample)
    assert len(chunks) == 3
    # verify 100-symbol overlap
    assert chunks[0][-100:] == chunks[1][:100]
