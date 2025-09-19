from fastapi import FastAPI
from src.controller.receiveVideoController import router
from src.controller.listUserVideos import routerUserVideos
from src.controller.userController import userRouter
from src.controller.receiveMetadata import routerM
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import re

app = FastAPI()

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "working"}


app.include_router(router)
app.include_router(routerM)
app.include_router(routerUserVideos)
app.include_router(userRouter)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
