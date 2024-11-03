from dubbing import dublar_video

import os

# procupar arquivos mp4 na pasta
arquivos_mp4 = [f for f in os.listdir(os.getcwd()) if f.endswith('.mp4')]

for arquivo in arquivos_mp4:
    arquivo_dublado = dublar_video(arquivo, 'pt')
    print(f"Dublicado {arquivo} -> {arquivo_dublado}")
    
