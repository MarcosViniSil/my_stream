from datetime import datetime, timedelta
import jwt
from dotenv import load_dotenv
load_dotenv()
import os

def createJwtToken(email:str) -> str:
    if email is None:
        raise ValueError("Email não informado, portanto não é possível gerar token")
    
    SECRET_KEY = os.environ["KEY_JWT"] 
    if SECRET_KEY is None:
        raise ValueError("Não foi possível capturar chave para gerar o token")
    
    payload = createPayLoad(email)

    algorithm = 'HS256'
    try:
        token = jwt.encode(payload, SECRET_KEY, algorithm=algorithm)
        return token
    except Exception as e:
        raise ValueError(f"Ocorreu um erro ao gerar token jwt, erro: {e} [DEV]")

def validateJwtToken(token: str) -> dict:
    if token is None:
        raise ValueError("Token não foi informado")
    
    SECRET_KEY = os.environ["KEY_JWT"] 
    if SECRET_KEY is None:
        raise ValueError("Não foi possível capturar chave para gerar o token")
    
    algorithm = 'HS256'
    try:
        response = jwt.decode(token, SECRET_KEY, algorithms=[algorithm])
        return response
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expirado, realize o login novamente")
    except jwt.InvalidTokenError:
        raise ValueError("Token inválido, realize o login para gerar um token correto")

def createPayLoad(email:str) -> dict:
    payload = {
        'userEmail': email,
        'exp': datetime.now() + timedelta(hours=24) 
    }

    return payload
