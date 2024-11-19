import yt_dlp
import os

def baixar_youtube(url):
    # Define o diretório de destino
    destino_final = 'downloads'
    os.makedirs(destino_final, exist_ok=True)
    
    if os.path.isfile(url):
        outtmpl = url
    else:
        # Define o modelo de nome do arquivo de saída usando o título do vídeo
        outtmpl = os.path.join(destino_final, f"video_baixado.mp4")
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
