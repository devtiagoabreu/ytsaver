import os
import re
from flask import Flask, request, render_template
from pytubefix import YouTube  # Usando pytubefix
from moviepy.editor import VideoFileClip
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

app = Flask(__name__)

def limpar_nome(nome):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', nome)

def baixar_video(url, pasta):
    yt = YouTube(url)  # Usando pytubefix aqui
    titulo_limpo = limpar_nome(yt.title)
    
    # Baixar o vídeo na maior resolução possível
    video_stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by('resolution').desc().first()
    video_path = os.path.join(pasta, f"{titulo_limpo}.mp4")
    audio_path = os.path.join(pasta, f"{titulo_limpo}.mp3")
    
    # Fazendo o download do vídeo
    video_stream.download(output_path=pasta, filename=f"{titulo_limpo}.mp4")
    
    # Convertendo o áudio
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    video.close()
    return titulo_limpo

def obter_transcricao(url, pasta, titulo):
    video_id = url.split("v=")[-1]
    try:
        # Tentando obter a transcrição em português (pt)
        transcricao = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt'])
        texto = "\n".join([item["text"] for item in transcricao])
        transcricao_path = os.path.join(pasta, f"{titulo}.txt")
        with open(transcricao_path, "w", encoding="utf-8") as f:
            f.write(texto)
    except TranscriptsDisabled:
        # Caso o vídeo tenha transcrição desabilitada
        print("Transcrição desabilitada para este vídeo.")
    except Exception as e:
        # Tratando outros erros
        print(f"Erro ao obter a transcrição: {e}")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        pasta = os.path.join(desktop, "Videos_Baixados")
        os.makedirs(pasta, exist_ok=True)
        
        titulo = baixar_video(url, pasta)
        obter_transcricao(url, pasta, titulo)
        
        return f"Download concluído! Arquivos salvos em {pasta}"  
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
