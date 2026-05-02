#!/usr/bin/env bash
# setup.sh — Instalação da Joi
# Uso: bash setup.sh

set -e

REPO_URL="https://github.com/marcosgabrielgomes110-collab/JOE-AGENT.git"
INSTALL_DIR="$HOME/.joi"
BIN_DIR="$HOME/.local/bin"
JOI_DIR="$INSTALL_DIR/joi"
VENV_DIR="$INSTALL_DIR/venv"

echo "  + Joi - Instalacao +"
echo ""

# 1. Clone ou atualiza
if [ -d "$INSTALL_DIR" ]; then
    echo "  >> atualizando..."
    cd "$INSTALL_DIR"
    git pull
else
    echo "  >> clonando..."
    git clone "$REPO_URL" "$INSTALL_DIR"
fi

# 2. Cria estrutura de dados
mkdir -p "$JOI_DIR/data/sessions"
mkdir -p "$JOI_DIR/data/logs"
mkdir -p "$JOI_DIR/data/cache"
mkdir -p "$JOI_DIR/skills"
mkdir -p "$JOI_DIR/tools"

# 3. .env se nao existir
if [ ! -f "$JOI_DIR/.env" ]; then
    cp "$JOI_DIR/.env.example" "$JOI_DIR/.env"
    echo "  >> .env criado"
    echo "  >> EDITE O ARQUIVO com sua chave GROQ_API_KEY"
fi

# 4. Cria virtualenv e instala dependencias
echo "  >> criando virtualenv..."
python3 -m venv "$VENV_DIR"
echo "  >> instalando dependencias (rich, requests)..."
"$VENV_DIR/bin/pip" install --quiet rich requests 2>&1 | tail -1
echo "  >> dependencias instaladas"

# 5. Cria atalho joi no PATH
mkdir -p "$BIN_DIR"
cat > "$BIN_DIR/joi" << 'SCRIPT'
#!/usr/bin/env bash
INSTALL_DIR="$HOME/.joi"
VENV_PYTHON="$INSTALL_DIR/venv/bin/python"
MAIN_PY="$INSTALL_DIR/joi/main.py"

case "${1:-}" in
    --help|-h)
        echo "Joi - Assistente Pessoal Autonoma"
        echo ""
        echo "  joi            inicia o chat"
        echo "  joi --uninstall remove a instalacao"
        echo "  joi --help     mostra esta ajuda"
        ;;
    --uninstall)
        echo "Removendo Joi..."
        rm -f "$HOME/.local/bin/joi"
        rm -rf "$INSTALL_DIR"
        echo "Joi removida."
        ;;
    *)
        exec "$VENV_PYTHON" "$MAIN_PY" "$@"
        ;;
esac
SCRIPT
chmod +x "$BIN_DIR/joi"

# 6. Adiciona ao PATH se necessario
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    SHELL_CONFIG="$HOME/.bashrc"
    [ -f "$HOME/.zshrc" ] && SHELL_CONFIG="$HOME/.zshrc"
    echo "" >> "$SHELL_CONFIG"
    echo "# Joi" >> "$SHELL_CONFIG"
    echo "export PATH=\"\$PATH:$BIN_DIR\"" >> "$SHELL_CONFIG"
    echo "  >> PATH atualizado em $SHELL_CONFIG"
    echo "  >> execute: source $SHELL_CONFIG"
fi

echo ""
echo "  + instalacao concluida +"
echo "  joi              inicia o chat"
echo "  joi --uninstall  remove"
echo ""
echo "  Antes de usar, edite:"
echo "  nano $JOI_DIR/.env"
