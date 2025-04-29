
from src.service.bucket import Bucket
import os

class ReciveVideo:

    def __init__(self,bucket: Bucket):
        self.bucket = bucket


    def saveVideo(self,file_path: str) -> str:
        try:
            hashVideo = self.saveVideoOnBucket(file_path)
            return hashVideo
        except Exception as e:
            return ""
    
    def removeLocalVideo(self,hashVideoBucket: str,file_path: str) -> None:
        if hashVideoBucket != "":
            os.remove(file_path)
        else:
            raise ValueError("Ocorreu um erro, video não foi salvo na nuvem, tente novamente")