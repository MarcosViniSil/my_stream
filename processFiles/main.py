import time
from src.db.connectionDb import ConnectionDB
from src.processing.processFile import ProcessFiles
from src.processing.subtitles import Subtitles
from src.queue.consumeDatas import ConsumeQueue
from src.repository.streamRepository import StreamRepository
import logging
from datetime import date
import os


while True:
    try:
        
        db = ConnectionDB()
        streamRepository = StreamRepository(db)
        subtitles = Subtitles()
        processFiles = ProcessFiles(streamRepository,subtitles)
        consumeQueue = ConsumeQueue(processFiles)

        print("[INFO] Iniciando consumidor da fila...")
        consumeQueue.consumeMessageQueue()
    
    except Exception as e:
        print(f"[ERRO] A aplicação falhou com erro: {e}")
        print("[INFO] Reiniciando em 5 segundos...")
        time.sleep(5)


