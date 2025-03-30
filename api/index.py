import os
import re
from flask import Flask, request, render_template
from pytubefix import YouTube
from moviepy.editor import VideoFileClip
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

def limpar_nome(nome):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', nome)

def baixar_video(url, pasta):
    yt = YouTube(url)
    titulo_limpo = limpar_nome(yt.title)
    video_path = os.path.join(pasta, f"{titulo_limpo}.mp4")
    audio_path = os.path.join(pasta, f"{titulo_limpo}.mp3")
    
    # Baixando o vídeo na maior resolução
    video_stream = yt.streams.get_highest_resolution()
    video_stream.download(output_path=pasta, filename=f"{titulo_limpo}.mp4")
    
    # Convertendo vídeo para áudio
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    video.close()
    
    # Baixando a transcrição
    obter_transcricao(url, pasta, titulo_limpo)

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

        # Exibe a mensagem de "Aguarde" após o envio do formulário
        return render_template("index.html", pasta=pasta, aguardando=True, url=url)

    return render_template("index.html", aguardando=False)

@app.route("/processar", methods=["POST"])
def processar():
    url = request.form["url"]
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    pasta = os.path.join(desktop, "Videos_Baixados")
    os.makedirs(pasta, exist_ok=True)

    # Baixa o vídeo, áudio e transcrição
    titulo = baixar_video(url, pasta)

    return render_template("index.html", pasta=pasta, titulo=titulo, url=url)

@app.route("/reset", methods=["POST"])
def reset():
    return render_template("index.html", pasta=None)

if __name__ == "__main__":
    app.run(debug=True)
