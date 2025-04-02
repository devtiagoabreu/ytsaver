# ytsaver

YouTube Saver é um aplicativo em Python com interface web que permite baixar vídeos do YouTube, extrair o áudio, capturar a transcrição (se disponível) e efetua resumos da mesma. Os arquivos são organizados em uma pasta no desktop do usuário.

## 📌 Funcionalidades
- 📥 Baixa vídeos do YouTube na melhor qualidade disponível.
- 🎵 Extrai o áudio do vídeo e salva como MP3.
- 📜 Obtém a transcrição do vídeo (se disponível) e salva como TXT.
- 📁 Cria automaticamente uma pasta chamada **Videos_Baixados** no Desktop para armazenar os arquivos.
- 🚀 Gera resumos da transcrição utilizando api gratuita do google

## 🚀 Como instalar e executar
### 1️⃣ Clone o repositório e configure o arquivo .env
```bash
git clone https://github.com/devtiagoabreu/ytsaver.git
```
OBS: ENTRE EM SUA CONTA GOOGLE, ACESSE [AISTUDIO](https://aistudio.google.com/apikey) E GERE SUA API KEY GRATUITAMENTE
Dentro da pasta raiz do projeto você encontrará o arquivo .env.exemple
Renomeie para .env 
Edite o arquivo inserindo sua APIKEY --> API_KEY_GOOGLE_AI = "COLE AQUI DENTRO DA ASPAS" E SALVE


### 1️⃣ Instale as dependências
```bash
pip install flask pytubefix moviepy==1.0.3 youtube-transcript-api
pip install -U google-generativeai 
```

### 2️⃣ Execute o aplicativo dentro da pasta API
```bash
python index.py
```

### 3️⃣ Acesse no navegador
Abra o navegador e vá para:
```
http://127.0.0.1:5000
```

## 🖥️ Uso
1. Insira a URL do vídeo do YouTube no campo de texto.
2. Clique no botão **Baixar Vídeo**.
3. Aguarde o download e processamento.
4. Os arquivos serão salvos na pasta **Videos_Baixados** no Desktop.

## 📂 Estrutura dos arquivos
```
📁 Videos_Baixados/
   📄 NomeDoVideo.mp4  (Vídeo)
   🎵 NomeDoVideo.mp3  (Áudio extraído)
   📜 NomeDoVideo.txt  (Transcrição, se disponível)
   📜 NomeDoVideo_resumo.txt  (Resumo da Transcrição)
```

## 🛠️ Tecnologias usadas
- **Flask** → Interface web
- **pytubefix** → Download de vídeos
- **moviepy** → Extração de áudio
- **youtube_transcript_api** → Captura de transcrição
- **google.generativeai** → Efetua resumos da transcrição pela API do gemini gratuita
- **obs** → ENTRE EM SUA CONTA GOOGLE, ACESSE [AISTUDIO](https://aistudio.google.com/apikey) E GERE SUA API KEY 


## 📌 Observações
- A transcrição só será salva se o vídeo tiver legendas ativadas pelo proprietário.
- O nome dos arquivos será formatado para evitar caracteres especiais.
- A API KEY gratuita geralmente possui uma limitação. Sendo assim alguns resumos podem não ser carregados, conforme o tamanho do texto de transcrição.

## 📜 Licença
Este projeto é de uso livre para qualquer finalidade.

Codado com muito entusiasmo e filhas no colo ♥ by [Tiago de Abreu](http://atriostech.com.br/tiago/) :wave: 
[![Linkedin Badge](https://img.shields.io/badge/-tiagodeabreu-blue?style=flat-square&logo=Linkedin&logoColor=white&link=https://www.linkedin.com/in/tiago-de-abreu-8020b5b1/)](https://www.linkedin.com/in/tiago-de-abreu-8020b5b1/)
[![Gmail Badge](https://img.shields.io/badge/-devtiagoabreu@gmail.com-c14438?style=flat-square&logo=Gmail&logoColor=white&link=mailto:devtiagoabreu@gmail.com)](mailto:devtiagoabreu@gmail.com)
