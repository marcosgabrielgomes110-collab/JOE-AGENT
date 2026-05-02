#!/usr/bin/env python3
"""
Joi — Assistente Pessoal Autônoma
"""

import sys
import os
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.pycache_prefix = os.path.join(ROOT, "data", "cache")

# Limpa __pycache__ residuais de execuções anteriores
for dirpath, dirnames, _ in os.walk(ROOT):
    if "__pycache__" in dirnames:
        shutil.rmtree(os.path.join(dirpath, "__pycache__"), ignore_errors=True)
        dirnames.remove("__pycache__")

import capataz as cp
from capataz import SessionManager
from tools.builtins import register_all
from utils.llm import configure, call as _llm_call
from utils.logger import event as _log
from utils.interface import (
    console, banner, prompt_user, typewrite,
    error_msg, goodbye, divider, status,
    spinner_ctx, stop_spinner,
)


def _load_dotenv(path=".env"):
    with open(os.path.join(os.path.dirname(__file__), path)) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            os.environ.setdefault(key.strip(), val.strip())


def _load_persona(path="config/persona.md"):
    full = os.path.join(os.path.dirname(__file__), path)
    with open(full, "r", encoding="utf-8") as f:
        return f.read().strip()


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    _load_dotenv()

    api_key = os.getenv("GROQ_API_KEY", "")
    model = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
    debug = os.getenv("DEBUG", "").lower() in ("1", "true", "sim")

    configure(api_key=api_key, model=model)
    cp.set_llm(_llm_call)

    register_all(cp)

    for name, entry in cp.tools._registry.items():
        original_fn = entry["fn"]
        def _logged(args, _name=name, _fn=original_fn):
            result = _fn(args)
            _log("TOOL", f"{_name}({args}) → {str(result)[:200]}")
            return result
        entry["fn"] = _logged

    persona = _load_persona()

    if "joi" not in cp.agent.list_all():
        cp.agent.create("joi", system=persona, max_turns=5)

    skills_dir = os.path.join(os.path.dirname(__file__), "skills")
    if os.path.isdir(skills_dir):
        cp.skills.load(skills_dir)

    sessions = SessionManager(
        persist_dir=os.path.join(os.path.dirname(__file__), "data", "sessions"),
        context_size=10,
    )

    session = sessions.get("cli")

    console.print(banner())

    while True:
        try:
            user_input = prompt_user()
        except (EOFError, KeyboardInterrupt):
            console.print(goodbye())
            session.save()
            break

        if not user_input:
            continue
        if user_input.lower() == "sair":
            session.save()
            console.print(goodbye())
            break
        if user_input.lower() == "limpar":
            session.clear()
            console.print(status("memória limpa."))
            continue

        try:
            _log("USER", user_input)

            matched = cp.skills.match(user_input)
            if matched:
                _log("SKILL", ", ".join(f"{s.name}({s.prioridade})" for s in matched))

            spinner = spinner_ctx()
            spinner.start()
            resposta = cp.run("joi", user_input, memory=session, debug=debug)
            stop_spinner(spinner)

            _log("JOI", resposta[:300])
            typewrite(resposta)
            console.print(divider())
            session.save()
        except Exception as e:
            console.print(error_msg(str(e)[:200]))


if __name__ == "__main__":
    main()
