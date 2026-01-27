# Multi-stage build para otimizar o tamanho da imagem
FROM python:3.11-slim as builder

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema necessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar apenas requirements.txt primeiro (cache layer)
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage final - imagem limpa e menor
FROM python:3.11-slim

# Criar usuário não-root para segurança
RUN useradd -m -u 1000 streamlit && \
    apt-get update && \
    apt-get install -y --no-install-recommends postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar dependências Python do builder
COPY --from=builder /root/.local /home/streamlit/.local

# Copiar código da aplicação
COPY --chown=streamlit:streamlit . .

# Criar diretório para cache do Streamlit
RUN mkdir -p /home/streamlit/.streamlit && \
    chown -R streamlit:streamlit /home/streamlit/.streamlit

# Configurar PATH para binários locais do Python
ENV PATH=/home/streamlit/.local/bin:$PATH

# Mudar para usuário não-root
USER streamlit

# Expor porta padrão do Streamlit
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Comando para executar a aplicação
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true", "--server.fileWatcherType=none", "--browser.gatherUsageStats=false"]
