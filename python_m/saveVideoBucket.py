from minio import Minio
from dotenv import load_dotenv
load_dotenv()
import os
import secrets

BUCKET_NAME = os.environ["BUCKET_NAME"] 

def saveVideoOnBucket(pathFile):

    if pathFile == "":
        raise ValueError("Arquivo não informado")

    client = createConnection()

    source_file = pathFile

    destination_file = generateHashForFileName(pathFile)

    createBucketIfNotExists(client,BUCKET_NAME)

    sendFileToBucket(client,BUCKET_NAME,destination_file,source_file)

    return f"http://localhost:9001/browser/{BUCKET_NAME}/{destination_file}"


def createConnection():
    try:
        client = Minio("localhost:9000",
            access_key= os.environ["ACCESS_KEY_AWS"],
            secret_key= os.environ["SECRET_KEY_AWS"],
            secure=False
        )
    except Exception as e:
        raise ValueError("Erro ao se conectar com o servidor, tente novamente")
    return client


def createBucketIfNotExists(client,bucket_name):
    found = client.bucket_exists(bucket_name)
    if not found:
        try:
            client.make_bucket(bucket_name)
        except Exception as e:
            raise ValueError("Erro ao criar o bucket, tente novamente")


def sendFileToBucket(client,bucket_name,destination_file,source_file):
    try:
        client.fput_object(
            bucket_name, destination_file, source_file,
        )
    except Exception as e:
        raise ValueError("Erro ao enviar o arquivo para o bucket, tente novamente")

def generateHashForFileName(file_path):
    ext = os.path.splitext(file_path)[1]
    return f"{secrets.token_urlsafe(5)}{ext}"


