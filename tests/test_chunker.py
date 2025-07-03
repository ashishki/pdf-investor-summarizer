from src.pdf_investor_summarizer.chunker import Chunker


def test_overlap():
    sample = "A" * 1050
    ch = Chunker(chunk_size=500, overlap=100)
    chunks = ch.split(sample)
    assert len(chunks) == 3
    # verify 100-symbol overlap
    assert chunks[0][-100:] == chunks[1][:100]

def test_no_overlap():
    sample = "ABCDEFGHIJ" * 80  # 800 chars, unique sequence
    ch = Chunker(chunk_size=400, overlap=0)
    chunks = ch.split(sample)
    assert len(chunks) == 2
    assert chunks[0] == sample[:400]
    assert chunks[1] == sample[400:800]


def test_huge_overlap_no_infinite_loop():
    sample = "B" * 600
    ch = Chunker(chunk_size=400, overlap=399)
    chunks = ch.split(sample)
    # The number of chunks should not exceed len(text)
    assert len(chunks) < 1000
    # No infinite loop, but lots of overlapping chunks
    assert all(len(chunk) <= 400 for chunk in chunks)
