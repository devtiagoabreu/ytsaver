# ytsaver

YouTube Saver é um aplicativo em Python com interface web que permite baixar vídeos do YouTube, extrair o áudio e capturar a transcrição (se disponível). Os arquivos são organizados em uma pasta no desktop do usuário.

## 📌 Funcionalidades
- 📥 Baixa vídeos do YouTube na melhor qualidade disponível.
- 🎵 Extrai o áudio do vídeo e salva como MP3.
- 📜 Obtém a transcrição do vídeo (se disponível) e salva como TXT.
- 📁 Cria automaticamente uma pasta chamada **Videos_Baixados** no Desktop para armazenar os arquivos.

## 🚀 Como instalar e executar
### 1️⃣ Instale as dependências
```bash
pip install flask pytube moviepy youtube-transcript-api
```

### 2️⃣ Execute o aplicativo
```bash
python app.py
```

### 3️⃣ Acesse no navegador
Abra o navegador e vá para:
```
http://127.0.0.1:5000
```

## 🖥️ Uso
1. Insira a URL do vídeo do YouTube no campo de texto.
2. Clique no botão **Baixar**.
3. Aguarde o download e processamento.
4. Os arquivos serão salvos na pasta **Videos_Baixados** no Desktop.

## 📂 Estrutura dos arquivos
```
📁 Videos_Baixados/
   📄 NomeDoVideo.mp4  (Vídeo)
   🎵 NomeDoVideo.mp3  (Áudio extraído)
   📜 NomeDoVideo.txt  (Transcrição, se disponível)
```

## 🛠️ Tecnologias usadas
- **Flask** → Interface web
- **pytube** → Download de vídeos
- **moviepy** → Extração de áudio
- **youtube_transcript_api** → Captura de transcrição

## 📌 Observações
- A transcrição só será salva se o vídeo tiver legendas ativadas pelo proprietário.
- O nome dos arquivos será formatado para evitar caracteres especiais.

## 📜 Licença
Este projeto é de uso livre para qualquer finalidade.
