#!/bin/bash

# Script para configurar e executar o AI Analytics Service
set -e

echo "🔧 Configurando AI Analytics Service..."

# Verificar se Python 3.11 está disponível
if ! command -v python3.11 &> /dev/null; then
    echo "⚠️  Python 3.11 não encontrado. Tentando usar python3..."
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python3.11"
fi

# Criar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    $PYTHON_CMD -m venv venv
fi

# Ativar ambiente virtual
echo "🔌 Ativando ambiente virtual..."
source venv/bin/activate

# Atualizar pip
echo "⬆️  Atualizando pip..."
pip install --upgrade pip

# Instalar dependências
echo "📚 Instalando dependências..."
pip install -r requirements.txt

# Verificar instalação
echo "✅ Verificando instalação..."
python -c "import fastapi, uvicorn, sentence_transformers, torch; print('Todas as dependências instaladas com sucesso!')"

echo "🚀 Configuração concluída! Iniciando servidor..."

# Iniciar servidor
uvicorn main:app --host 0.0.0.0 --port 8000 --reload