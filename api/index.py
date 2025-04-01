import os
import re
import dotenv 
from flask import Flask, request, render_template
from pytubefix import YouTube
from moviepy.editor import VideoFileClip
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai

# Carregar variáveis de ambiente
dotenv.load_dotenv()

app = Flask(__name__, template_folder="../templates")

# Configurar a API Key
genai.configure(api_key=os.getenv("API_KEY_GOOGLE_AI"))
##genai.configure(api_key="AIzaSyAgYRfAzc_4iITAXZ13qotOFeutna8a6Vo")


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

        # Salvar transcrição completa
        transcricao_path = os.path.join(pasta, f"{titulo}.txt")
        with open(transcricao_path, "w", encoding="utf-8") as f:
            f.write(texto)

        # Gerar e salvar resumo
        resumo = resumir_transcricao(texto)
        resumo_path = os.path.join(pasta, f"{titulo}_resumo.txt")
        with open(resumo_path, "w", encoding="utf-8") as f:
            f.write(resumo)

         # Gerar e salvar contúdo para tabnews
        resumo = gerar_conteudo_para_tabnews_da_transcricao(texto)
        resumo_path = os.path.join(pasta, f"{titulo}_conteudo_tabnews.txt")
        with open(resumo_path, "w", encoding="utf-8") as f:
            f.write(resumo)

        # Gerar e salvar contúdo para rede social
        resumo = gerar_conteudo_para_rede_social_da_transcricao(texto)
        resumo_path = os.path.join(pasta, f"{titulo}_conteudo_rede_social.txt")
        with open(resumo_path, "w", encoding="utf-8") as f:
            f.write(resumo)

        # Gerar e salvar Reunião empresarial
        resumo = criar_reuniao_empresarial_da_transcricao(texto)
        resumo_path = os.path.join(pasta, f"{titulo}_reuniao_empresarial.txt")
        with open(resumo_path, "w", encoding="utf-8") as f:
            f.write(resumo)
        
    except Exception as e:
        print(f"Erro ao obter a transcrição: {e}")

def carregar_prompt():
    """Lê o prompt de um arquivo externo."""
    prompt_path = os.path.join(os.path.dirname(__file__), "prompt.txt")
    if os.path.exists(prompt_path):
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return "Resuma este texto em 3 partes: 1) Descrição clara (3000 chars); 2) Tópicos-chave em tópicos; 3) Plano de estudo com fontes (livros, artigos). Mantenha acadêmico e direto, no final crie mais um tópico como se fosse um post em um blog especializado sobre o assunto, com estudos sobre o assunto e com emojis para ficar bonito, crie tags para ligar informações no obsidian logo no final de acordo com o resumo gerado, Título criativo** (usar emojis e trocadilhos, ex: 'Async/Await: O Herói Sem Capa do JavaScript', Formato Markdown:"  # Caso o arquivo não exista

def resumir_transcricao(texto):
    """Gera um resumo da transcrição com um prompt personalizado."""
    try:
        prompt = carregar_prompt()
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(f"{prompt}\n\n{texto}")
        return response.text
    except Exception as e:
        return f"Erro ao gerar resumo: {str(e)}"

def gerar_conteudo_para_tabnews_da_transcricao(texto):
    """Gera um resumo da transcrição com um prompt personalizado."""
    try:
        prompt = "Transforme esta transcrição de vídeo em um **artigo didático para o TabNews**, mas o conteúdo precisa parecer orinal, escrito por um programador experiente, seguindo o estilo Filipe Deschamps, Tom Descontraído, mas técnico e Direto ao ponto, com piadinhas nerds e analogias fáceis de entender (ex: 'Isso é tipo um `console.log` da vida real') - Título criativo** (usar emojis e trocadilhos, ex: 'Async/Await: O Herói Sem Capa do JavaScript', Formato Markdown, Tá, mas como funciona? Tópicos técnicos em **lista simples**, com código snippets (se aplicável), Exemplo prático, Ênfase em **'por que isso importa'** (ex: 'Isso evita aquele loop infernal de callbacks!') Dica Pro Insights úteis que não estão óbvios no vídeo) Bônus: Links Úteis [Documentação]() | [Ferramenta]() | [Artigo Relacionado]() , crie tags para ligar informações no obsidian logo no final de acordo com o resumo gerado"
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(f"{prompt}\n\n{texto}")
        return response.text
    except Exception as e:
        return f"Erro ao gerar resumo: {str(e)}"

def criar_reuniao_empresarial_da_transcricao(texto):
    """Gera um resumo da transcrição com um prompt personalizado."""
    try:
        prompt = "Deste texto, selecione os tópicos, crie um título e comentário para cada para ser usado em uma reunião empresarial, crie tags para ligar informações no obsidian logo no final de acordo com o resumo gerado"
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(f"{prompt}\n\n{texto}")
        return response.text
    except Exception as e:
        return f"Erro ao gerar resumo: {str(e)}"
    
def gerar_conteudo_para_rede_social_da_transcricao(texto):
    """Gera um resumo da transcrição com um prompt personalizado."""
    try:
        prompt = "Deste texto, gere contúdos para redes sociais nos formatos de reels, shorts e storys, com a Estrutura em 'F' de atenção (layout que guia o olhar do usuário, comum em design), no Formato de storytelling (Introdução → Conflito → Clímax → Resolução) e Fórmulas de copywriting (como AIDA: Atenção, Interesse, Desejo, Ação), crie tags para ligar informações no obsidian logo no final de acordo com o resumo gerado."
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(f"{prompt}\n\n{texto}")
        return response.text
    except Exception as e:
        return f"Erro ao gerar resumo: {str(e)}"
    
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
