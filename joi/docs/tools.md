# Tools — Como criar e cadastrar novas ferramentas

Tools são funções Python que a Joi pode chamar automaticamente quando precisa.

---

## Estrutura

Toda tool vive em `joi/tools/`. O arquivo principal é `builtins.py`, mas você pode criar quantos arquivos quiser.

```
joi/tools/
├── __init__.py
├── builtins.py        # tools nativas da Joi
└── meus_comandos.py   # suas tools customizadas
```

---

## Criando uma tool

### 1. Crie um arquivo ou edite `builtins.py`

```python
# tools/meus_comandos.py

def register_all(cp):
    """Registra todas as tools deste arquivo no capataz."""

    @cp.tool("previsao",
             desc="Previsao do tempo para uma cidade. "
                  "Parâmetro: cidade (str) — nome da cidade.")
    def previsao(args: dict) -> str:
        cidade = args.get("cidade", "desconhecida")
        # Aqui voce chamaria uma API real
        return f"{cidade}: 28°C, ensolarado"
```

### 2. Importe e registre no `main.py`

Abra `main.py` e adicione:

```python
from tools.meus_comandos import register_all as register_meus

# Dentro de main(), depois de register_all(cp):
register_meus(cp)
```

---

## Regras para uma boa tool

| Regra | Explicação |
|---|---|
| **Nome curto** | `previsao`, `buscar`, `baixar` — a Joi vai chamar pelo nome |
| **Descrição clara** | Inclua parâmetros e exemplos na `desc` |
| **Único parâmetro dict** | A LLM envia `Action Input: {"chave": "valor"}` |
| **Sempre retorna string** | O que for retornado vira Observation da Joi |
| **Trate erros** | Retorne string com erro, não levante exceção |

---

## Exemplo completo

```python
@cp.tool("buscar_arquivo",
         desc="Busca um arquivo no sistema. "
              "Parâmetro: nome (str) — nome do arquivo.")
def buscar_arquivo(args: dict) -> str:
    import os, glob
    nome = args.get("nome", "")
    if not nome:
        return "Erro: informe um nome de arquivo."
    resultados = glob.glob(f"**/{nome}", recursive=True)
    if not resultados:
        return "Nenhum arquivo encontrado."
    return "\n".join(resultados[:10])
```

---

## Tools com permissão sudo

A tool `terminal` já tem suporte a sudo automático via `SUDO_PASSWORD` no `.env`.

```env
SUDO_PASSWORD=minha_senha
```

Quando a Joi executar `sudo apt install pacote`, a senha é injetada automaticamente.

---

## Tools que usam API externa

```python
@cp.tool("cotacao",
         desc="Cotacao atual do dolar. Parâmetros: nenhum.")
def cotacao(args: dict) -> str:
    import requests
    try:
        resp = requests.get("https://api.exemplo.com/dolar", timeout=10)
        return f"Dolar: R$ {resp.json()['valor']}"
    except Exception as e:
        return f"Erro ao obter cotacao: {e}"
```
