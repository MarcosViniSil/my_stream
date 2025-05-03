from fastapi import APIRouter, File, UploadFile, Depends,Form
from src.models.dependencies import getReceiveMetaData

from src.models.metadataResponse import MetadataResponse
from uuid import UUID
from src.service.receiveMetaData import ReceiveMetadaService

routerM = APIRouter()

@routerM.post("/upload/metadata")
async def upload_metadata(
    id: UUID = Form(...),
    videoTitle: str = Form(...),
    thumbnailImage: UploadFile = File(...),
    reciveMetadata: ReceiveMetadaService = Depends(getReceiveMetaData)
):
    return await reciveMetadata.processMetaData(id,videoTitle,thumbnailImage)
