from minio import Minio
from dotenv import load_dotenv
load_dotenv()
import os
import secrets


class Bucket:

    def __init__(self):
        self.BUCKET_NAME = os.environ["BUCKET_NAME"] 

    def saveFileOnBucket(self, pathFile: str) -> str:

        if pathFile == "":
            raise ValueError("Arquivo não informado")

        client = self.createConnection()

        source_file = pathFile

        destination_file = self.generateHashForFileName(pathFile)

        self.createBucketIfNotExists(client,self.BUCKET_NAME)

        self.sendFileToBucket(client,self.BUCKET_NAME,destination_file,source_file)

        return f"http://localhost:9001/browser/{self.BUCKET_NAME}/{destination_file}"
    

    def deleteFileOnBucket(self,fileCode: str) -> None:
        if fileCode == "":
            raise ValueError("Arquivo não informado")

        client = self.createConnection()

        destination_file = fileCode

        self.removeFileFromBucket(client,self.BUCKET_NAME,destination_file)

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


    def createBucketIfNotExists(self,client: Minio,bucket_name: str):
        found = client.bucket_exists(bucket_name)
        if not found:
            try:
                client.make_bucket(bucket_name)
            except Exception as e:
                raise ValueError("Erro ao criar o bucket, tente novamente")


    def sendFileToBucket(self,client: Minio,bucket_name: str,destination_file: str,source_file: str):
        try:
            client.fput_object(
                bucket_name, destination_file, source_file,
            )
        except Exception as e:
            raise ValueError("Erro ao enviar o arquivo para o bucket, tente novamente")

    def generateHashForFileName(self,file_path: str):
        ext = os.path.splitext(file_path)[1]
        return f"{secrets.token_urlsafe(5)}{ext}"

    def removeFileFromBucket(self,client: Minio,bucket_name: str,destination_file: str):
        try:
            client.remove_object(bucket_name, destination_file)
        except Exception as e:
            raise ValueError("Erro ao remover o arquivo do bucket, tente novamente")

