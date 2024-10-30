# app.py

from flask import Flask, render_template, request, redirect, url_for
import moviepy.editor as mp
import os
from dubbing import dublar_audio  # Importar a função de dublagem

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
    if 'video' not in request.files:
        return redirect(url_for('index'))
    
    video_file = request.files['video']
    if video_file.filename == '':
        return redirect(url_for('index'))
    
    # Salvar o vídeo enviado
    video_path = "uploaded_video.mp4"
    video_file.save(video_path)

    try:
        # Extrair áudio do vídeo
        video = mp.VideoFileClip(video_path)
        audio_path = "extracted_audio.wav"
        video.audio.write_audiofile(audio_path)

        # Processar o áudio para dublagem
        caminho_audio_final = dublar_audio(audio_path)

        # Adicionar áudio dublado ao vídeo original
        final_video_path = "static/dubbed_video.mp4"
        video = video.set_audio(mp.AudioFileClip(caminho_audio_final))
        video.write_videofile(final_video_path, codec='libx264')

        # Opcional: Remover arquivos intermediários
        os.remove(video_path)
        os.remove(audio_path)
        os.remove(caminho_audio_final)

        # Aqui você pode implementar o envio do vídeo final para o usuário
        # Por exemplo, renderizar uma página com um link para download
        return redirect(url_for('video_processado'))

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8010)
