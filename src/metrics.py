from typing import Dict, Any

_METRICS: Dict[str, Any] = {"requests_total": 0, "errors_total": 0}

def track_request(status: str = "success"):
    _METRICS["requests_total"] += 1
    if status == "error":
        _METRICS["errors_total"] += 1

def get_metrics() -> Dict[str, Any]:
    return _METRICS
