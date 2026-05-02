"""
joi.utils.llm — Adapter Groq (OpenAI-compatible)
"""

import os
import time
import requests

API_KEY = None
MODEL = "llama-3.3-70b-versatile"
MAX_RETRIES = 2


def _log_error(detail: str):
    try:
        from utils.logger import event
        event("LLM_ERRO", detail)
    except Exception:
        pass


def configure(api_key: str, model: str = "llama-3.3-70b-versatile"):
    global API_KEY, MODEL
    API_KEY = api_key
    MODEL = model


def call(messages: list[dict]) -> str:
    if not API_KEY:
        return "Final Answer: API_KEY não configurada."

    last_error = ""
    for attempt in range(MAX_RETRIES + 1):
        try:
            resp = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json",
                },
                json={"model": MODEL, "messages": messages},
                timeout=90,
            )
            resp.raise_for_status()
            data = resp.json()
            choices = data.get("choices", [])
            if choices:
                return choices[0].get("message", {}).get("content", "")
            return "Final Answer: Desculpe, não consegui processar sua mensagem."

        except requests.exceptions.Timeout:
            last_error = "timeout"
            _log_error("timeout após 90s")
            if attempt < MAX_RETRIES:
                time.sleep(2)
                continue
            return "Final Answer: A API está demorando muito. Tente de novo em alguns segundos."

        except requests.exceptions.ConnectionError:
            last_error = "connection"
            _log_error("erro de conexão")
            if attempt < MAX_RETRIES:
                time.sleep(3)
                continue
            return "Final Answer: Sem conexão com a API. Verifique sua internet."

        except requests.exceptions.HTTPError as e:
            status = e.response.status_code if e.response is not None else 0
            _log_error(f"HTTP {status}")
            if status == 401:
                return "Final Answer: Chave de API inválida. Verifique seu .env."
            if status == 429:
                if attempt < MAX_RETRIES:
                    time.sleep(5)
                    continue
                return "Final Answer: Muitas requisições. Aguarde um momento e tente de novo."
            if status >= 500:
                if attempt < MAX_RETRIES:
                    time.sleep(3)
                    continue
            return "Final Answer: O servidor da API está com problemas. Tente mais tarde."

        except Exception as e:
            last_error = str(e)[:100]
            _log_error(f"erro inesperado: {last_error}")
            return "Final Answer: Ocorreu um erro ao processar sua mensagem. Tente de novo."

    return f"Final Answer: Não consegui me comunicar com a API. ({last_error})"
