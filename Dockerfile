
# Utiliser une image de base officielle de Python
FROM python:3.9-slim

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de l'application dans le conteneur
COPY . /app

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port sur lequel l'application va s'exécuter
EXPOSE 5000

# Définir la commande de démarrage de l'application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
