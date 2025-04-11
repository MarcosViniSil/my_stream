import os
import shutil

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from saveVideoBucket import createConnection, createBucketIfNotExists, sendFileToBucket, genrateHashForFileName, saveVideoOnBucket

app = FastAPI()

UPLOAD_DIR = "uploads"
PATH_DELETE_FILE = ""

os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_video(file: UploadFile = File(...)):
    if not file.filename.endswith(".mp4"):
        return JSONResponse(status_code=400, content={"error": "Apenas arquivos .mp4 são permitidos."})
    
    hashVideo = ""
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    PATH_DELETE_FILE = file_path

    try:
        hashVideo = saveVideoOnBucket(file_path)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"Erro ao salvar o vídeo: {str(e)}"})

    if hashVideo != "":
        os.remove(PATH_DELETE_FILE)
        #TODO Logic save hash video on data base
    else:
        return JSONResponse(status_code=500, content={"error": "Erro ao salvar o vídeo."})

    return {"message": "Vídeo recebido com sucesso!", "filename": file.filename}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("reciveVideo:app", host="127.0.0.1", port=8000, reload=True)
