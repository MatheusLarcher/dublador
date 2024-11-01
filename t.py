import whisper
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
from pydub import AudioSegment
from moviepy.editor import VideoFileClip, AudioFileClip

# Caminho do arquivo de entrada
arquivo_entrada = "1.mp4"

# Carrega o modelo Whisper
modelo = whisper.load_model("base")

# Transcreve o áudio
resultado = modelo.transcribe(arquivo_entrada, word_timestamps=True)

# Cria uma pasta para salvar os áudios traduzidos
if not os.path.exists('audio_traduzido'):
    os.makedirs('audio_traduzido')

# Lista para armazenar caminhos dos segmentos de áudio
lista_segmentos = []

for idx, segmento in enumerate(resultado['segments']):
    inicio = segmento['start']
    fim = segmento['end']
    texto_original = segmento['text']

    # Traduz o texto para português usando deep_translator
    texto_traduzido = GoogleTranslator(source='auto', target='pt').translate(texto_original)
    print(f"[{inicio} - {fim}] {texto_original}")
    print(texto_traduzido)

    # Converte o texto traduzido em áudio
    tts = gTTS(texto_traduzido, lang='pt', slow=False)
    caminho_arquivo = f"audio_traduzido/segmento_{idx}.mp3"
    tts.save(caminho_arquivo)
    lista_segmentos.append(caminho_arquivo)

# Concatena todos os segmentos de áudio
audio_final = AudioSegment.empty()
for caminho in lista_segmentos:
    segmento_audio = AudioSegment.from_mp3(caminho)
    audio_final += segmento_audio

# Exporta o áudio final concatenado
caminho_audio_final = "audio_traduzido/audio_final.mp3"
audio_final.export(caminho_audio_final, format="mp3")

# Verifica se o arquivo de entrada é um vídeo
extensao = os.path.splitext(arquivo_entrada)[1].lower()
extensoes_video = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']

if extensao in extensoes_video:
    # Carrega o vídeo original
    video_clip = VideoFileClip(arquivo_entrada)

    # Carrega o áudio traduzido
    audio_clip = AudioFileClip(caminho_audio_final)

    # Define o áudio traduzido como áudio do vídeo
    video_clip = video_clip.set_audio(audio_clip)

    # Exporta o novo vídeo com áudio traduzido
    video_clip.write_videofile("video_traduzido.mp4", codec='libx264', audio_codec='aac')

    print("Vídeo com áudio traduzido salvo como 'video_traduzido.mp4'.")

else:
    print("Arquivo de entrada não é um vídeo. O áudio traduzido foi salvo como 'audio_traduzido/audio_final.mp3'.")
