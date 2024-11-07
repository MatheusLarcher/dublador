from pytube import YouTube
import ffmpeg

# URL do vídeo do YouTube
url = "https://www.youtube.com/watch?v=ID_DO_VIDEO"

# Baixa o vídeo
yt = YouTube(url)
stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
download_path = stream.download()

# Converte para MP4 se necessário
output_path = download_path.replace(".mp4", "_converted.mp4")
ffmpeg.input(download_path).output(output_path).run()

print(f"Vídeo baixado e convertido com sucesso para {output_path}")
