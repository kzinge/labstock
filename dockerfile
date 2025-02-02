# Usando uma imagem oficial do Python
FROM python:3.11

# Definindo o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiando os arquivos do projeto para o contêiner
COPY . .

# Instalando as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Definindo a variável de ambiente para evitar problemas de buffer de saída
ENV PYTHONUNBUFFERED=1

# Expondo a porta do Flask
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "app.py"]
