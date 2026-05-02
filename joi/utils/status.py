"""
joi.utils.status — Informacoes do sistema Joi
"""

import os
import capataz as cp

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _p(path):
    full = os.path.join(ROOT, path)
    return os.path.abspath(full)


def report():
    lines = []
    lines.append("  + Joi - Status +")
    lines.append("")

    # Caminhos
    lines.append("  Caminhos:")
    lines.append(f"    Raiz:       {ROOT}")
    lines.append(f"    Config:     {_p('config.yaml')}")
    lines.append(f"    Persona:    {_p('config/persona.md')}")
    lines.append(f"    Heartbeat:  {_p('config/heartbeat.md')}")
    lines.append(f"    .env:       {_p('.env')}")
    lines.append(f"    Dados:      {_p('data/')}")
    lines.append(f"    Cache:      {_p('data/cache/')}")
    lines.append(f"    Log:        {_p('data/logs/joi.log')}")
    lines.append("")

    # Skills
    skills_dir = _p("skills/")
    lines.append(f"  Skills ({skills_dir}):")
    loaded = cp.skills.list_all()
    if loaded:
        for s in loaded:
            skill = cp.skills._skills.get(s)
            gatilhos = ", ".join(skill.gatilhos[:5]) if skill else ""
            extra = "..." if skill and len(skill.gatilhos) > 5 else ""
            lines.append(f"    - {s} [{skill.prioridade}] ({gatilhos}{extra})")
    else:
        lines.append("    (nenhuma skill carregada)")
    lines.append("")

    # Tools
    lines.append("  Tools disponiveis:")
    for name in sorted(cp.tools.list_tools()):
        info = cp.tools._registry.get(name, {})
        desc = info.get("desc", "sem descricao")[:70]
        lines.append(f"    - {name}: {desc}")
    lines.append("")

    # LLM
    from utils.llm import API_KEY, MODEL
    lines.append("  LLM:")
    lines.append(f"    Provedor:   Groq")
    lines.append(f"    Modelo:     {MODEL}")
    api_status = "configurada" if API_KEY else "NAO CONFIGURADA"
    lines.append(f"    API Key:    {api_status}")
    lines.append("")

    # Agente
    lines.append("  Agente:")
    if "joi" in cp.agent.list_all():
        ag = cp.agent.get("joi")
        lines.append(f"    Nome:       joi")
        lines.append(f"    Max turns:  {ag.get('max_turns', 5)}")
        lines.append(f"    Persona:    {len(ag.get('system', ''))} chars")
    else:
        lines.append("    (agente nao criado)")
    lines.append("")

    return "\n".join(lines)
