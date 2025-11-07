# AI Analytics Service

Serviço de classificação semântica de eventos JSON usando FastAPI e sentence-transformers.

## 🚀 Funcionalidades

- **Classificação Semântica**: Classifica eventos JSON em etapas usando similaridade semântica
- **Cache Inteligente**: Cache em memória para embeddings de etapas
- **API REST**: Interface HTTP simples e documentada
- **Suporte Multilíngue**: Modelo MiniLM suporta múltiplos idiomas

## 🛠️ Requisitos

- Python 3.11+
- Memória: ~1GB (para carregar o modelo)
- CPU: Mínimo 2 cores (recomendado 4+)

## ⚡ Instalação e Execução Rápida

### Opção 1: Script Automatizado (Recomendado)

```bash
./setup_and_run.sh
```

### Opção 2: Manual

```bash
# Criar ambiente virtual
python3.11 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Executar servidor
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Opção 3: Docker

```bash
# Construir imagem
docker build -t ai-analytics-service .

# Executar container
docker run -p 8000:8000 ai-analytics-service
```

## 🧪 Testes

```bash
# Executar testes automatizados
./test_api.sh
```

## 📖 Uso da API

### Health Check

```bash
curl -X GET "http://localhost:8000/"
```

### Classificar Evento

```bash
curl -X POST "http://localhost:8000/classify" \
  -H "Content-Type: application/json" \
  -d '{
    "event": {
      "tipo": "pedido",
      "status": "processando",
      "cliente": "João Silva"
    },
    "etapas": [
      "Recebimento do pedido",
      "Processamento",
      "Enviado",
      "Entregue"
    ]
  }'
```

### Resposta

```json
{
  "type": "mover",
  "to": "Processamento",
  "original_event": {
    "tipo": "pedido",
    "status": "processando",
    "cliente": "João Silva"
  },
  "similarity_score": 0.8945,
  "processing_time_ms": 45.23
}
```

## 📊 Documentação Interativa

Acesse `http://localhost:8000/docs` para a documentação Swagger automática.

## 🔧 Configurações de Performance

### Variáveis de Ambiente

```bash
export OMP_NUM_THREADS=4
export TOKENIZERS_PARALLELISM=false
```

### Múltiplos Workers

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2
```

## 🐛 Solução de Problemas

### Erro de NumPy

Se encontrar erros relacionados ao NumPy:

```bash
pip install "numpy<2.0"
pip install --force-reinstall sentence-transformers torch
```

### Erro de Memória

Para ambientes com pouca memória, use um worker único:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1
```

### Modelo não carrega

Verifique se tem pelo menos 1GB de RAM disponível e conexão com internet para download inicial do modelo.

## 🏗️ Estrutura do Projeto

```
ai-analytics-service/
├── main.py              # Aplicação principal FastAPI
├── requirements.txt     # Dependências Python
├── Dockerfile          # Configuração Docker
├── setup_and_run.sh   # Script de instalação automática
├── test_api.sh         # Testes automatizados
├── .python-version     # Versão Python especificada
├── .gitignore         # Arquivos ignorados pelo Git
└── README.md          # Esta documentação
```

## 📈 Monitoramento

- **Logs**: Uvicorn fornece logs detalhados
- **Métricas**: Tempo de processamento incluído na resposta
- **Health**: Endpoint `/` para verificação de saúde

## 🔒 Segurança

Para produção, considere:

- Configurar CORS adequadamente
- Implementar rate limiting
- Usar HTTPS
- Validação adicional de entrada
- Autenticação/autorização

## 📄 Licença

Projeto interno - Todos os direitos reservados.
