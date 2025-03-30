import os
import re
from flask import Flask, request, render_template, jsonify
from pytubefix import YouTube
from moviepy.editor import VideoFileClip
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

def limpar_nome(nome):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', nome)

# Função para tratar o progresso do download
def progresso_callback(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    progresso = (bytes_downloaded / total_size) * 100
    return progresso

def baixar_video(url, pasta):
    yt = YouTube(url)
    titulo_limpo = limpar_nome(yt.title)
    video_path = os.path.join(pasta, f"{titulo_limpo}.mp4")
    audio_path = os.path.join(pasta, f"{titulo_limpo}.mp3")
    
    # Obtém o stream de maior resolução
    video_stream = yt.streams.get_highest_resolution()
    
    # Baixando o vídeo com monitoramento do progresso
    video_stream.download(output_path=pasta, filename=f"{titulo_limpo}.mp4")
    
    # Extrai o áudio do vídeo
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    video.close()
    
    return titulo_limpo

def obter_transcricao(url, pasta, titulo):
    video_id = url.split("v=")[-1]
    try:
        transcricao = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt'])
        texto = "\n".join([item["text"] for item in transcricao])
        transcricao_path = os.path.join(pasta, f"{titulo}.txt")
        with open(transcricao_path, "w", encoding="utf-8") as f:
            f.write(texto)
    except Exception as e:
        print(f"Erro ao obter a transcrição: {e}")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        pasta = os.path.join(desktop, "Videos_Baixados")
        os.makedirs(pasta, exist_ok=True)
        
        # Realiza o download e transcrição
        titulo = baixar_video(url, pasta)
        obter_transcricao(url, pasta, titulo)
        
        return render_template("index.html", pasta=pasta, titulo=titulo)
    
    return render_template("index.html", pasta=None)

@app.route("/reset", methods=["GET"])
def reset():
    return render_template("index.html", pasta=None)

if __name__ == "__main__":
    app.run(debug=True)
