from pydantic import BaseModel

class MetadataResponse(BaseModel):
    message: str