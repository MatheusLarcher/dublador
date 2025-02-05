from deep_translator import GoogleTranslator
from pydub import AudioSegment
import tempfile
import os
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import moviepy.video.fx.all as vfx
import whisper
from datetime import datetime
from TTS.utils.synthesizer import Synthesizer  # Importação do Coqui TTS
import torch

def dublar_video(arquivo_entrada, caminho_video_saida, idioma_destino='pt', progress_callback=None):
    # Carrega o modelo Whisper 
    modelo = whisper.load_model("base")
    
    # Transcreve o áudio
    resultado = modelo.transcribe(arquivo_entrada, word_timestamps=True, task='translate', temperature=0.0)
    
    # Verifica se o arquivo de entrada é um vídeo
    extensao = os.path.splitext(arquivo_entrada)[1].lower()
    extensoes_video = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']

    if extensao in extensoes_video:
        # Carrega o vídeo original
        video_clip = VideoFileClip(arquivo_entrada)
        duracao_total = video_clip.duration  # em segundos
    else:
        print("O arquivo de entrada não é um vídeo suportado.")
        return

    # Verifica antes de chamar
    if progress_callback:
        progress_callback(12)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Extrai o áudio do vídeo
        audio_path = os.path.join(temp_dir, "original_audio.wav")
        video_clip.audio.write_audiofile(audio_path)
        
        # Carrega o modelo TTS do Coqui
        model_name = "tts_models/multilingual/multi-dataset/your_tts"
        synthesizer = Synthesizer.from_pretrained(model_name)
        
        # Extrai a embedding do locutor a partir do áudio original
        speaker_embedding = synthesizer.compute_embedding(audio_path)
        
        video_segments = []
        total_segments = len(resultado['segments'])
        for idx, segmento in enumerate(resultado['segments']):
            if progress_callback:
                progresso = 12 + (idx / total_segments) * 87  # Ajusta para ir de 12 a 99
                progress_callback(progresso)
            
            inicio = segmento['start']
            fim = segmento['end']
            texto_original = segmento['text']

            # Traduz o texto para o idioma destino
            texto_traduzido = GoogleTranslator(source='en', target=idioma_destino).translate(texto_original)
            print(f"[{inicio:.2f} - {fim:.2f}] {texto_traduzido}")

            # Gera o áudio TTS usando Coqui TTS
            caminho_audio_segmento = os.path.join(temp_dir, f"segmento_{idx}.wav")
            # Gera o áudio TTS com a mesma voz do áudio original
            wav = synthesizer.tts(texto_traduzido, speaker_embedding=speaker_embedding, language=idioma_destino)
            # Salva o áudio
            synthesizer.save_wav(wav, caminho_audio_segmento)

            # Carrega o áudio TTS gerado
            segmento_audio = AudioSegment.from_wav(caminho_audio_segmento)
            duracao_tts = len(segmento_audio) / 1000  # em segundos

            # Extrai o segmento de vídeo correspondente
            video_segment = video_clip.subclip(inicio, fim)
            duracao_video_segmento = fim - inicio

            # Ajusta a duração do vídeo para corresponder ao áudio TTS
            if duracao_tts > duracao_video_segmento:
                # Estica o vídeo para corresponder à duração do áudio
                fator = duracao_tts / duracao_video_segmento
                video_segment = video_segment.fx(vfx.speedx, factor=1/fator)
            elif duracao_tts < duracao_video_segmento:
                # Estica o vídeo para corresponder à duração do áudio
                fator = duracao_tts / duracao_video_segmento
                video_segment = video_segment.fx(vfx.speedx, factor=1/fator)

            # Define o áudio TTS como áudio do segmento de vídeo
            audio_segment_clip = AudioFileClip(caminho_audio_segmento)
            video_segment = video_segment.set_audio(audio_segment_clip)

            # Adiciona o segmento processado à lista
            video_segments.append(video_segment)

        if progress_callback:
            progress_callback(99)

        # Concatena todos os segmentos de vídeo
        final_video = concatenate_videoclips(video_segments, method="compose")
        final_video.write_videofile(caminho_video_saida, codec='libx264', audio_codec='aac')
        
        if progress_callback:
            progress_callback(100)  # Indica que o processo foi concluído
        
        return caminho_video_saida
