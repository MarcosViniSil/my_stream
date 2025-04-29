import os
import shutil
from src.service.bucket import Bucket
from src.service.reciveVideo import ReciveVideo
import uvicorn

from fastapi import FastAPI, File, UploadFile,APIRouter
from fastapi.responses import JSONResponse


router = APIRouter()
bucket = Bucket()
reciveVideo = ReciveVideo(bucket)
UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload/")
async def upload_video(file: UploadFile = File(...)):
    if not file.filename.endswith(".mp4"):
        return JSONResponse(status_code=400, content={"error": "Apenas arquivos .mp4 são permitidos."})
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    hashVideo = saveVideo(file_path)

    try:
        reciveVideo.removeLocalVideo(hashVideo,file_path)
    except Exception as e:
        return JSONResponse(status_code=400, content={"erro": f"{str(e)}"})
    
    #TODO Logic save vide hash on data base
    #TODO logic to delete video from bucket if insert on data base fail
    
    return {"message": "Vídeo recebido com sucesso!", "filename": file.filename}

def saveVideo(file_path):
    try:
        hashVideo = reciveVideo.saveVideoOnBucket(file_path)
        return hashVideo
    except Exception as e:
        return ""
    
def removeLocalVideo(hashVideoBucket,file_path):
    if hashVideoBucket != "":
        os.remove(file_path)
    else:
        raise ValueError("Ocorreu um erro, video não foi salvo na nuvem, tente novamente")


if __name__ == "__main__":
    uvicorn.run("reciveVideo:app", host="127.0.0.1", port=8000, reload=True)


