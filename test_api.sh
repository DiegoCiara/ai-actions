#!/bin/bash

# Script para testar a API do AI Analytics Service
set -e

BASE_URL="http://localhost:8000"

echo "🧪 Testando AI Analytics Service..."

# Teste 1: Health Check
echo "1️⃣  Testando health check..."
response=$(curl -s -w "HTTPSTATUS:%{http_code}" -X GET "$BASE_URL/")
http_code=$(echo $response | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')
body=$(echo $response | sed -e 's/HTTPSTATUS\:.*//g')

if [ $http_code -eq 200 ]; then
    echo "✅ Health check passou: $body"
else
    echo "❌ Health check falhou (código: $http_code)"
    exit 1
fi

# Teste 2: Classificação de evento
echo "2️⃣  Testando classificação de evento..."
test_payload='{
  "event": {
    "tipo": "pedido",
    "status": "processando",
    "cliente": "João Silva",
    "produto": "Notebook Dell"
  },
  "etapas": [
    "Recebimento do pedido",
    "Processamento",
    "Preparação para envio",
    "Enviado",
    "Entregue"
  ]
}'

response=$(curl -s -w "HTTPSTATUS:%{http_code}" \
  -X POST "$BASE_URL/classify" \
  -H "Content-Type: application/json" \
  -d "$test_payload")

http_code=$(echo $response | tr -d '\n' | sed -e 's/.*HTTPSTATUS://')
body=$(echo $response | sed -e 's/HTTPSTATUS\:.*//g')

if [ $http_code -eq 200 ]; then
    echo "✅ Classificação passou!"
    echo "📊 Resultado: $body" | jq '.'
else
    echo "❌ Classificação falhou (código: $http_code)"
    echo "📝 Resposta: $body"
    exit 1
fi

echo "🎉 Todos os testes passaram!"