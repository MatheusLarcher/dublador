import whisper
from deep_translator import GoogleTranslator
from gtts import gTTS
from pydub import AudioSegment
from pydub.effects import speedup
import tempfile
import os
import moviepy.editor as mp

# Função para carregar o modelo Whisper pré-treinado
def carregar_modelo_whisper(modelo="base"):
    return whisper.load_model(modelo)

# Função para transcrever áudio
def transcrever_audio(model, audio_path, language="en"):
    result = model.transcribe(audio_path, language=language, word_timestamps=True)
    return result["segments"]

# Função para traduzir texto usando Google Translator
def traduzir_texto(texto, source_lang='en', target_lang='pt'):
    translator = GoogleTranslator(source=source_lang, target=target_lang)
    return translator.translate(texto)

# Função para gerar áudio TTS de um texto em português
def gerar_audio_tts(texto_pt, idx, temp_dir):
    temp_audio_path = os.path.join(temp_dir, f"segment_{idx}.mp3")
    tts = gTTS(text=texto_pt, lang='pt')
    tts.save(temp_audio_path)
    return temp_audio_path

# Função para ajustar a velocidade do áudio e sincronizar a duração
def ajustar_velocidade(segmento_audio, duracao_original_ms):
    duracao_atual_ms = len(segmento_audio)
    if duracao_atual_ms > 0 and duracao_original_ms > 0:
        fator_velocidade = round(duracao_atual_ms / duracao_original_ms, 6)
        fator_velocidade = max(fator_velocidade, 1)
        segmento_audio = speedup(segmento_audio, playback_speed=fator_velocidade)
        segmento_audio = segmento_audio[:duracao_original_ms]
    else:
        segmento_audio = AudioSegment.silent(duration=max(1, duracao_original_ms))
    return segmento_audio

# Função principal que coordena o processo de tradução e sincronização
def dublar_audio(audio_path):
    # Carregar o modelo Whisper
    model = carregar_modelo_whisper("turbo") # base, small, medium, large, large-v3, turbo

    # Transcrever o áudio em inglês
    segments = transcrever_audio(model, audio_path, language="en")

    # Inicializar o áudio final e criar diretório temporário
    audio_final = AudioSegment.empty()
    with tempfile.TemporaryDirectory() as temp_dir:
        # Processar cada segmento
        for idx, segment in enumerate(segments):
            # Extrair e traduzir texto
            texto_en = segment['text']
            texto_pt = traduzir_texto(texto_en)
            segment['text_pt'] = texto_pt

            # Exibir informações do segmento
            print(f"Segmento {idx+1}:")
            print(f" - Início: {segment['start']}s")
            print(f" - Fim: {segment['end']}s")
            print(f" - Texto original: {texto_en}")
            print(f" - Texto traduzido: {texto_pt}")

            # Gerar áudio TTS e carregar o segmento de áudio
            temp_audio_path = gerar_audio_tts(texto_pt, idx, temp_dir)
            segmento_audio = AudioSegment.from_mp3(temp_audio_path)

            # Ajustar a velocidade e duração do áudio
            duracao_original_ms = (segment['end'] - segment['start']) * 1000
            segmento_audio = ajustar_velocidade(segmento_audio, duracao_original_ms)

            # Adicionar o segmento ao áudio final
            audio_final += segmento_audio

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio_file:
            caminho_audio_final = temp_audio_file.name
            # Exportar o áudio final sincronizado
            audio_final.export(caminho_audio_final, format="mp3")

    print("Processo concluído! O áudio traduzido e sincronizado está em 'output_audio_pt.mp3'.")
    return caminho_audio_final


def dublar_video(video_path):
    try:
        video = mp.VideoFileClip(video_path)
        
        # Create a temporary file for the extracted audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
            audio_path = temp_audio_file.name
            video.audio.write_audiofile(audio_path)

        # Processar o áudio para dublagem
        caminho_audio_final = dublar_audio(audio_path)

        final_video_path = os.path.join("static", f"dubbed_video.mp4")

        video = video.set_audio(mp.AudioFileClip(caminho_audio_final))
        video.write_videofile(final_video_path, codec='libx264')

        # Opcional: Remover arquivos intermediários
        os.remove(audio_path)
        os.remove(caminho_audio_final)
        
        return final_video_path

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
