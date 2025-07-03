import functools
import hashlib
import json
from pathlib import Path
from typing import Callable, TypeVar, Any

F = TypeVar("F", bound=Callable[..., Any])

CACHE_DIR = Path(".cache")
CACHE_DIR.mkdir(exist_ok=True)

def _hash(text: str) -> str:
    """Compute SHA-256 hash of the input text."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def disk_cache(func: F) -> F:
    """
    Decorator that caches a function's output based on its first string argument.
    Works for both standalone functions and instance methods.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # If called as a method, args[0] is self, args[1] is the text argument
        # If called as a function, args[0] is the text argument
        if len(args) == 0:
            raise ValueError("No arguments provided to the cached function.")
        if hasattr(args[0], "__class__") and len(args) > 1:
            # method: first arg is self, second is text
            text_arg = args[1]
        else:
            # function: first arg is text
            text_arg = args[0]
        cache_file = CACHE_DIR / f"{_hash(text_arg)}.json"
        if cache_file.exists():
            return json.loads(cache_file.read_text(encoding="utf-8"))
        result = func(*args, **kwargs)
        cache_file.write_text(json.dumps(result), encoding="utf-8")
        return result
    return wrapper  # type: ignore
