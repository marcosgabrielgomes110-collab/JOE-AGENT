"""
joi.tools.builtins — Ferramentas nativas da Joi
"""

import os
import json
import subprocess
from datetime import datetime


def register_all(cp):
    """Registra todas as tools nativas no capataz."""

    @cp.tool("hora", desc="Retorna a data e hora atual. Parâmetros: nenhum.")
    def hora(args: dict) -> str:
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    @cp.tool("ler_arquivo", desc="Lê o conteúdo de um arquivo. Parâmetro: caminho (str) — caminho do arquivo.")
    def ler_arquivo(args: dict) -> str:
        path = args.get("caminho", "")
        if not path:
            return "Erro: caminho não informado."
        try:
            with open(os.path.expanduser(path), "r", encoding="utf-8") as f:
                conteudo = f.read()
            if len(conteudo) > 3000:
                return conteudo[:3000] + "\n... (truncado)"
            return conteudo
        except FileNotFoundError:
            return f"Arquivo não encontrado: {path}"
        except Exception as e:
            return f"Erro ao ler arquivo: {e}"

    @cp.tool("escrever_arquivo", desc="Escreve conteúdo em um arquivo. Parâmetros: caminho (str), conteudo (str).")
    def escrever_arquivo(args: dict) -> str:
        path = args.get("caminho", "")
        conteudo = args.get("conteudo", "")
        if not path:
            return "Erro: caminho não informado."
        try:
            with open(os.path.expanduser(path), "w", encoding="utf-8") as f:
                f.write(conteudo)
            return f"Arquivo salvo: {path}"
        except Exception as e:
            return f"Erro ao escrever arquivo: {e}"

    @cp.tool("listar_dir", desc="Lista arquivos de um diretório. Parâmetro: caminho (str) — diretório (padrão: atual).")
    def listar_dir(args: dict) -> str:
        path = args.get("caminho", ".")
        try:
            entries = os.listdir(os.path.expanduser(path))
            if not entries:
                return f"Diretório vazio: {path}"
            return "\n".join(f"  {e}{'/' if os.path.isdir(os.path.join(path, e)) else ''}" for e in sorted(entries))
        except FileNotFoundError:
            return f"Diretório não encontrado: {path}"
        except Exception as e:
            return f"Erro ao listar: {e}"

    @cp.tool("terminal", desc=(
        "Ferramenta MAIS VERSÁTIL — use para QUALQUER operação que não tenha uma tool específica. "
        "Executa comandos no shell do sistema: instalar pacotes (apt, pip, npm), gerenciar processos, "
        "manipular arquivos, configurar rede, rodar scripts, tudo pelo terminal. "
        "Tem acesso sudo automático (não precisa perguntar senha). "
        "Parâmetro: comando (str) — comando shell completo a executar."
    ))
    def terminal(args: dict) -> str:
        cmd = args.get("comando", "")
        if not cmd:
            return "Erro: comando não informado."

        sudo_pass = os.getenv("SUDO_PASSWORD", "")

        if cmd.startswith("sudo ") and sudo_pass:
            cmd = cmd.replace("sudo ", f"echo '{sudo_pass}' | sudo -S ", 1)

        try:
            result = subprocess.run(
                ["/bin/bash", "-c", cmd],
                capture_output=True, text=True, timeout=60,
                cwd=os.path.expanduser("~"),
            )
            output = result.stdout + result.stderr
            return output.strip() or "Comando executado (sem saída)."
        except subprocess.TimeoutExpired:
            return "Comando excedeu 60s."
        except Exception as e:
            return f"Erro: {e}"

    @cp.tool("memoria", desc="Busca no histórico da conversa. Parâmetro: consulta (str) — termo a buscar.")
    def memoria(args: dict) -> str:
        return "Memória disponível no contexto atual da conversa."

    @cp.tool("lembrete", desc="Cria um lembrete persistente. Parâmetros: texto (str), quando (str) — ex: '5min', 'amanhã 9h'.")
    def lembrete(args: dict) -> str:
        texto = args.get("texto", "")
        quando = args.get("quando", "indefinido")
        if not texto:
            return "Erro: texto do lembrete não informado."

        path = os.path.expanduser("~/.joi/lembretes.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)

        try:
            with open(path, "r") as f:
                lembretes = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            lembretes = []

        lembretes.append({
            "texto": texto,
            "quando": quando,
            "criado_em": datetime.now().isoformat(),
        })

        with open(path, "w") as f:
            json.dump(lembretes, f, ensure_ascii=False, indent=2)

        return f"Lembrete criado: '{texto}' ({quando})"
