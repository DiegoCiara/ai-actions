from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sentence_transformers import SentenceTransformer, util
import torch
import time
import logging
import os
from typing import Dict, List

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Classificador de Eventos JSON",
    description="API FastAPI para classificar eventos em contextos semânticos usando MiniLM",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Carrega modelo global (uma única vez)
logger.info("Carregando modelo de embeddings...")
try:
    model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    model.to('cpu')
    logger.info("Modelo carregado com sucesso.")
except Exception as e:
    logger.error(f"Erro ao carregar modelo: {e}")
    raise RuntimeError(f"Falha ao inicializar modelo: {e}")

# Cache simples em memória
cache_etapas = {}

# Configurações
MAX_CACHE_SIZE = int(os.getenv("MAX_CACHE_SIZE", "1000"))
MIN_SIMILARITY_THRESHOLD = float(os.getenv("MIN_SIMILARITY_THRESHOLD", "0.1"))

# ---- Modelos de entrada e saída ----
class EventInput(BaseModel):
    event: Dict = Field(..., description="Evento JSON para classificar", example={
        "tipo": "pedido",
        "status": "processando",
        "cliente": "João Silva"
    })
    etapas: List[str] = Field(..., min_items=1, description="Lista de etapas possíveis", example=[
        "Recebimento do pedido",
        "Processamento",
        "Enviado",
        "Entregue"
    ])


class ClassificationResponse(BaseModel):
    type: str = Field(description="Tipo de ação recomendada")
    to: str = Field(description="Etapa mais similar ao evento")
    original_event: Dict = Field(description="Evento original recebido")
    similarity_score: float = Field(description="Score de similaridade (0-1)")
    processing_time_ms: float = Field(description="Tempo de processamento em ms")


class HealthResponse(BaseModel):
    model_config = {"protected_namespaces": ()}

    status: str = Field(description="Status da API")
    message: str = Field(description="Mensagem informativa")
    model_loaded: bool = Field(description="Se o modelo está carregado")
    cache_size: int = Field(description="Tamanho atual do cache")


@app.post("/classify", response_model=ClassificationResponse)
def classify_event(data: EventInput):
    """
    Recebe um JSON de evento e uma lista de etapas.
    Retorna a etapa mais próxima semanticamente.
    """
    start_time = time.time()

    try:
        event = data.event
        etapas = data.etapas

        # Validações
        if not event:
            raise HTTPException(status_code=400, detail="Evento não pode estar vazio")

        if len(etapas) == 0:
            raise HTTPException(status_code=400, detail="Lista de etapas não pode estar vazia")

        # Descrição textual do evento
        try:
            texto_evento = " ".join([f"{k}: {v}" for k, v in event.items() if v is not None])
            if not texto_evento.strip():
                raise HTTPException(status_code=400, detail="Evento deve conter dados válidos")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Erro ao processar evento: {e}")

        # Gera embedding do evento
        try:
            emb_evento = model.encode(texto_evento, convert_to_tensor=True)
        except Exception as e:
            logger.error(f"Erro ao gerar embedding do evento: {e}")
            raise HTTPException(status_code=500, detail="Erro interno ao processar evento")

        # Cache embeddings das etapas (com limpeza se necessário)
        if len(cache_etapas) > MAX_CACHE_SIZE:
            logger.info(f"Limpando cache (tamanho: {len(cache_etapas)})")
            cache_etapas.clear()

        embeddings_etapas = []
        for etapa in etapas:
            if not etapa or not etapa.strip():
                continue
            if etapa not in cache_etapas:
                try:
                    cache_etapas[etapa] = model.encode(etapa, convert_to_tensor=True)
                except Exception as e:
                    logger.warning(f"Erro ao gerar embedding da etapa '{etapa}': {e}")
                    continue
            embeddings_etapas.append(cache_etapas[etapa])

        if not embeddings_etapas:
            raise HTTPException(status_code=400, detail="Nenhuma etapa válida encontrada")

        # Calcula similaridade
        try:
            emb_etapas_tensor = torch.stack(embeddings_etapas)
            sims = util.cos_sim(emb_evento, emb_etapas_tensor)[0]

            idx_melhor = int(torch.argmax(sims))
            etapa_escolhida = etapas[idx_melhor]
            score = float(sims[idx_melhor])

            # Verificar threshold mínimo
            if score < MIN_SIMILARITY_THRESHOLD:
                logger.warning(f"Similaridade baixa detectada: {score}")

        except Exception as e:
            logger.error(f"Erro no cálculo de similaridade: {e}")
            raise HTTPException(status_code=500, detail="Erro interno no cálculo de similaridade")

        total_time = (time.time() - start_time) * 1000  # ms

        logger.info(f"Classificação concluída: '{etapa_escolhida}' (score: {score:.4f}, tempo: {total_time:.2f}ms)")

        return ClassificationResponse(
            type="mover",
            to=etapa_escolhida,
            original_event=event,
            similarity_score=round(score, 4),
            processing_time_ms=round(total_time, 2)
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro inesperado na classificação: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor")


@app.get("/", response_model=HealthResponse)
def healthcheck():
    """
    Endpoint de verificação de saúde da API.
    """
    try:
        # Testar se o modelo está funcional
        test_encode = model.encode("teste", convert_to_tensor=True)
        model_loaded = True
    except Exception as e:
        logger.error(f"Modelo não está funcional: {e}")
        model_loaded = False

    return HealthResponse(
        status="ok" if model_loaded else "warning",
        message="API de classificação de eventos rodando!" if model_loaded else "API rodando mas modelo com problemas",
        model_loaded=model_loaded,
        cache_size=len(cache_etapas)
    )


@app.get("/metrics")
def get_metrics():
    """
    Endpoint com métricas básicas do sistema.
    """
    return {
        "cache_size": len(cache_etapas),
        "max_cache_size": MAX_CACHE_SIZE,
        "min_similarity_threshold": MIN_SIMILARITY_THRESHOLD,
        "model_device": str(model.device) if hasattr(model, 'device') else "unknown"
    }