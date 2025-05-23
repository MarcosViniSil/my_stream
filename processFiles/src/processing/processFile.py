import os
import json
from dotenv import load_dotenv
import boto3
from botocore.client import Config

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
            self.videoId = data["videoId"]
            bucketName = str(data["videoUrl"]).split("/")[-2]
            fileName = str(data["videoUrl"]).split("/")[-1]
            
            self.downloadFileFromBucket(bucketName,fileName)

        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar a mensagem: {e}")

    def downloadFileFromBucket(self,bucketName:str,fileName: str) -> None:
        if fileName == "" or bucketName == "":
            print("Arquivo ou bucket inválido.")
            return

        try:
            s3 = self.createConnection()
            local_path = os.path.join(LOCAL_PATH, fileName)
            print("bucketName ",bucketName)
            print("fileName ",fileName)
            s3.download_file(bucketName, fileName, local_path)
            
            print(f"Arquivo '{fileName}' baixado para '{local_path}'.")

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
