from pydantic import BaseModel

class VideoResponse(BaseModel):
    message: str
    videoId: str