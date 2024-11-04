from moviepy.editor import VideoFileClip

def extrair_20_segundos(caminho_video, caminho_saida, inicio=0, duracao=20):
    """
    Extrai uma parte de 20 segundos de um vídeo.

    :param caminho_video: Caminho para o arquivo de vídeo original.
    :param caminho_saida: Caminho onde o vídeo cortado será salvo.
    :param inicio: Tempo de início da extração em segundos.
    :param duracao: Duração da extração em segundos (padrão é 20).
    """
    # Carrega o vídeo
    video = VideoFileClip(caminho_video)
    
    # Define o tempo de fim da extração
    fim = inicio + duracao
    
    # Garante que o tempo de fim não exceda a duração total do vídeo
    fim = min(fim, video.duration)
    
    # Corta o vídeo
    video_cortado = video.subclip(inicio, fim)
    
    # Salva o vídeo cortado
    video_cortado.write_videofile(caminho_saida, codec="libx264", audio_codec="aac")

# Exemplo de uso:
if __name__ == "__main__":
    caminho_video_original = r"C:\Users\mathe\Downloads\Nova pasta (2)\Running MPT-30B on CPU - You DON_T Need a GPU.mp4"
    caminho_video_saida = r"C:\Users\mathe\Downloads\Nova pasta (2)\2d_seg.mp4"
    
    # Extrair os primeiros 20 segundos
    extrair_20_segundos(caminho_video_original, caminho_video_saida)
    
    # Para extrair uma faixa específica, por exemplo, dos 30 aos 50 segundos:
    # extrair_20_segundos(caminho_video_original, "video_30_50s.mp4", inicio=30, duracao=20)
