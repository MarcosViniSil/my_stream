import os
import uuid
import boto3
from dotenv import load_dotenv
from botocore.exceptions import ClientError
from botocore.client import Config
from urllib.parse import urlparse
from urllib.parse import urlparse
load_dotenv()

class Bucket:

    def __init__(self):
        self.BUCKET_NAME = os.environ["BUCKET_NAME"]
        self.MINIO_INTERNAL_ENDPOINT = os.getenv("MINIO_INTERNAL_ENDPOINT", "minio")
        self.MINIO_PUBLIC_ENDPOINT = os.getenv("MINIO_PUBLIC_ENDPOINT", "localhost")

    def saveFileOnBucket(self, pathFile: str) -> str:
        if not pathFile:
            raise ValueError("Arquivo não informado")

        client = self.createConnection()

        source_file = pathFile
        destination_file = self.generateHashForFileName(pathFile)

        self.createBucketIfNotExists(client, self.BUCKET_NAME)
        self.sendFileToBucket(client, self.BUCKET_NAME, destination_file, source_file)

        return f"http://localhost:9000/{self.BUCKET_NAME}/{destination_file}"

    def deleteFileOnBucket(self, fileCode: str) -> None:
        if not fileCode:
            raise ValueError("Arquivo não informado")

        client = self.createConnection()
        self.removeFileFromBucket(client, self.BUCKET_NAME, fileCode)

    def deleteFolderOnBucket(self,folderName:str) -> None:
        if not folderName:
            raise ValueError("Pasta não informada")
        client = self.createConnection()
        self.removeFolderFromBucket(client,self.BUCKET_NAME,folderName)
    

    def generatePresignedUrl(self, full_url, expiration=900):

        internal_url = full_url.replace(self.MINIO_PUBLIC_ENDPOINT, self.MINIO_INTERNAL_ENDPOINT)

        parsed = urlparse(internal_url)
        path = parsed.path.lstrip('/')
        bucket_name = path.split('/')[0]
        object_key = '/'.join(path.split('/')[1:])
        print(f"[INFO] bucket: {bucket_name}, key: {object_key}")

        client = self.createConnection()

        try:
            client.head_object(Bucket=bucket_name, Key=object_key)
        except client.exceptions.NoSuchKey:
            raise Exception("Objeto não encontrado no bucket")

        # gera presigned URL com endpoint interno
        presigned_url = client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_key},
            ExpiresIn=expiration
        )

        public_url = presigned_url.replace(self.MINIO_INTERNAL_ENDPOINT, self.MINIO_PUBLIC_ENDPOINT)

        return public_url

    
    def createConnection(self):
        try:
            client = boto3.client(
            "s3",
            endpoint_url=f'http://localhost:9000',
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
    
    def removeFolderFromBucket(self, client, bucket_name: str, prefix: str):
        try:
            response = client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
            if 'Contents' in response:
                objects_to_delete = [{'Key': obj['Key']} for obj in response['Contents']]
                client.delete_objects(
                    Bucket=bucket_name,
                    Delete={'Objects': objects_to_delete}
                )
        except ClientError as e:
            raise ValueError("Erro ao remover a pasta: " + str(e))
    
