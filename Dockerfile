# Imagem base do Python
FROM python:3.12-slim

# Evita geração de .pyc e logs em tempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho dentro do conteiner
WORKDIR /app

# Instalação de dependências
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalação de dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia do código da aplicação
COPY . .

# Exposição de porta usada pela aplicação
EXPOSE 5000

# Comando para iniciar o servidor
CMD ["gunicorn", "--bind", "0.0.0.0:5000","wsgi:app"]
