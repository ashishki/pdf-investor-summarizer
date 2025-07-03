# tests/test_cache.py

import shutil
import pytest

from src.pdf_investor_summarizer.utils.cache import disk_cache, _hash, CACHE_DIR

@pytest.fixture(autouse=True)
def clear_and_override_cache_dir(tmp_path, monkeypatch):
    """
    Redirect the module's CACHE_DIR to a temp path and ensure it's empty.
    """
    # Point the cache into our tmp_path
    monkeypatch.setattr(
        "src.pdf_investor_summarizer.utils.cache.CACHE_DIR",
        tmp_path
    )
    tmp_path.mkdir(exist_ok=True)
    yield
    shutil.rmtree(tmp_path, ignore_errors=True)

@disk_cache
def fake_heavy_compute(text: str) -> dict:
    """Simulate an expensive computation by returning the reversed text."""
    return {"echo": text[::-1]}

def test_disk_cache_creates_file(tmp_path):
    """First call should compute and create a cache file."""
    key_path = tmp_path / f"{_hash('hello')}.json"
    assert not key_path.exists()

    result = fake_heavy_compute("hello")
    assert result == {"echo": "olleh"}
    assert key_path.exists()

def test_disk_cache_loads_from_file(tmp_path):
    """Second call with same text should load result from cache, not recompute."""
    # Prime the cache
    _ = fake_heavy_compute("world")
    key_path = tmp_path / f"{_hash('world')}.json"
    assert key_path.exists()

    # Replace the original function to ensure it would error if called
    original = fake_heavy_compute.__wrapped__
    fake_heavy_compute.__wrapped__ = lambda text: (_ for _ in ()).throw(RuntimeError("Should not be called"))

    # This call must come from cache and not raise
    result = fake_heavy_compute("world")
    assert result == {"echo": "dlrow"}

    # Restore the original
    fake_heavy_compute.__wrapped__ = original
