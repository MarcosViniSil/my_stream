import os
import json
from dotenv import load_dotenv
import boto3
from botocore.client import Config
import subprocess
import shutil
import logging
from datetime import date

from src.email.sendEmail import sendEmail
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

    def getMessageFromQueue(self, message: str) -> None:
        self.configureFileLog()
        message = message.replace("'", '"')
        try:
            data = json.loads(message)
            videoId = str(data["videoId"])
            bucketName = str(data["videoUrl"]).split("/")[-2]
            fileName = str(data["videoUrl"]).split("/")[-1]

            if videoId == None or bucketName == None or fileName == None:
                raise ValueError("Processamento falhou, tente novamente")

            self.processFile(videoId,bucketName,fileName)
            
            self.deleteLocalVideoAfterProcessing(fileName)

            self.deleteFileFromBucket(fileName,bucketName)

        except BaseException as r:
            try:
                if videoId != None:
                    userEmail = self.streamRepository.getOwnerEmail(videoId)
                    self.streamRepository.updateStatusVideoToFail(videoId);
                    #sendEmail(videoId,"Falhou ❌",str(r.args[0]),userEmail)
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
        
        streamFolderName = self.convertVideoToStream(fileName, pathDownload)
        self.sendStreamToBucket(streamFolderName, bucketName, videoId)
        
        pathStreamLocally = f"http://localhost:9000/{bucketName}/{videoId}/output.m3u8"
        self.updateUrlVideoOnDb(pathStreamLocally,videoId)
        
        #self.sendEmailUser(videoId)

    def updateUrlVideoOnDb(self,pathStreamLocally:str,videoId:str) -> None:
        logging.info(f"atualizando url no banco de dados do video de id {videoId}")
        try:
            self.streamRepository.updateUrlVideo(pathStreamLocally,videoId)
        except Exception as r:
            logging.error(f"Ocorreu um erro ao atualizar url do video de id {videoId}. Detalhes:",r)
            raise ValueError("Erro ao atualizar video na base de dados, tente novamente")
        
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
        
        cmd = ["ffmpeg","-i",pathDownload,"-vf","scale=854:480",
                "-c:v","libx264","-b:v","1000k","-c:a","aac",
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
            raise ValueError("Ocorreu um erro ao salvar o vídeo em nuvem, tente novamente")

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

    def configureFileLog(self):
        dateActual = date.today()
        foundFile = False

        for root, _, files in os.walk("./logs"):
            for file in files:
                if str(file).endswith(".log"):
                    if(os.path.splitext(str(file))[0] == dateActual):
                        foundFile = True

        if not foundFile:
            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s - %(levelname)s - %(message)s",
                filename=f"./logs/{dateActual}.log",
                filemode="a",
            )
