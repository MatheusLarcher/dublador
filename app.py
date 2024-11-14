# app.py

from flask import Flask, render_template, request, redirect, url_for
from baixar_youtube import baixar_youtube # Importar a função de download do YouTube
from dubbing import dublar_video  # Importar a função de dublagem
import tempfile
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('upload.html', filename=None)

@app.route('/video_processado/<filename>')
def video_processado(filename):
    return render_template('upload.html', filename=filename)

@app.route('/process_video', methods=['POST'])
def process_video():
    youtube_url = request.form.get('youtube_url')
    video_file = request.files.get('video')

    if youtube_url:
        # Download do vídeo do YouTube usando yt-dlp
        video_path = baixar_youtube(youtube_url)

        # Dublar o vídeo baixado
        final_video_path = dublar_video(video_path)
    elif video_file:
        file_extension = os.path.splitext(video_file.filename)[1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_video_file:
            video_path = temp_video_file.name
            video_file.save(video_path)
        final_video_path = dublar_video(video_path)
    else:
        return "Nenhum vídeo ou URL fornecido.", 400

    return redirect(url_for('video_processado', filename=final_video_path))

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8010)
