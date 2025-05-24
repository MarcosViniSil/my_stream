import os
import json
from dotenv import load_dotenv
import boto3
from botocore.client import Config
import subprocess
import shutil
import logging
from datetime import date

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
            print(data)
            videoId = str(data["videoId"])
            bucketName = str(data["videoUrl"]).split("/")[-2]
            fileName = str(data["videoUrl"]).split("/")[-1]

            pathDownload = self.downloadFileFromBucket(bucketName, fileName)
            streamFolderName = self.convertVideoToStream(fileName, pathDownload)

            self.sendStreamToBucket(streamFolderName, bucketName, videoId)

            urlStream = f"http://localhost:9000/{bucketName}/{videoId}/output.m3u8"
            print(urlStream)
            self.streamRepository.updateUrlVideo(urlStream,videoId)

        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar a mensagem: {e.msg}")
        except ValueError as v:
            print(f"Erro: {e.msg}")
        except Exception as r:
            print(f"Erro: {r}")

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
            logging.error(resultado.stderr)
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

        s3 = self.createConnection()
        local_path = os.path.join(LOCAL_PATH, fileName)
        s3.download_file(bucketName, fileName, local_path)
        return local_path

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
