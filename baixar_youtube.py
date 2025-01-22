import yt_dlp
import os

def baixar_youtube(url):
    # Define o diretório de destino
    destino_final = 'downloads'
    os.makedirs(destino_final, exist_ok=True)
    
    if os.path.isfile(url):
        outtmpl = url
    else:
        outtmpl = os.path.join(destino_final, "video_baixado.mp4")
        pasta_atual = os.path.dirname(os.path.abspath(__file__))
        pasta_cookies = os.path.join(pasta_atual, 'cookies.txt')

        # Primeira tentativa (best)
        ydl_opts_best = {
            'format': 'best',
            'outtmpl': outtmpl,
            'noplaylist': True,
            'cookies': pasta_cookies
        }

        # Segunda tentativa (bestvideo + bestaudio em MP4 ou fallback)
        ydl_opts_alternativo = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': outtmpl,
            'noplaylist': True,
            'cookies': pasta_cookies
        }

        # Tenta baixar com formato "best"
        try:
            with yt_dlp.YoutubeDL(ydl_opts_best) as ydl:
                ydl.download([url])
        except Exception as e:
            print(f"Falha ao baixar em 'best': {e}")
            print("Tentando formato alternativo...")
            # Se der erro, tenta o formato alternativo
            with yt_dlp.YoutubeDL(ydl_opts_alternativo) as ydl:
                ydl.download([url])

    return outtmpl
