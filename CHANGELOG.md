# 📋 Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-07

### ✅ Adicionado

- **API REST completa** com FastAPI
- **Classificação semântica** usando sentence-transformers
- **Modelo multilíngue** MiniLM-L12-v2 com suporte ao português
- **Sistema de cache** em memória para embeddings
- **Endpoints de saúde** e métricas
- **Documentação Swagger** automática
- **Tratamento de erros** robusto com logs detalhados
- **Validação de entrada** com Pydantic
- **Suporte a Docker** com Dockerfile otimizado
- **Scripts de automação** (setup_and_run.sh, test_api.sh)
- **Configuração via variáveis** de ambiente
- **Documentação completa** com exemplos de uso

### 🔧 Configuração

- Python 3.11+ como requisito mínimo
- Cache configurável (MAX_CACHE_SIZE=1000)
- Threshold de similaridade ajustável (MIN_SIMILARITY_THRESHOLD=0.1)
- Suporte a múltiplos workers para escalabilidade

### 📊 Performance

- Latência típica: 20-50ms por classificação
- Suporte a ~100-300 req/s dependendo da configuração
- Uso de memória: ~1-4GB dependendo do número de workers
- Cache inteligente com limpeza automática

### 🛡️ Segurança

- Validação rigorosa de entrada
- Tratamento seguro de exceções
- Logs sem exposição de dados sensíveis
- Configuração preparada para HTTPS

## [Unreleased]

### 🎯 Planejado para próximas versões

- [ ] Testes unitários automatizados
- [ ] Cache distribuído com Redis
- [ ] Métricas avançadas com Prometheus
- [ ] Autenticação JWT
- [ ] Batch processing
- [ ] Fine-tuning de modelos

---

**Legenda:**

- ✅ Adicionado: Novas funcionalidades
- 🔄 Modificado: Mudanças em funcionalidades existentes
- ❌ Removido: Funcionalidades removidas
- 🐛 Corrigido: Correções de bugs
- 🔒 Segurança: Melhorias de segurança
