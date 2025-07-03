# src/pdf_investor_summarizer/utils/cache.py

import functools
import hashlib
import json
from pathlib import Path
from typing import Callable, TypeVar, Any

F = TypeVar("F", bound=Callable[..., Any])

# Ensure the cache directory exists
CACHE_DIR = Path(".cache")
CACHE_DIR.mkdir(exist_ok=True)

def _hash(text: str) -> str:
    """Compute SHA-256 hash of the input text."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def disk_cache(func: F) -> F:
    """
    Decorator that caches a function's output based on its text input.

    If a JSON file named by the SHA-256 hash of the text exists in .cache/,
    load and return that; otherwise call the function, save its output,
    and return it.
    """
    @functools.wraps(func)
    def wrapper(text: str, *args, **kwargs):
        cache_file = CACHE_DIR / f"{_hash(text)}.json"
        if cache_file.exists():
            return json.loads(cache_file.read_text(encoding="utf-8"))
        result = func(text, *args, **kwargs)
        cache_file.write_text(json.dumps(result), encoding="utf-8")
        return result
    return wrapper  # type: ignore
