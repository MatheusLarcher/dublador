
import sys
import os
from dublador import *
from baixar_youtube import *



if __name__ == "__main__":
    
    if getattr(sys, 'frozen', False):
        pasta_atual = os.path.dirname(os.path.abspath(sys.executable))
    else:
        pasta_atual = os.path.dirname(os.path.abspath(__file__))
    

    arquivo_mp4 = r"C:\Users\Matheus\Downloads\The EASIEST and BEST Skyrim VR Mod List - FUS Installation Guide.mp4"
    
    video_baixado = os.path.join(pasta_atual, "video_baixado.mp4")

    baixar_youtube("https://www.youtube.com/watch?v=-GAk_jc4B4Q", video_baixado)
    arquivo_mp4 = video_baixado

    try:
        caminho_saida = os.path.join(pasta_atual, "video_dublado.mp4")
        arquivo_dublado = dublar_video(arquivo_mp4, caminho_saida, 'pt')
        logging.info(f"Dublando {arquivo_mp4} -> {arquivo_dublado}")
    except Exception as e:
        logging.error(f"Erro ao dublar {arquivo_mp4}: {e}")
        
    logging.info("Fim do processo")

