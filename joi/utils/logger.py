"""
joi.utils.logger — Registro de eventos da Joi
"""

import os
from datetime import datetime


def _log_path() -> str:
    return os.path.join(os.path.dirname(__file__), "..", "data", "logs", "joi.log")


def event(log_type: str, detail: str):
    """Registra um evento no log da Joi."""
    path = _log_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(path, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {log_type}: {detail}\n")
