
import os
import subprocess
import uuid
from dotenv import load_dotenv
from google import genai
load_dotenv()
import logging

LOCAL_PATH = "./subtitles"
os.makedirs(LOCAL_PATH, exist_ok=True)

class Subtitles:

    def __init__(self):
        self.key       =   os.environ["GEMINI_KEY"] 

    def createSubTitle(self,videoPath:str) -> str:
        audioPath = self.extractAudioFromVideo(videoPath)

        subtitlesPath = self.sendAudioToGemini(audioPath)

        return subtitlesPath

    
    def extractAudioFromVideo(self, videoPath:str) -> str:
        audioId = uuid.uuid4().bytes
        audioIdStr = str(uuid.UUID(bytes=audioId))
        audioPath = f"{LOCAL_PATH}/{audioIdStr}.mp3"
        
        logging.info(f"Iniciando conversão de vídeo mp4 para mp3 para o caminho {audioPath}")
        
        cmd = ["ffmpeg", "-y","-i", videoPath,"-vn","-ar", "44100","-ac", "2","-b:a", "192k",audioPath]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
    
            if result.returncode != 0:
                logging.error(f"Erro na conversão de mp4 para mp3, erro que ocorreu(FFMPEG): {result.stderr}")
                raise ValueError("Ocorreu um erro ao converter o vídeo em streaming, tente novamente")
            
            logging.info(f"conversão de aúdio realizada com sucesso, áudio salvo em: {audioPath}")
            return audioPath
        except subprocess.CalledProcessError as e:
            logging.error(f"Erro na conversão de áudio (ffmpeg):\nSTDOUT: {e.stdout}\nSTDERR: {e.stderr}")
            return None
        except Exception as e:
            logging.error(f"Erro inesperado: {e}")
            return None
    
    def sendAudioToGemini(self,audioPath:str) -> str:
        try:
            logging.info(f"Iniciando o envio do audio para o gemini, caminho do arquivo enviado: {audioPath}")
            client = genai.Client(api_key=self.key)

            myfile = client.files.upload(file=audioPath)
            messageError = "Erro ao obter áudio"

            response = client.models.generate_content(model="gemini-2.5-flash",contents=[self.createPrompt(messageError),myfile],)
            subscribleId = uuid.uuid4().bytes
            subscribleIdStr = str(uuid.UUID(bytes=subscribleId))
            if response == messageError:
                logging.error(f"Não foi possível converter o áudio em legendas, gemini não identificou: {audioPath}")
                return None
        
            subtitlePath = f"{LOCAL_PATH}/{subscribleIdStr}.vtt"
        
            with open(subtitlePath, "w", encoding="utf-8") as f:
                f.write(response.text)
            
            logging.info(f"Legenda gerada com sucesso, caminho do arquvio gerado: {subtitlePath}")
            return subtitlePath
        except Exception as e:
            logging.error(f"Ocorreu um erro ao converter o áudio em legenda com gemini, erro que ocorreu: {e}")
            return None
        
    def createPrompt(self,messageError:str) -> str:
        prompt = f"""
        
            Transcreva completamente este áudio para o formato de legenda WEBVTT válido.

            Instruções:
                - Detecte e transcreva todas as falas no áudio em português.
                - Identifique corretamente os tempos de início e fim de cada trecho falado, no formato: HH:MM:SS.mmm --> HH:MM:SS.mmm.
                - A legenda deve começar com a linha: WEBVTT.
                - Entre cada bloco de legenda, deve haver uma linha em branco.
                - Cada bloco deve conter apenas o timestamp e a transcrição.
                - Não inclua cabeçalhos extras, comentários, explicações ou qualquer texto fora do padrão WEBVTT.
                - Quebre as legendas em trechos curtos de no máximo 2 linhas e não mais que 5 segundos cada.

            O conteúdo gerado deve ser apenas o arquivo .vtt completo e válido.

            Exemplo mínimo do formato esperado:

            WEBVTT

            00:00:00.000 --> 00:00:04.000
            Primeira frase falada no áudio.

            00:00:04.500 --> 00:00:08.000
            Segunda frase falada no áudio.

            Agora, transcreva o áudio enviado para um arquivo .vtt, seguindo exatamente essas regras.
            observação: Se não for possível traduzir retorne a seguinte mensagem: {messageError}
        """
         
        return prompt