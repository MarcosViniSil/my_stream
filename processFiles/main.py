from src.processing.processFile import ProcessFiles
from src.queue.consumeDatas import ConsumeQueue

processFiles = ProcessFiles()
consumeQueue = ConsumeQueue(processFiles)
consumeQueue.consumeMessageQueue()