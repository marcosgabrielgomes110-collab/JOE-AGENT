"""
joi.tools.obsidian — Ferramentas de integracao com Obsidian vault
"""

import os
import glob
from datetime import date


def _vault_path() -> str:
    """Retorna o caminho absoluto do vault a partir de VAULT_PATH no .env."""
    raw = os.getenv("VAULT_PATH", "")
    if not raw:
        return ""
    return os.path.abspath(os.path.expanduser(raw))


def _resolve(rel_path: str) -> str:
    """Converte caminho relativo ao vault para absoluto, com proteção contra path traversal."""
    vault = _vault_path()
    if not vault or not os.path.isdir(vault):
        return ""
    full = os.path.normpath(os.path.join(vault, rel_path))
    # Protecao contra path traversal (ex: ../../../etc/passwd)
    if not full.startswith(os.path.normpath(vault)):
        return ""
    return full


def register_all(cp):
    """Registra as tools do Obsidian no capataz."""

    @cp.tool("obsidian_ler",
             desc="Le o conteudo de uma nota do Obsidian. "
                  "Parâmetro: nota (str) — caminho relativo ao vault (ex: 'Ideias/ideia.md').")
    def obsidian_ler(args: dict) -> str:
        nota = (args.get("nota") or "").strip()
        if not nota:
            return "Erro: informe o parametro 'nota' (ex: 'Ideias/minha-ideia.md')."
        path = _resolve(nota)
        if not path and _vault_path():
            return f"Caminho invalido: {nota}"
        if not path:
            vault_raw = os.getenv("VAULT_PATH", "")
            if not vault_raw:
                return "Erro: VAULT_PATH nao configurado no .env."
            return f"Erro: vault nao encontrado em: {os.path.abspath(os.path.expanduser(vault_raw))}"
        if not os.path.exists(path):
            return f"Nota nao encontrada: {nota}"
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                conteudo = f.read()
            if not conteudo:
                return f"Nota vazia: {nota}"
            if len(conteudo) > 3000:
                return f"{conteudo[:3000]}\n\n...(nota truncada, {len(conteudo)} chars)"
            return conteudo
        except PermissionError:
            return f"Erro: sem permissao para ler: {nota}"
        except Exception as e:
            return f"Erro ao ler nota: {e}"

    @cp.tool("obsidian_criar",
             desc="Cria uma nova nota no Obsidian (nao sobrescreve se existir). "
                  "Parâmetros: nota (str) — caminho relativo, conteudo (str).")
    def obsidian_criar(args: dict) -> str:
        nota = (args.get("nota") or "").strip()
        conteudo = (args.get("conteudo") or "").strip()
        if not nota:
            return "Erro: informe o parametro 'nota'."
        path = _resolve(nota)
        if not path:
            return "Erro: vault nao encontrado ou VAULT_PATH nao configurado."
        if os.path.exists(path):
            return f"Nota ja existe: {nota}. Use obsidian_editar para adicionar conteudo."
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(conteudo + "\n")
            return f"Nota criada: {nota} ({len(conteudo)} chars)"
        except PermissionError:
            return f"Erro: sem permissao para escrever em: {nota}"
        except Exception as e:
            return f"Erro ao criar nota: {e}"

    @cp.tool("obsidian_editar",
             desc="Adiciona conteudo ao final de uma nota existente no Obsidian. "
                  "Parâmetros: nota (str) — caminho relativo, conteudo (str).")
    def obsidian_editar(args: dict) -> str:
        nota = (args.get("nota") or "").strip()
        conteudo = (args.get("conteudo") or "").strip()
        if not nota:
            return "Erro: informe o parametro 'nota'."
        if not conteudo:
            return "Erro: informe o parametro 'conteudo'."
        path = _resolve(nota)
        if not path:
            return "Erro: vault nao encontrado ou VAULT_PATH nao configurado."
        if not os.path.exists(path):
            return f"Nota nao existe: {nota}. Use obsidian_criar primeiro."
        try:
            with open(path, "a", encoding="utf-8") as f:
                f.write(f"\n{conteudo}\n")
            return f"Conteudo adicionado a: {nota}"
        except PermissionError:
            return f"Erro: sem permissao para editar: {nota}"
        except Exception as e:
            return f"Erro ao editar nota: {e}"

    @cp.tool("obsidian_buscar",
             desc="Busca por uma palavra-chave em todas as notas do vault. "
                  "Parâmetro: termo (str) — palavra ou frase para buscar.")
    def obsidian_buscar(args: dict) -> str:
        termo = (args.get("termo") or "").strip()
        if not termo:
            return "Erro: informe o parametro 'termo'."
        vault = _vault_path()
        if not vault or not os.path.isdir(vault):
            return "Erro: vault nao encontrado ou VAULT_PATH nao configurado."
        resultados = []
        for root, _, files in os.walk(vault):
            for file in files:
                if not file.endswith(".md"):
                    continue
                caminho = os.path.join(root, file)
                try:
                    with open(caminho, "r", encoding="utf-8", errors="replace") as f:
                        conteudo = f.read()
                    if termo.lower() in conteudo.lower():
                        rel = os.path.relpath(caminho, vault)
                        resultados.append(rel)
                except (PermissionError, OSError):
                    continue
        if not resultados:
            return f"Nenhuma nota encontrada com: '{termo}'"
        total = len(resultados)
        limite = resultados[:20]
        linhas = "\n".join(f"  - {r}" for r in limite)
        extra = f"\n  ...e mais {total - 20}" if total > 20 else ""
        return f"Notas com '{termo}' ({total}):\n{linhas}{extra}"

    @cp.tool("obsidian_listar",
             desc="Lista as notas de uma pasta do vault. "
                  "Parâmetro: pasta (str) — caminho relativo (ex: 'Daily', 'Projects'). Vazio lista a raiz.")
    def obsidian_listar(args: dict) -> str:
        pasta = (args.get("pasta") or "").strip()
        vault = _vault_path()
        if not vault or not os.path.isdir(vault):
            return "Erro: vault nao encontrado ou VAULT_PATH nao configurado."
        target = _resolve(pasta) if pasta else vault
        if not target:
            return f"Pasta invalida: {pasta}"
        if not os.path.isdir(target):
            return f"Pasta nao encontrada: {pasta or '(raiz)'}"
        try:
            arquivos = sorted(f for f in os.listdir(target) if f.endswith(".md"))
            subpastas = sorted(
                d for d in os.listdir(target)
                if os.path.isdir(os.path.join(target, d)) and not d.startswith(".")
            )
            linhas = []
            for s in subpastas:
                linhas.append(f"  [{s}/]")
            for a in arquivos:
                linhas.append(f"  - {a}")
            if not linhas:
                return f"Pasta vazia: {pasta or '(raiz)'}"
            cab = f"Conteudo de '{pasta or '(raiz)'}':\n"
            return cab + "\n".join(linhas)
        except PermissionError:
            return f"Erro: sem permissao para listar: {pasta or '(raiz)'}"
        except Exception as e:
            return f"Erro ao listar: {e}"

    @cp.tool("obsidian_diaria",
             desc="Retorna o caminho da nota diaria de hoje no vault (Daily/YYYY-MM-DD.md). "
                  "Parâmetros: nenhum.")
    def obsidian_diaria(args: dict) -> str:
        vault = _vault_path()
        if not vault or not os.path.isdir(vault):
            return "Erro: vault nao encontrado ou VAULT_PATH nao configurado."
        today = date.today().isoformat()
        rel = f"Daily/{today}.md"
        full = os.path.join(vault, rel)
        if os.path.exists(full):
            return f"Nota diaria de hoje: {rel}"
        return f"Nota diaria ainda nao existe: {rel}. Use obsidian_criar para criar."
