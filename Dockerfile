FROM tiangolo/uwsgi-nginx-flask:python3.11

# Installer ffmpeg via pip (avec image compatible)
RUN pip install --no-cache-dir yt-dlp ffmpeg-python Flask

# Copier les fichiers de l'application
COPY ./ /app

# Définir le dossier de travail
WORKDIR /app

# Exposer le port utilisé par Flask
ENV PORT=10000
EXPOSE $PORT

# Lancer l'application Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=10000"]
