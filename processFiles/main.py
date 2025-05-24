from src.db.connectionDb import ConnectionDB
from src.processing.processFile import ProcessFiles
from src.queue.consumeDatas import ConsumeQueue
from src.repository.streamRepository import StreamRepository

db = ConnectionDB()
streamRepository = StreamRepository(db)
processFiles = ProcessFiles(streamRepository)
consumeQueue = ConsumeQueue(processFiles)
consumeQueue.consumeMessageQueue()