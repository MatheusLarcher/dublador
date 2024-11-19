import yt_dlp
import os
from datetime import datetime
import re

def sanitize_filename(name):
    # Remove caracteres proibidos em nomes de arquivos
    return re.sub(r'[\\/:"*?<>|]+', '', name)

def baixar_youtube(url, progress_callback=None):
    # Define o diretório de destino
    destino_final = 'downloads'
    os.makedirs(destino_final, exist_ok=True)

    # Define o modelo de nome do arquivo de saída usando o título do vídeo
    outtmpl = os.path.join(destino_final, '%(title)s.%(ext)s')
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    pasta_cookies = os.path.join(pasta_atual, 'cookies.txt')

    ydl_opts = {
        'format': 'best',  # Escolhe a melhor qualidade de vídeo disponível
        'outtmpl': outtmpl,  # Define o caminho e nome do arquivo de saída
        'noplaylist': True,
        'cookies': pasta_cookies,
        'progress_hooks': [progress_callback] if progress_callback else [],
        'restrictfilenames': True,  # Restringe caracteres no nome do arquivo
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_title = info_dict.get('title', 'video_baixado')
        # Sanitiza o título para uso no sistema de arquivos
        sanitized_title = sanitize_filename(video_title)
        ext = info_dict.get('ext', 'mp4')
        video_path = os.path.join(destino_final, f"{sanitized_title}.{ext}")

    # Retorna o caminho completo do arquivo baixado
    return video_path
