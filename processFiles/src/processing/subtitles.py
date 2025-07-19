
import os
import re
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

        if not self.isFileSizeAllowed(audioPath):
            return None

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

            messageError = "Erro ao obter áudio"

            myfile = client.files.upload(file=audioPath)
            print(myfile)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[self.createPrompt(messageError), myfile],
                stream=False,              
                automatic_function_calling=None,  
                )
            subscribleId = uuid.uuid4().bytes
            subscribleIdStr = str(uuid.UUID(bytes=subscribleId))
            if response.text == messageError:
                logging.error(f"Não foi possível converter o áudio em legendas, gemini não identificou: {audioPath}")
                return None
        
            subtitlePath = f"{LOCAL_PATH}/{subscribleIdStr}.vtt"
            correction = self.correctTimesTamp(response.text)

            with open(subtitlePath, "w", encoding="utf-8") as f:
                f.write(correction)
  
            
            logging.info(f"Legenda gerada com sucesso, caminho do arquvio gerado: {subtitlePath}")
            
            self.deleteAudioFileLocally(audioPath)
            
            return subtitlePath
        except Exception as e:
            logging.error(f"Ocorreu um erro ao converter o áudio em legenda com gemini, erro que ocorreu: {e}")
            return None
    
    def deleteAudioFileLocally(self,audioPath:str)-> None:
        try:
            logging.info(f"Deletando audio .mp3 que está no caminho: {audioPath}")
            os.remove(audioPath)
            logging.info(f"audio .mp3 deletado com sucesso")
        except Exception as e:
            logging.error(f"Erro ao deletar legenda localmente, erro: {e}")

    def createPrompt(self, messageError: str) -> str:
        prompt = f"""

                Transcreva completamente este áudio para o formato de legenda WEBVTT válido, traduzindo todas as falas para português se necessário.

                Instruções:
                    - Detecte e transcreva todas as falas no áudio, e caso estejam em inglês, deixe as legendas em inglês.
                    - Se o idioma estiver em inglês, o arquivo de lgendas deve estar em inglês também, mantendo o áudio original se estiver em inglês.
                    - Identifique corretamente os tempos de início e fim de cada trecho falado, no formato: HH:MM:SS.mmm --> HH:MM:SS.mmm.
                    - A legenda deve começar com a linha: WEBVTT.
                    - Entre cada bloco de legenda, deve haver uma linha em branco.
                    - Cada bloco deve conter apenas o timestamp e a transcrição (em português).
                    - Não inclua cabeçalhos extras, comentários, explicações ou qualquer texto fora do padrão WEBVTT.
                    - Nos timestamps, os milissegundos devem ser sempre precedidos por um ponto (`.`) e não por dois pontos (`:`), no formato: HH:MM:SS.mmm.
                        Exemplo válido: 00:01:23.456
                        Exemplo inválido: 00:01:23:456
                    - Revise todos os timestamps e garanta que todos os milissegundos usem ponto (.) no lugar de dois-pontos (:).

                O conteúdo gerado deve ser apenas o arquivo .vtt completo e válido, contendo apenas a transcrição em português.

                Exemplo mínimo do formato esperado:

                WEBVTT

                00:00:00.000 --> 00:00:04.000
                Primeira frase falada no áudio.

                00:00:04.500 --> 00:00:08.000
                Segunda frase falada no áudio.

                Agora, transcreva o áudio enviado para um arquivo .vtt, seguindo exatamente essas regras.
                Observação: Se não for possível traduzir, retorne a seguinte mensagem: {messageError}
            """
        return prompt

    
    def correctTimesTamp(self, vtt_text: str) -> str:
        return re.sub(r':(\d{3})', r'.\1', vtt_text)
    
    def isFileSizeAllowed(self,filePath:str) -> bool:
        oneMegaByte = 1048576
        try:
            logging.info(f"Obtendo tamanho do arquivo em bytes")
            size = os.path.getsize(filePath)
            logging.info(f"tamanho do arquivo {filePath} em bytes: {size}")
            logging.info(f"arquivo permitido {size/oneMegaByte < 30}")
            return size/oneMegaByte < 30
        except Exception as e:
            logging.error(f"Ocorreu um erro ao obter tamanho do arquivo: {e}")
            return False