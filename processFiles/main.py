import time
from src.db.connectionDb import ConnectionDB
from src.processing.processFile import ProcessFiles
from src.queue.consumeDatas import ConsumeQueue
from src.repository.streamRepository import StreamRepository
import logging
from datetime import date
import os

def configureFileLog():
    dateActual = date.today()
    foundFile = False
    print("configurando log")
    for root, _, files in os.walk("./logs"):
        for file in files:
            if str(file).endswith(".log"):
                if os.path.splitext(str(file))[0] == str(dateActual):
                    foundFile = True

    if not foundFile:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            filename=f"./logs/{dateActual}.log",
            filemode="a",
        )

configureFileLog()

while True:
    try:
        
        db = ConnectionDB()
        streamRepository = StreamRepository(db)
        processFiles = ProcessFiles(streamRepository)
        consumeQueue = ConsumeQueue(processFiles,streamRepository)

        print("[INFO] Iniciando consumidor da fila...")
        consumeQueue.consumeMessageQueue()
    
    except Exception as e:
        print(f"[ERRO] A aplicação falhou com erro: {e}")
        print("[INFO] Reiniciando em 5 segundos...")
        time.sleep(5)


