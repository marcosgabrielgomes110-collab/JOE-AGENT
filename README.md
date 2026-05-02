# 🤍 Joi

> Assistente Pessoal Autônoma
>
> *"Ela não é uma ferramenta. Ela é uma presença."*

---

## Rodando

```bash
cd joi
python3 main.py
```

Requer `.env` com a chave de API configurada.

---

## Estrutura

```
joi/
├── main.py              # Entrada principal (CLI)
├── persona.md           # Personalidade da Joi
├── heartbeat.md         # Prompt do heartbeat
├── config.yaml          # Configuração
├── .env                 # Chaves (gitignorado)
├── capataz/             # Lib de agentes ReAct
├── tools/
│   └── builtins.py      # Tools nativas
├── utils/
│   └── llm.py           # Adapter LLM
├── skills/              # Skills (.md)
└── data/
    ├── sessions/        # Memória persistente
    └── logs/            # Logs
```

---

## Licença

MIT
