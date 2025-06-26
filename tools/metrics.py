import time
from datetime import datetime
from collections import defaultdict

LOG_FILE = "metrics.log"

metrics = {
    "latency": [],
    "token_counts": [],
    "tool_usage": defaultdict(int),
    "errors": 0,
    "context_hits": 0,
    "context_misses": 0
}

def _log_to_file(message: str):
    timestamp = datetime.now().isoformat()
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def track_latency(start_time):
    latency = round(time.time() - start_time, 4)
    metrics["latency"].append(latency)
    _log_to_file(f"Latency: {latency}s")

def track_tokens(prompt_tokens, response_tokens):
    metrics["token_counts"].append((prompt_tokens, response_tokens))
    _log_to_file(f"Tokens - Prompt: {prompt_tokens}, Response: {response_tokens}")

def track_tool_usage(tool_name):
    metrics["tool_usage"][tool_name] += 1
    _log_to_file(f"Tool used: {tool_name}")

def track_error():
    metrics["errors"] += 1
    _log_to_file("Error occurred")

def track_context_hit(hit=True):
    if hit:
        metrics["context_hits"] += 1
        _log_to_file("Context HIT")
    else:
        metrics["context_misses"] += 1
        _log_to_file("Context MISS")

def get_metrics():
    return metrics
