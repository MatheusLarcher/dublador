import whisper
from deep_translator import GoogleTranslator
from gtts import gTTS
from pydub import AudioSegment
from pydub.effects import speedup
import os
import shutil

# Função para carregar o modelo Whisper pré-treinado
def carregar_modelo_whisper(modelo="base"):
    return whisper.load_model(modelo)

# Função para transcrever áudio
def transcrever_audio(model, audio_path, language="en"):
    result = model.transcribe(audio_path, language=language)
    return result["segments"]

# Função para traduzir texto usando Google Translator
def traduzir_texto(texto, source_lang='en', target_lang='pt'):
    translator = GoogleTranslator(source=source_lang, target=target_lang)
    return translator.translate(texto)

# Função para gerar áudio TTS de um texto em português
def gerar_audio_tts(texto_pt, idx):
    tts = gTTS(text=texto_pt, lang='pt')
    temp_audio_path = f"temp_segments/segment_{idx}.mp3"
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
    model = carregar_modelo_whisper("base")

    # Transcrever o áudio em inglês
    segments = transcrever_audio(model, audio_path, language="en")

    # Inicializar o áudio final e criar pasta temporária
    audio_final = AudioSegment.empty()
    if not os.path.exists("temp_segments"):
        os.makedirs("temp_segments")

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
        temp_audio_path = gerar_audio_tts(texto_pt, idx)
        segmento_audio = AudioSegment.from_mp3(temp_audio_path)

        # Ajustar a velocidade e duração do áudio
        duracao_original_ms = (segment['end'] - segment['start']) * 1000
        segmento_audio = ajustar_velocidade(segmento_audio, duracao_original_ms)

        # Adicionar o segmento ao áudio final
        audio_final += segmento_audio

    caminho_audio_final = "output_audio_pt.mp3"
    # Exportar o áudio final sincronizado
    audio_final.export(caminho_audio_final, format="mp3")

    # Remover arquivos temporários
    shutil.rmtree("temp_segments")
    print("Processo concluído! O áudio traduzido e sincronizado está em 'output_audio_pt.mp3'.")
    return caminho_audio_final

