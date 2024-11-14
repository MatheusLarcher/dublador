import yt_dlp
import os
from datetime import datetime



def baixar_youtube(url):
    # Define o diretório de destino
    destino_final = 'downloads'
    os.makedirs(destino_final, exist_ok=True)
    
    # Define o modelo de nome do arquivo de saída
    outtmpl = os.path.join(destino_final, f'video_baixado{datetime.now().strftime("%Y%m%d%H%M%S")}.mp4')
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    pasta_cookies = os.path.join(pasta_atual, 'cookies.txt')
    ydl_opts = {
        'format': 'best',  # Escolhe a melhor qualidade de vídeo disponível
        'outtmpl': outtmpl,  # Define o caminho e nome do arquivo de saída
        'noplaylist': True,
        'cookies': pasta_cookies
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    # Retorna o caminho completo do arquivo baixado
    return outtmpl
