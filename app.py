from flask import Flask, render_template, request, send_from_directory, redirect, url_for, after_this_request
import re


from urllib.parse import urlparse, parse_qs
import yt_dlp
import os
import uuid

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# ✅ Fonction pour nettoyer l'URL YouTube
def clean_youtube_url(url):
    parsed = urlparse(url)
    query = parse_qs(parsed.query)
    video_id = query.get("v", [""])[0]
    return f"https://www.youtube.com/watch?v={video_id}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = clean_youtube_url(request.form['url'])
    format_type = request.form['format']

    # ✅ Extraire les infos de la vidéo
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'video')
    except Exception as e:
        return "❌ Vidéo introuvable ou lien invalide. Veuillez vérifier le lien YouTube.", 400


    # ✅ Nettoyer le titre
    safe_title = re.sub(r'[\\/*?:"<>|]', "", title)
    filename = safe_title if safe_title else str(uuid.uuid4())
    output_template = os.path.join(DOWNLOAD_FOLDER, filename + ".%(ext)s")

    # ✅ Options yt_dlp
  
    if format_type == 'mp3':
        ydl_opts = {
            'outtmpl': output_template,
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'cookiefile': 'cookies.txt',
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'

            }
        }
    else:  # format_type == 'mp4'
        ydl_opts = {
            'outtmpl': output_template,
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
            'quiet': True,
            'cookiefile': 'cookies.txt',
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            }
        }

    

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.download([url])
    except Exception as e:
        return f"Erreur lors du téléchargement : {str(e)}", 500

    # ✅ Trouver le fichier généré
    expected_ext = 'mp3' if format_type == 'mp3' else 'mp4'
    final_filename = f"{filename}.{expected_ext}"
    final_path = os.path.join(DOWNLOAD_FOLDER, final_filename)

    # ✅ Vérifie que le fichier existe
    if not os.path.exists(final_path):
        # Cherche un fichier avec une autre extension
        for f in os.listdir(DOWNLOAD_FOLDER):
            if f.startswith(filename):
                final_filename = f
                final_path = os.path.join(DOWNLOAD_FOLDER, f)
                break
        else:
            return f"Le fichier {filename} n'a pas été généré.", 500
    return request.host_url + 'download_file/' + final_filename

@app.route('/download_file/<filename>')
def download_file(filename):
    file_path = os.path.join(DOWNLOAD_FOLDER, filename)

    @after_this_request
    def remove_file(response):
        try:
            os.remove(file_path)
            print(f"✅ Fichier supprimé : {file_path}")
        except Exception as e:
            print(f"Erreur lors de la suppression du fichier : {e}")
        return response

    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
