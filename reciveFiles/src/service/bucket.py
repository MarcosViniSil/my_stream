import os
import uuid
import boto3
from dotenv import load_dotenv
from botocore.exceptions import ClientError
from botocore.client import Config

load_dotenv()

class Bucket:

    def __init__(self):
        self.BUCKET_NAME = os.environ["BUCKET_NAME"]

    def saveFileOnBucket(self, pathFile: str) -> str:
        if not pathFile:
            raise ValueError("Arquivo não informado")

        client = self.createConnection()

        source_file = pathFile
        destination_file = self.generateHashForFileName(pathFile)

        self.createBucketIfNotExists(client, self.BUCKET_NAME)
        self.sendFileToBucket(client, self.BUCKET_NAME, destination_file, source_file)

        return f"http://{self.BUCKET_NAME}/{destination_file}"

    def deleteFileOnBucket(self, fileCode: str) -> None:
        if not fileCode:
            raise ValueError("Arquivo não informado")

        client = self.createConnection()
        self.removeFileFromBucket(client, self.BUCKET_NAME, fileCode)

    def createConnection(self):
        try:
            client = boto3.client(
            "s3",
            endpoint_url='http://localhost:9000',
            aws_access_key_id=os.environ["ACCESS_KEY_AWS"],
            aws_secret_access_key=os.environ["SECRET_KEY_AWS"],
            aws_session_token=None,
            config=boto3.session.Config(signature_version='s3v4'),
            verify=False
            )
            return client
        except Exception as e:
            raise ValueError("Erro ao se conectar com o servidor: " + str(e))

    def createBucketIfNotExists(self, client, bucket_name: str):
        try:
            existing_buckets = client.list_buckets()
            if not any(b['Name'] == bucket_name for b in existing_buckets['Buckets']):
                client.create_bucket(Bucket=bucket_name)
        except ClientError as e:
            raise ValueError("Erro ao criar/verificar bucket: " + str(e))

    def sendFileToBucket(self, client, bucket_name: str, destination_file: str, source_file: str):
        try:
            client.upload_file(source_file, bucket_name, destination_file)
        except ClientError as e:
            raise ValueError("Erro ao enviar o arquivo: " + str(e))

    def generateHashForFileName(self, file_path: str) -> str:
        hashFile = uuid.uuid4()
        ext = os.path.splitext(file_path)[1]
        return f"{hashFile}{ext}"

    def removeFileFromBucket(self, client, bucket_name: str, destination_file: str):
        try:
            client.delete_object(Bucket=bucket_name, Key=destination_file)
        except ClientError as e:
            raise ValueError("Erro ao remover o arquivo: " + str(e))
