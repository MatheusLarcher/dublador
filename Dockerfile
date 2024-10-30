# Use uma imagem base oficial do Python
FROM python:3.11.9

# Defina variáveis de ambiente para evitar a criação de arquivos .pyc e bufferização de saída
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instale dependências do sistema necessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie o arquivo requirements.txt e instale as dependências Python
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copie todo o código do projeto para o diretório de trabalho
COPY . .

# Assegure-se de que a pasta 'static/videos' exista
RUN mkdir -p static/videos

# Defina a variável de ambiente para o Flask
ENV FLASK_APP=app.py

# Exponha a porta que a aplicação Flask irá rodar
EXPOSE 8010

# Comando para rodar a aplicação Flask
CMD ["python", "app.py"]
