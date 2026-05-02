#!/usr/bin/env bash
# setup.sh — Instalação da Joi
# Uso: bash setup.sh

set -e

REPO_URL="https://github.com/marcosgabrielgomes110-collab/JOE-AGENT.git"
INSTALL_DIR="$HOME/.joi"
BIN_DIR="$HOME/.local/bin"
JOI_DIR="$INSTALL_DIR/joi"

echo "  + Joi - Instalacao +"
echo ""

# 1. Clone ou atualiza
if [ -d "$INSTALL_DIR" ]; then
    echo "  >> atualizando repositorio..."
    cd "$INSTALL_DIR"
    git pull
else
    echo "  >> clonando repositorio..."
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
    echo "  >> .env criado em $JOI_DIR/.env"
    echo "  >> EDITE O ARQUIVO com sua chave GROQ_API_KEY"
fi

# 4. Instala dependencias
echo "  >> instalando dependencias..."
pip install --break-system-packages rich requests 2>/dev/null || \
pip install rich requests 2>/dev/null || true

# 5. Cria atalho joi no PATH
mkdir -p "$BIN_DIR"
cat > "$BIN_DIR/joi" << 'SCRIPT'
#!/usr/bin/env bash
exec python3 "$HOME/.joi/joi/main.py" "$@"
SCRIPT
chmod +x "$BIN_DIR/joi"

# 6. Adiciona ao PATH se necessario
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    SHELL_CONFIG="$HOME/.bashrc"
    if [ -f "$HOME/.zshrc" ]; then
        SHELL_CONFIG="$HOME/.zshrc"
    fi
    echo "" >> "$SHELL_CONFIG"
    echo "# Joi" >> "$SHELL_CONFIG"
    echo "export PATH=\"\$PATH:$BIN_DIR\"" >> "$SHELL_CONFIG"
    echo "  >> PATH atualizado em $SHELL_CONFIG"
    echo "  >> execute: source $SHELL_CONFIG"
fi

echo ""
echo "  + instalacao concluida +"
echo "  joi          # inicia o chat"
echo "  joi --help   # ajuda"
echo ""
echo "  Antes de usar, edite suas credenciais:"
echo "  nano $JOI_DIR/.env"
