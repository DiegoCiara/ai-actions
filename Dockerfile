FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Variáveis de ambiente recomendadas para desempenho
ENV OMP_NUM_THREADS=4
ENV TOKENIZERS_PARALLELISM=false

# Exponha porta
EXPOSE 8000

# Comando de execução com múltiplos workers (ideal para KVM4)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]