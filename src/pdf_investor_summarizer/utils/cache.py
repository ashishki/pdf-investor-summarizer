import asyncio
import functools
import hashlib
import json
from pathlib import Path
from typing import Callable, TypeVar, Any, Awaitable

F = TypeVar("F", bound=Callable[..., Any])

CACHE_DIR = Path(".cache")
CACHE_DIR.mkdir(exist_ok=True)

def _hash(text: str) -> str:
    """Compute SHA-256 hash of the input text."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def disk_cache(func: F) -> F:
    """
    Decorator that caches sync or async method/function output based on its first string argument.
    """
    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        # Support both methods (self, chunk, ...) and functions (chunk, ...)
        if len(args) == 0:
            raise ValueError("No arguments provided to the cached function.")
        if hasattr(args[0], "__class__") and len(args) > 1:
            text_arg = args[1]
        else:
            text_arg = args[0]
        cache_file = CACHE_DIR / f"{_hash(text_arg)}.json"
        if cache_file.exists():
            return json.loads(cache_file.read_text(encoding="utf-8"))
        result = func(*args, **kwargs)
        cache_file.write_text(json.dumps(result), encoding="utf-8")
        return result

    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        # Support async methods/functions
        if len(args) == 0:
            raise ValueError("No arguments provided to the cached function.")
        if hasattr(args[0], "__class__") and len(args) > 1:
            text_arg = args[1]
        else:
            text_arg = args[0]
        cache_file = CACHE_DIR / f"{_hash(text_arg)}.json"
        if cache_file.exists():
            return json.loads(cache_file.read_text(encoding="utf-8"))
        result = await func(*args, **kwargs)
        cache_file.write_text(json.dumps(result), encoding="utf-8")
        return result

    if asyncio.iscoroutinefunction(func):
        return async_wrapper  # type: ignore
    else:
        return sync_wrapper  # type: ignore
