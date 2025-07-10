from pydantic import BaseModel

class User(BaseModel):
    name: str
    email:str
    password:str


class Userlogin(BaseModel):
    email:str
    password:str

class UserDatas(BaseModel):
    userId:str
    userName:str
    userEmail:str