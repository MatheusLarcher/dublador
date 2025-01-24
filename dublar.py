# dublar.py

from baixar_youtube import baixar_youtube
import sys
import tkinter as tk
from tkinter import ttk
import threading
from dubbing import dublar_video
from datetime import datetime

args = sys.argv
url = args[1] if len(args) > 1 else None

if not url:
    def on_submit():
        global url
        url = entry.get()
        progress_label.config(text="Iniciando o download...")
        download_thread = threading.Thread(target=start_download, daemon=True)
        download_thread.start()

    def update_progress(percent):
        progress_bar['value'] = percent
        progress_label.config(text=f"Progresso: {percent:.2f}%")

    def start_download():
        try:
            progress_bar['value'] = 1
            if url.startswith("http"):
                video_path_ingles = baixar_youtube(url)
            else:
                video_path_ingles = url
            progress_bar['value'] = 10
            modelo = "medium" #modelo_var.get()
            idioma_destino = idioma_var.get()
            caminho_video_saida = video_path_ingles.replace(".mp4", f"_dublado_{idioma_destino}.mp4")
            dublar_video(
                video_path_ingles,
                caminho_video_saida,
                modelo,
                idioma_destino,
                progress_callback=update_progress
            )
            progress_label.config(text="Download concluído!")
        except Exception as e:
            progress_label.config(text=f"Erro: {str(e)}")
        finally:
            button.config(state='normal')

    root = tk.Tk()
    root.title("YouTube Downloader")

    # Centraliza a janela
    window_width = 700
    window_height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    label = tk.Label(root, text="Digite a URL ou caminho local:", font=('Arial', 12))
    label.pack(pady=10)

    entry = tk.Entry(root, width=50, font=('Arial', 12))
    entry.pack(pady=10)

    # Combobox para escolher o modelo
    # tk.Label(root, text="Modelo:", font=('Arial', 12)).pack()
    # modelo_var = tk.StringVar(value="medium")
    # modelo_combo = ttk.Combobox(root, textvariable=modelo_var,
    #                             values=["medium", "large-v3-turbo"], state="readonly")
    # modelo_combo.pack(pady=5)

    # Combobox para escolher o idioma destino
    tk.Label(root, text="Idioma destino:", font=('Arial', 12)).pack()
    idioma_var = tk.StringVar(value="pt")
    idioma_combo = ttk.Combobox(root, textvariable=idioma_var,
                                values=["pt", "en", "es", "fr"], state="readonly")
    idioma_combo.pack(pady=5)

    button = tk.Button(root, text="Baixar e Dublar", command=lambda: [button.config(state='disabled'), on_submit()],
                       font=('Arial', 12))
    button.pack(pady=10)

    progress_bar = ttk.Progressbar(root, orient='horizontal', length=400, mode='determinate')
    progress_bar.pack(pady=10)

    progress_label = tk.Label(root, text="", font=('Arial', 10))
    progress_label.pack(pady=10)
    
    root.mainloop()

if not url:
    print("URL não fornecida. Encerrando...")
    sys.exit(1)
