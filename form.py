import sys
import os
import tkinter as tk
from tkinter import ttk
import threading
from baixar_youtube import baixar_youtube
from dublador import dublar_video
import subprocess

# Variáveis globais
url = None
arquivo_baixado = None

if getattr(sys, 'frozen', False):
    pasta_atual = os.path.dirname(os.path.abspath(sys.executable))
else:
    pasta_atual = os.path.dirname(os.path.abspath(__file__))

# Funções

def on_download():
    global url, arquivo_baixado
    url = entry.get()
    if not url:
        progress_label.config(text="Por favor, insira uma URL válida.")
        return
    
    progress_label.config(text="Baixando o vídeo...")
    console_output.insert(tk.END, "Iniciando download...\n")
    download_thread = threading.Thread(target=start_download, daemon=True)
    download_thread.start()

def on_dub():
    global arquivo_baixado
    progress_label.config(text="Dublando o vídeo...")
    console_output.insert(tk.END, "Iniciando dublagem...\n")
    dub_thread = threading.Thread(target=start_dub, daemon=True)
    dub_thread.start()

def on_open():
    global arquivo_baixado
    if arquivo_baixado and os.path.exists(arquivo_baixado):
        try:
            if sys.platform == "win32":
                os.startfile(arquivo_baixado)
            elif sys.platform == "darwin":
                subprocess.call(("open", arquivo_baixado))
            else:
                subprocess.call(("xdg-open", arquivo_baixado))
            console_output.insert(tk.END, "Abrindo vídeo...\n")
        except Exception as e:
            progress_label.config(text=f"Erro ao abrir o vídeo: {str(e)}")
            console_output.insert(tk.END, f"Erro ao abrir o vídeo: {str(e)}\n")
    else:
        progress_label.config(text="Nenhum vídeo baixado para abrir.")
        console_output.insert(tk.END, "Nenhum vídeo baixado para abrir.\n")

def on_open_folder():
    global arquivo_baixado
    if arquivo_baixado:
        pasta = os.path.dirname(arquivo_baixado)
        try:
            if sys.platform == "win32":
                os.startfile(pasta)
            elif sys.platform == "darwin":
                subprocess.call(("open", pasta))
            else:
                subprocess.call(("xdg-open", pasta))
            console_output.insert(tk.END, "Abrindo pasta do vídeo...\n")
        except Exception as e:
            progress_label.config(text=f"Erro ao abrir a pasta: {str(e)}")
            console_output.insert(tk.END, f"Erro ao abrir a pasta: {str(e)}\n")
    else:
        progress_label.config(text="Nenhum vídeo baixado para abrir a pasta.")
        console_output.insert(tk.END, "Nenhum vídeo baixado para abrir a pasta.\n")

def start_download():
    global arquivo_baixado
    try:
        arquivo_baixado = os.path.join(pasta_atual, "video_baixado.mp4")
        
        baixar_youtube(url, arquivo_baixado)
        progress_label.config(text="Download concluído!")
        console_output.insert(tk.END, "Download concluído!\n")
        dub_button.config(state='normal')
        open_folder_button.config(state='normal')
    except Exception as e:
        progress_label.config(text=f"Erro no download: {str(e)}")
        console_output.insert(tk.END, f"Erro no download: {str(e)}\n")
        download_button.config(state='normal')
    

def start_dub():
    global arquivo_baixado
    try:
        console_output.insert(tk.END, f"Arquivo baixado: {arquivo_baixado}\n")
        arquivo_dublado = os.path.join(pasta_atual, "video_dublado.mp4")
        console_output.insert(tk.END, f"Caminho do arquivo dublado: {arquivo_dublado}\n")
        dublar_video(arquivo_baixado, arquivo_dublado)
        progress_label.config(text=f"Dublagem concluída! Arquivo: {arquivo_dublado}")
        console_output.insert(tk.END, f"Dublagem concluída! Arquivo: {arquivo_dublado}\n")
    except Exception as e:
        progress_label.config(text=f"Erro na dublagem: {str(e)}")
        console_output.insert(tk.END, f"Erro na dublagem: {str(e)}\n")
    finally:
        dub_button.config(state='normal')

# Interface gráfica
root = tk.Tk()
root.title("YouTube Downloader e Dublador")

# Centraliza a janela
window_width = 700
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width / 2 - window_width / 2)
center_y = int(screen_height / 2 - window_height / 2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# Elementos
label = tk.Label(root, text="Digite a URL do vídeo:", font=('Arial', 12))
label.pack(pady=10)

entry = tk.Entry(root, width=50, font=('Arial', 12))
entry.pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=10)

download_button = tk.Button(frame, text="Baixar", command=lambda: [download_button.config(state='disabled'), on_download()], font=('Arial', 12))
download_button.grid(row=0, column=0, padx=10)

dub_button = tk.Button(frame, text="Dublar", command=lambda: [dub_button.config(state='disabled'), on_dub()], font=('Arial', 12), state='disabled')
dub_button.grid(row=0, column=1, padx=10)


open_folder_button = tk.Button(frame, text="Abrir Pasta", command=on_open_folder, font=('Arial', 12), state='disabled')
open_folder_button.grid(row=0, column=3, padx=10)

progress_label = tk.Label(root, text="", font=('Arial', 10))
progress_label.pack(pady=10)

console_frame = tk.Frame(root)
console_frame.pack(pady=10, fill=tk.BOTH, expand=True)

console_output = tk.Text(console_frame, wrap=tk.WORD, height=10, font=('Arial', 10))
console_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

console_scrollbar = tk.Scrollbar(console_frame, command=console_output.yview)
console_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

console_output.config(yscrollcommand=console_scrollbar.set)

root.mainloop()
