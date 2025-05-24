from enum import Enum

class VideoStatus(Enum):
    READY = 'READY'
    PROCESSING = 'PROCESSING'
    FAIL = 'FAIL'