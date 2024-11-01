# app.py

from flask import Flask, render_template, request, redirect, url_for
from dubbing import dublar_video  # Importar a função de dublagem
import tempfile
import os

app = Flask(__name__)

# Rota principal para renderizar a página inicial
@app.route('/')
def index():
    return render_template('upload.html', filename=None)

# Rota principal para renderizar a página inicial
@app.route('/video_processado')
def video_processado():

    return render_template('upload.html', filename='dubbed_video.mp4')

# Rota para processar o upload do vídeo e dublá-lo
@app.route('/process_video', methods=['POST'])
def process_video():
    video_file = request.files['video']
    file_extension = os.path.splitext(video_file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_video_file:
        video_path = temp_video_file.name
        video_file.save(video_path)
    final_video_path = dublar_video(video_path)
    return redirect(url_for('video_processado', filename=final_video_path))



if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8010)
