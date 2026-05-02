# Skills — Como criar e cadastrar novas skills

Skills são instruções injetadas no system prompt da Joi automaticamente quando o input do usuário ativa um gatilho.

---

## O que é uma Skill

Uma skill é um arquivo `.md` com:
- **Palavras de ativação** (gatilhos) — quando o usuário digita algo que contém uma delas, a skill é injetada no prompt
- **Instruções** — o que a Joi deve fazer quando a skill estiver ativa

---

## Onde colocar

```
joi/skills/
├── terminal.md      # existente
└── sua_skill.md     # crie aqui
```

---

## Formato do arquivo

```markdown
skill name: nome_da_skill
gatilhos: palavra1, palavra2, palavra3
prioridade: alta

# Instruções

O que a Joi deve fazer quando esta skill for ativada.

Use markdown normal para as instruções.
```

---

## Campos

| Campo | Obrigatório | Descrição |
|---|---|---|
| `skill name` | Sim | Identificador único |
| `gatilhos` | Sim | Palavras separadas por vírgula |
| `prioridade` | Não | `alta`, `media` (padrão) ou `baixa` |

Skills são ordenadas por prioridade no system prompt.

---

## Exemplos

### Skill para buscar na web

```markdown
skill name: busca_web
gatilhos: pesquisar, buscar, encontrar, google, internet
prioridade: alta

# Busca na Web

Quando o usuario pedir para buscar algo:
1. Use a ferramenta terminal com curl ou wget
2. Resuma os resultados de forma clara
```

### Skill para editar código

```markdown
skill name: modo_dev
gatilhos: codigo, funcao, bug, implementar, programar, debug, testar, refatorar
prioridade: alta

# Modo Desenvolvedor

Quando o usuario pedir ajuda com codigo:
1. Mostre exemplos de codigo sempre que relevante
2. Explique o raciocinio antes da solucao
3. Considere boas praticas, performance e seguranca
```

### Skill para análises

```markdown
skill name: analise
gatilhos: analisar, analise, dados, csv, json, relatorio, grafico, estatistica
prioridade: media

# Analise de Dados

Quando o usuario pedir para analisar dados:
1. Identifique o formato (CSV, JSON, texto)
2. Busque padroes e anomalias
3. Apresente insights de forma objetiva
```

---

## Como funciona o matching

### keyword (padrão)

O capataz varre as palavras do input do usuário e verifica se alguma delas contém (substring) qualquer gatilho da skill.

```
Input: "me ajuda a pesquisar sobre Python"
             ↓
Skill "busca_web" ativada (gatilho: "pesquisar")
```

### llm (mais preciso)

Se você quiser matching semântico, use `match_mode="llm"` no `load()`:

```python
cp.skills.load("./skills/", match_mode="llm")
```

Requer `cp.skills.set_llm(fn)` configurada.

---

## Como carregar

O `main.py` já carrega automaticamente todas as skills da pasta `skills/`:

```python
skills_dir = os.path.join(os.path.dirname(__file__), "skills")
if os.path.isdir(skills_dir):
    cp.skills.load(skills_dir)
```

Basta criar um `.md` novo na pasta que ele será carregado na próxima execução.

---

## Depurando

Para ver quais skills estão sendo ativadas, use `debug=true`:

```python
resposta = cp.run("joi", user_input, memory=session, debug=True)
```

Ou verifique manualmente:

```python
skills_ativadas = cp.skills.match("pesquisar python")
print([s.name for s in skills_ativadas])
# → ["busca_web"]
```
