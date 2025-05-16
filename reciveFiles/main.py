from fastapi import FastAPI
from src.controller.receiveVideoController import router
from src.controller.receiveMetadata import routerM
import uvicorn

app = FastAPI()
app.include_router(router)
app.include_router(routerM)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)