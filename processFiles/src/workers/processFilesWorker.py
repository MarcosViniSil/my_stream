from src.processing.processFile import ProcessFiles
from src.repository.streamRepository import StreamRepository
import logging

class ProcessFilesWorker:

    def __init__(self,process: ProcessFiles,streamRepository:StreamRepository):
        self.process = process
        self.streamRepository = streamRepository

    
    def processTask(self,taskId:str,videoId:str,bucket:str,fileName:str):
        print(f"[WORKER] Processando tarefa #{taskId} — vídeo {videoId}")
        self.streamRepository.changeStatus(taskId, 'PROCESSING')

        try:
            self.process.getMessageFromQueue(videoId=videoId,bucketName=bucket,fileName=fileName)

            self.streamRepository.changeStatus(taskId, 'READY')
            print(f"[WORKER] Tarefa #{taskId} concluída.")
        except Exception as e:
            print(f"[WORKER] Erro na tarefa #{taskId}: {e}")
            self.streamRepository.changeStatus(taskId, 'FAIL')

