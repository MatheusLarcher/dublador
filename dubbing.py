import whisper
from deep_translator import GoogleTranslator
from gtts import gTTS
from pydub import AudioSegment
import tempfile
import os
from moviepy.editor import VideoFileClip, AudioFileClip
import shutil

def dublar_video(arquivo_entrada, idioma_destino='pt'):
    """
    Transcreve o áudio de um arquivo, traduz cada segmento para o idioma desejado,
    converte os textos traduzidos em áudio e sobrepõe ao vídeo original se for um vídeo.

    Parâmetros:
    - arquivo_entrada (str): Caminho do arquivo de áudio ou vídeo.
    - idioma_destino (str): Código do idioma para tradução e síntese de voz (padrão é 'pt' para português).
    """

    # Carrega o modelo Whisper
    modelo = whisper.load_model("base")

    # Transcreve o áudio
    resultado = modelo.transcribe(arquivo_entrada, word_timestamps=True)

    # Cria uma pasta para salvar os áudios traduzidos temporaria
    with tempfile.TemporaryDirectory() as pasta_audio:
        # Lista para armazenar caminhos dos segmentos de áudio
        lista_segmentos = []

        for idx, segmento in enumerate(resultado['segments']):
            inicio = segmento['start']
            fim = segmento['end']
            texto_original = segmento['text']

            # Traduz o texto para o idioma destino usando deep_translator
            texto_traduzido = GoogleTranslator(source='auto', target=idioma_destino).translate(texto_original)
            print(f"[{inicio} - {fim}] {texto_traduzido}")

            # Converte o texto traduzido em áudio
            tts = gTTS(texto_traduzido, lang=idioma_destino)
            caminho_arquivo = os.path.join(pasta_audio, f"segmento_{idx}.mp3")
            tts.save(caminho_arquivo)
            lista_segmentos.append(caminho_arquivo)

        # Concatena todos os segmentos de áudio
        audio_final = AudioSegment.empty()
        for caminho in lista_segmentos:
            segmento_audio = AudioSegment.from_mp3(caminho)
            audio_final += segmento_audio

        # Exporta o áudio final concatenado
        caminho_audio_final = os.path.join(pasta_audio, "audio_final.mp3")
        audio_final.export(caminho_audio_final, format="mp3")

        # Verifica se o arquivo de entrada é um vídeo
        extensao = os.path.splitext(arquivo_entrada)[1].lower()
        extensoes_video = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']

        if extensao in extensoes_video:
            # Carrega o vídeo original
            video_clip = VideoFileClip(arquivo_entrada)

            # Ajusta a duração do áudio traduzido para corresponder à duração do vídeo
            duracao_video = video_clip.duration
            audio_clip = AudioFileClip(caminho_audio_final).set_duration(duracao_video)

            # Define o áudio traduzido como áudio do vídeo
            video_clip = video_clip.set_audio(audio_clip)

            # Exporta o novo vídeo com áudio traduzido
            video_saida = os.path.join("static", f"dubbed_video.mp4")
            with tempfile.NamedTemporaryFile(suffix=".mp4") as temp_video_file:
                video_clip.write_videofile(temp_video_file, codec='libx264', audio_codec='aac')
                shutil.copy(temp_video_file.name, video_saida)

            print(f"Vídeo com áudio traduzido salvo como '{video_saida}'.")
            return video_saida
        else:
            print(f"Arquivo de entrada não é um vídeo. O áudio traduzido foi salvo como '{caminho_audio_final}'.")
            return caminho_audio_final

    


#traduzir_e_sobrepor_audio("1.mp4", idioma_destino='pt')