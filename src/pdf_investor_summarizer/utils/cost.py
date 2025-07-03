import tiktoken

def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    enc = tiktoken.encoding_for_model(model)
    return len(enc.encode(text))

def estimate_cost(total_tokens: int, price_per_1k: float) -> float:
    return (total_tokens / 1000) * price_per_1k