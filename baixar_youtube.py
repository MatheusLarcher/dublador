import yt_dlp
import os
from datetime import datetime



def baixar_youtube(url, caminho_saida):
    
    # Define o modelo de nome do arquivo de saída
    outtmpl = caminho_saida
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    pasta_cookies = os.path.join(pasta_atual, 'cookies.txt')
    ydl_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',  # Escolhe melhor vídeo e áudio combinados
    'outtmpl': outtmpl,
    'noplaylist': True,
    'cookies': pasta_cookies
}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    # Retorna o caminho completo do arquivo baixado
    return outtmpl
