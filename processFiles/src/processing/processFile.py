import os
import json
from dotenv import load_dotenv
import boto3
from botocore.client import Config
import subprocess
import shutil

load_dotenv()

LOCAL_PATH = "./file"
os.makedirs(LOCAL_PATH, exist_ok=True)

class ProcessFiles:

    def __init__(self):
        self.videoId = None
        self.bucketName = None
        self.fileName = None

    def getMessageFromQueue(self, message: str) -> None:
        message = message.replace("'", '"')
        try:
            data = json.loads(message)
            videoId = str(data["videoId"])
            bucketName = str(data["videoUrl"]).split("/")[-2]
            fileName = str(data["videoUrl"]).split("/")[-1]
            
            pathDownload = self.downloadFileFromBucket(bucketName,fileName)
            streamFolderName = self.convertVideoToStream(fileName,pathDownload)

            self.sendStreamToBucket(streamFolderName,bucketName,videoId)

        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar a mensagem: {e}")



    def convertVideoToStream(self,nameFile:str,pathDownload:str) -> str:
        nameFolder = nameFile
        if nameFile.endswith(".mp4"):
            nameFolder = os.path.splitext(nameFile)[0]
        
        os.makedirs(f"./{nameFolder}", exist_ok=True)
        #ffmpeg -i input.mp4 -codec: copy -start_number 0 -hls_time 10 -hls_list_size 0 -f hls caminho/para/pasta/output.m3u8
        resultado = subprocess.run(["ffmpeg", "-i",f"{pathDownload}","-codec:","copy",
                                    "-start_number","0","-hls_time","10",
                                    "-hls_list_size","0","-f","hls",f"./{nameFolder}/output.m3u8"], 
                                   capture_output=True, text=True)
        
        #shutil.rmtree(f"./{nameFolder}")

        return nameFolder
        #print(resultado.stdout)
        #print(resultado.stderr)

    def sendStreamToBucket(self,folder_path:str,bucket_name:str,videoId: str):
        try:
            s3 = self.createConnection()
            for root, _, files in os.walk(folder_path):
               for file in files:
                   local_path = os.path.join(root, file)
                   relative_path = os.path.relpath(local_path, folder_path).replace("\\", "/")

                   s3_key = f"{videoId}/{relative_path}" 

                   s3.upload_file(local_path, bucket_name, s3_key)
                   
                   print(f"Enviado: {local_path} → {bucket_name}/{s3_key}")
        except Exception as e:
            print(e)        

    def downloadFileFromBucket(self,bucketName:str,fileName: str) -> str:
        if fileName == "" or bucketName == "":
            print("Arquivo ou bucket inválido.")
            return

        try:
            s3 = self.createConnection()
            local_path = os.path.join(LOCAL_PATH, fileName)
            s3.download_file(bucketName, fileName, local_path)
            return local_path

        except Exception as e:
            print(f"Erro ao baixar o arquivo: {e}")


    def createConnection(self):
        try:
            s3 = boto3.client(
            "s3",
            endpoint_url='http://localhost:9000',
            aws_access_key_id=os.environ["ACCESS_KEY_AWS"],
            aws_secret_access_key=os.environ["SECRET_KEY_AWS"],
            aws_session_token=None,
            config=boto3.session.Config(signature_version='s3v4'),
            verify=False
            )
            return s3
        except Exception as e:
            raise ValueError("Erro ao se conectar com o S3: " + str(e))
