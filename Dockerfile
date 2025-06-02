FROM jrottenberg/ffmpeg:4.4-ubuntu

# Installe Python et pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Crée le dossier de travail
WORKDIR /app

# Copie les fichiers de l'application
COPY . .

# Installe les dépendances Python
RUN pip3 install --no-cache-dir -r requirements.txt

# Variables d'environnement Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PORT=10000
EXPOSE $PORT
# Commande de démarrage
CMD ["flask", "run", "--port=10000"]
