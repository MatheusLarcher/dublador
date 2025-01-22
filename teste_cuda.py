
import whisper
modelo = whisper.load_model("large-v3").cuda()

arquivo_entrada = r"C:\Users\Matheus\Downloads\12 Insane Skyrim Mods You Need To Try.mp4"

resultado = modelo.transcribe(arquivo_entrada, word_timestamps=True, task='translate', temperature=0.0)


for segment in resultado['segments']:
    print(segment['text'])
    print(segment['start'])
    print(segment['end'])
    print('-'*100)

