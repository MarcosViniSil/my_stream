import os
import json
from dotenv import load_dotenv
import boto3
from botocore.client import Config
import subprocess
import shutil
import logging

from src.email.sendEmail import sendEmail
from src.exception.videoBucketException import VideoBucketException
from src.repository.streamRepository import StreamRepository

load_dotenv()

LOCAL_PATH = "./file"
os.makedirs(LOCAL_PATH, exist_ok=True)
os.makedirs("./logs", exist_ok=True)

class ProcessFiles:

    def __init__(self, streamRepository:StreamRepository):
        self.videoId = None
        self.bucketName = None
        self.fileName = None
        self.streamRepository = streamRepository

    def getMessageFromQueue(self, videoId: str,bucketName:str,fileName:str) -> None:
        try:
            if videoId == None or bucketName == None or fileName == None:
                raise ValueError("Processamento falhou, tente novamente")

            self.processFile(videoId,bucketName,fileName)
            
            self.deleteLocalVideoAfterProcessing(fileName)

            self.deleteFileFromBucket(fileName,bucketName)

        except VideoBucketException as vb:
            self.handleException(videoId,fileName)
            try:
                self.deleteFileFromBucket(fileName,bucketName)
            except BaseException as r:
                logging.error(f"Ocorreu o erro {vb} e ao tentar deletar video de id {videoId} do bucket {bucketName} ocorreu o erro {r}")
        
        except BaseException as r:
            logging.error(f"Ocorreu o erro {r} ")
            self.handleException(videoId,fileName)

    def handleException(self,videoId : str,fileName : str) -> None:
        try:
            if videoId != None:
                userEmail = self.streamRepository.getOwnerEmail(videoId)
                self.streamRepository.updateStatusVideoToFail(videoId);
                #sendEmail(videoId,"Falhou ❌",str(r.args[0]),userEmail)
                self.deleteLocalVideoAfterProcessing(fileName)
        except Exception as r:
                logging.error(f"Erro ao avisar usuário de email {userEmail} sobre falha no processamento do video de id {videoId}",r)
                self.deleteLocalVideoAfterProcessing(fileName)

    def deleteLocalVideoAfterProcessing(self,nameFile:str) -> None:
        try:
            pathD = ""
            if nameFile.endswith(".mp4"):
                pathD = os.path.splitext(nameFile)[0]
            shutil.rmtree(f"./{pathD}")
            os.remove(f"./file/{nameFile}")
        except BaseException as r:
            logging.error(f"Erro ao deletar vídeo de nome {nameFile} localmente",r)

    def processFile(self,videoId:str,bucketName:str,fileName:str) -> None:
        pathDownload = self.downloadFileFromBucket(bucketName, fileName)
        
        self.validateVideo(pathDownload)
        
        streamFolderName = self.convertVideoToStream(fileName, pathDownload)
        self.sendStreamToBucket(streamFolderName, bucketName, videoId)
        
        self.validateGeneratedStream(streamFolderName)

        pathStreamLocally = f"http://localhost:9000/{bucketName}/{videoId}/output.m3u8"
        self.updateUrlVideoOnDb(pathStreamLocally,videoId)
        
        #self.sendEmailUser(videoId)

    def updateUrlVideoOnDb(self,pathStreamLocally:str,videoId:str) -> None:
        logging.info(f"atualizando url no banco de dados do video de id {videoId}")
        try:
            self.streamRepository.updateUrlVideo(pathStreamLocally,videoId)
        except Exception as r:
            logging.error(f"Ocorreu um erro ao atualizar url do video de id {videoId}. Detalhes:",r)
            raise VideoBucketException("Erro ao atualizar video na base de dados, tente novamente")
        
        logging.info(f"url do video de id {videoId} atualizada com sucesso")

    def sendEmailUser(self,videoId:str) -> None:
        userEmail = self.streamRepository.getOwnerEmail(videoId)
        logging.info(f"Enviando email sobre video de id {videoId} para {userEmail}")

        sendEmail(videoId,"Disponível ✅","Vídeo recebido com sucesso",userEmail)

        logging.info(f"Email enviado para email {userEmail}")
    

    def convertVideoToStream(self, nameFile: str, pathDownload: str) -> str:
        nameFolder = nameFile
        if nameFile.endswith(".mp4"):
            nameFolder = os.path.splitext(nameFile)[0]

        os.makedirs(f"./{nameFolder}", exist_ok=True)
        outputPath = f"./{nameFolder}/output.m3u8"
        
        cmd = ["ffmpeg","-i",pathDownload,"-vf","scale=1280:720",
                "-c:v","libx264","-b:v","3000k","-c:a","aac",
                "-b:a","96k","-hls_time","10","-hls_list_size","0","-f","hls",outputPath,]
        
        logging.info(f"Iniciando conversão de {pathDownload} para 480p.")

        resultado = subprocess.run(cmd, capture_output=True, text=True)

        # shutil.rmtree(f"./{nameFolder}")

        if resultado.returncode != 0:
            logging.error(f"Erro na conversão, erro que ocorreu: {resultado.stderr}")
            raise ValueError("Ocorreu um erro ao converter o vídeo em streaming, tente novamente")
        else:
            logging.info(f"Conversão bem-sucedida. Arquivo HLS: {outputPath}")

        return nameFolder

    def validateVideo(self,filePath):
        
        self.validateVideoDownloaded(filePath=filePath)

        cmd = ["ffmpeg", "-v", "error", "-i", filePath, "-f", "null", "-"]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            logging.error(f"[VALIDAÇÃO] Arquivo inválido: {result.stderr}")
            raise Exception(f"Arquivo inválido: {result.stderr}")
        
        logging.info(f"[VALIDAÇÃO] Arquivo {filePath} válido.")

    def validateGeneratedStream(self,folderPath):
        playlist = os.path.join(folderPath, "output.m3u8")
        
        if not os.path.exists(playlist):
            logging.error(f"Playlist .m3u8 não encontrada em {folderPath}")
            raise Exception(f"Playlist .m3u8 não encontrada em {folderPath}")

        cmd = ["ffmpeg","-v", "error","-i", playlist,"-f", "null","-"]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            logging.error(f"[VALIDAÇÃO STREAMING] Stream inválido. Erros do ffmpeg:\n{result.stderr}")
            raise Exception(f"Stream inválido. Erros do ffmpeg:\n{result.stderr}")
        else:
            logging.info(f"[VALIDAÇÃO STREAMING] Stream em {folderPath} é válido usando ffmpeg.")

    def validateVideoDownloaded(self,filePath):
        if not os.path.exists(filePath):
            logging.error(f"[VALIDAÇÃO] Arquivo não encontrado: {filePath}")
            raise Exception(f"Arquivo não encontrado: {filePath}")
        if os.path.getsize(filePath) == 0:
            logging.error(f"[VALIDAÇÃO] Arquivo vazio: {filePath}")
            raise Exception(f"Arquivo vazio: {filePath}")
        
        logging.info(f"[VALIDAÇÃO] Arquivo correto: {filePath}")
        
    def sendStreamToBucket(self, folder_path: str, bucket_name: str, videoId: str):
        logging.info(f"Iniciando envio de stream de id {videoId} que está na pasta local {folder_path} para o bucket {bucket_name}")
        s3 = self.createConnection()

        try:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    local_path = os.path.join(root, file)
                    relative_path = os.path.relpath(local_path, folder_path).replace("\\", "/")

                    s3_key = f"{videoId}/{relative_path}"

                    s3.upload_file(local_path, bucket_name, s3_key)

            logging.info(f"stream de id {videoId} enviado com sucesso para o bucket {bucket_name}")

        except Exception as e:
            logging.error(f"ocorreu um erro ao enviar o stream de id {videoId} para o bucket {bucket_name}. Erro que ocorreu: {e}")
            raise VideoBucketException("Ocorreu um erro ao salvar o vídeo em nuvem, tente novamente")

    def downloadFileFromBucket(self, bucketName: str, fileName: str) -> str:
        if fileName == "" or bucketName == "":
            raise ValueError("Ocorreu um erro ao processar o vídeo recebido, tente novamente")
        
        logging.info(f"Baixando o arquivo {fileName} do bucket {bucketName}")
        try:
            s3 = self.createConnection()
            local_path = os.path.join(LOCAL_PATH, fileName)
            s3.download_file(bucketName, fileName, local_path)
            logging.info(f"Arquivo {fileName} baixado com sucesso")
            return local_path
        except Exception as e:

            logging.error(f"Ocorreu um erro ao baixar arquivo {fileName} vindo do bucket {bucketName}")
            raise ValueError("Ocorreu um erro ao iniciar o processamento do vídeo, tente novamente")

    def deleteFileFromBucket(self, fileName:str, bucketName:str) -> None:
        try:
            s3 = self.createConnection()
            s3.delete_object(Bucket=bucketName, Key=fileName)
        except BaseException as r:
            logging.error(f"Ocoreru um erro ao deletar arquivo {fileName} do buket {bucketName} após o processamento")

    def createConnection(self):
        try:
            s3 = boto3.client(
                "s3",
                endpoint_url="http://localhost:9000",
                aws_access_key_id=os.environ["ACCESS_KEY_AWS"],
                aws_secret_access_key=os.environ["SECRET_KEY_AWS"],
                aws_session_token=None,
                config=boto3.session.Config(signature_version="s3v4"),
                verify=False,
            )
            return s3
        except Exception as e:
            raise ValueError("Ocorreu um erro interno ao tentar processar o vídeo, tente novamente")

