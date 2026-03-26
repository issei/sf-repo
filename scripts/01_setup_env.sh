#!/bin/bash

# ==============================================================================
# Script: 01_setup_env.sh
# Objetivo: Configurar o ambiente operacional do Devin para Salesforce e Flosum
# Autor: Arquitetura de IA / DevOps
# ==============================================================================

# Habilita o "Fail-Fast": o script para imediatamente se qualquer comando falhar
set -e
# Garante que falhas em pipes (ex: echo "y" | comando) sejam capturadas
set -o pipefail

# Função de log padronizada para facilitar a leitura no terminal do Devin
log() {
    echo -e "\n[DEVIN ENV SETUP] 🔹 $1"
}

error_handler() {
    echo -e "\n[DEVIN ENV SETUP] ❌ ERRO CRÍTICO na linha $1. Abortando setup."
    exit 1
}

# Associa a função de erro ao sinal de saída de erro
trap 'error_handler $LINENO' ERR

log "Iniciando a preparação do ambiente autônomo..."

# 1. Verificação e Atualização do Node.js
# O Salesforce CLI e os plugins dependem fortemente de uma versão recente do Node.js
log "Verificando instalação do Node.js e NPM..."
if ! command -v npm &> /dev/null; then
    log "NPM não encontrado. Instalando Node.js (LTS)..."
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y nodejs
else
    log "Node.js atual: $(node -v)"
fi

# 2. Instalação do Salesforce CLI (sf v2)
log "Instalando Salesforce CLI (@salesforce/cli) globalmente..."
# Usamos npm para garantir que não dependemos de instaladores binários específicos do SO
npm install --global @salesforce/cli@latest

# Verifica se o SF CLI foi instalado corretamente
if ! command -v sf &> /dev/null; then
    echo "Falha ao instalar o Salesforce CLI."
    exit 1
fi

log "Salesforce CLI instalado com sucesso: $(sf version)"

# 3. Instalação de Plugins do Ecossistema (Silenciosa)
# O comando `echo "y"` evita que o prompt de confirmação de trust trave o Devin
log "Instalando plugin do Flosum (flosum-sfdx-plugin)..."
echo "y" | sf plugins install flosum-sfdx-plugin

log "Instalando Salesforce Code Analyzer (SFCA)..."
echo "y" | sf plugins install @salesforce/plugin-code-analyzer

log "Instalando Salesforce Data Move Utility (SFDMU) para Data Seeding..."
echo "y" | sf plugins install sfdmu

log "Instalando SFDX Git Delta (SGD) para empacotamento cirúrgico..."
echo "y" | sf plugins install sfdx-git-delta

# 4. Ajustes de Configuração Global do SFDX
log "Aplicando configurações globais de telemetria e limites..."
# Desabilita telemetria para evitar gargalos de rede ou prompts indesejados
sf config set disable-telemetry=true --global
# Aumenta o max-old-space-size do Node para lidar com a extração de metadados pesados (ex: Profiles)
export NODE_OPTIONS="--max-old-space-size=8192"

log "Ambiente configurado com sucesso! Resumo dos plugins instalados:"
sf plugins

log "Pronto para iniciar a autenticação (02_auth_orgs.sh)."
exit 0