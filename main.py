from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
import torch
import time

app = FastAPI(
    title="Classificador de Eventos JSON",
    description="API FastAPI para classificar eventos em contextos semânticos usando MiniLM",
    version="1.0.0"
)

# Carrega modelo global (uma única vez)
print("Carregando modelo de embeddings...")
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L6-v2')
model.to('cpu')
print("Modelo carregado com sucesso.")

# Cache simples em memória
cache_etapas = {}

# ---- Modelos de entrada e saída ----
class EventInput(BaseModel):
    event: dict
    etapas: list[str]


class ClassificationResponse(BaseModel):
    type: str
    to: str
    original_event: dict
    similarity_score: float
    processing_time_ms: float


@app.post("/classify", response_model=ClassificationResponse)
def classify_event(data: EventInput):
    """
    Recebe um JSON de evento e uma lista de etapas.
    Retorna a etapa mais próxima semanticamente.
    """
    start_time = time.time()

    event = data.event
    etapas = data.etapas

    # Descrição textual do evento
    texto_evento = " ".join([f"{k}: {v}" for k, v in event.items()])

    # Gera embedding do evento
    emb_evento = model.encode(texto_evento, convert_to_tensor=True)

    # Cache embeddings das etapas
    embeddings_etapas = []
    for etapa in etapas:
        if etapa not in cache_etapas:
            cache_etapas[etapa] = model.encode(etapa, convert_to_tensor=True)
        embeddings_etapas.append(cache_etapas[etapa])

    # Calcula similaridade
    emb_etapas_tensor = torch.stack(embeddings_etapas)
    sims = util.cos_sim(emb_evento, emb_etapas_tensor)[0]

    idx_melhor = int(torch.argmax(sims))
    etapa_escolhida = etapas[idx_melhor]
    score = float(sims[idx_melhor])

    total_time = (time.time() - start_time) * 1000  # ms

    return ClassificationResponse(
        type="mover",
        to=etapa_escolhida,
        original_event=event,
        similarity_score=round(score, 4),
        processing_time_ms=round(total_time, 2)
    )


@app.get("/")
def healthcheck():
    return {"status": "ok", "message": "API de classificação de eventos rodando!"}