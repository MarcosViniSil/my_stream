from minio import Minio
from dotenv import load_dotenv
from minio.error import S3Error
import os
import json

load_dotenv()

LOCAL_PATH = "./file"

os.makedirs(os.path.dirname(LOCAL_PATH), exist_ok=True)

class ProcessFiles:

    def __init__(self):
        self.videoId = None
        self.bucketName = None
        self.fileName = None
    
    def getMessageFromQueue(self,message: str) -> None:
        message = message.replace("'", '"')
        try:
            data = json.loads(message)
            self.videoId = data["videoId"]
            self.bucketName = str(data["videoUrl"]).split("/")[-2]
            self.fileName = str(data["videoUrl"]).split("/")[-1]
            self.downloadFileFromBucket()

        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar a mensagem: {e}")

    def downloadFileFromBucket(self) -> None:
        try:
            if self.fileName == None or self.bucketName == None:
                return
            
            client = self.createConnection()
            client.fget_object(self.bucketName, self.fileName, f"{LOCAL_PATH}/{self.fileName}")

            print(f"Arquivo '{self.fileName}' baixado para '{LOCAL_PATH}'.")

        except S3Error as e:
            print(f"Erro ao baixar o arquivo: {e}")

    def createConnection(self) -> Minio:
        try:
            client = Minio("localhost:9000",
                access_key= os.environ["ACCESS_KEY_AWS"],
                secret_key= os.environ["SECRET_KEY_AWS"],
                secure=False
            )
        except Exception as e:
            raise ValueError("Erro ao se conectar com o servidor, tente novamente")
        return client