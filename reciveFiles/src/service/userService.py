from src.models.user import User,Userlogin
from src.repository.userRepository import UserRepository
from fastapi import HTTPException
from src.security.hash.hashService import createHashForPassword,isPasswordEqualDB
from src.security.jwt.jwtService import createJwtToken,validateJwtToken
import re

class UserService:

    def __init__(self,userRepository:UserRepository):
        self.userRepository = userRepository

    def createUser(self,user:User) -> None:
        
        self.isUserValid(user)

        try:
            passwordHash = createHashForPassword(user.password)
            user.password = passwordHash
        except Exception as e:
            raise HTTPException(status_code=400,detail="Ocorreu um erro ao validar senha, tente novamente")

        try:
            self.userRepository.createUser(user)
        except Exception as e:
            raise HTTPException(status_code=400,detail=f"{e}")
        
        return {"message":"cadastrado com sucesso"}

    def logInUser(self,user:Userlogin) -> str:
        
        self.validateEmail(user.email)
        self.validatePassword(user.password)  
        
        row = None
        
        try:
            row = self.userRepository.getHashedPassword(user.email)
        except Exception as e:
            raise HTTPException(status_code=400,detail="Ocorreu um erro ao verificar dados")
        
        if row is None or row[0] is None:
            raise HTTPException(status_code=400,detail="O usuário informado não foi encontrado")
        
        hashedPassword = row[0].encode("utf-8")
        isPasswordValid = False

        try:
            isPasswordValid = isPasswordEqualDB(hashedPassword,user.password)
        except Exception as e:
            raise HTTPException(status_code=400,detail=f"Ocorreu um erro ao verificar senha, tente novamente{e}")
            
        if not isPasswordValid:
            raise HTTPException(status_code=400,detail="Email ou senha inválidos")
        
        try:
            token = createJwtToken(user.email)
            return {"token":token}
        
        except Exception as e:
            raise HTTPException(status_code=400,detail=f"Não foi possível realizar o login, tente novamente{e}")

    
    def isUserValid(self,user:User) -> None:
        if user is None:
            raise HTTPException(status_code=400,detail="Offset deve ser maior que 0")

        self.validateName(user.name)

        self.validateEmail(user.email)

        self.validatePassword(user.password)

    def getUserId(self,token:str) -> bytes:
        datas = None
        
        try:
            datas = validateJwtToken(token)
        except Exception as e:
                raise ValueError("token inválido")
        
        if datas is None or datas.email is None:
            raise ValueError("erro ao validar token")
        userEmail = datas.email
        
        try:
            row = self.userRepository.getUserId(userEmail)
            if row is None or row[0] is None:
                raise ValueError("erro ao consultar banco para validar usuário, dados nulos")
            return row[0]
        except Exception as e:
            raise ValueError("Ocoreru um erro ao acessar banco de dados para obter token do usuário")

    def validateName(self,name:str) -> None:
        if not name.strip():
            raise HTTPException(status_code=400,detail="Nome não pode conter apenas espaços")

        if len(name) < 3 or len(name) > 40:
            raise HTTPException(status_code=400,detail="Nome deve conter no mínimo 3 e no máximo 40 caracteres")
    
    def validateEmail(self,email:str) -> None:
        regexEmail = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$' # regex to validate email, source: https://www.geeksforgeeks.org/python/input-validation-in-python-string/

        if not re.match(regexEmail,email):
            raise HTTPException(status_code=400,detail="Email inválido")
    
    def validatePassword(self,password:str) -> None:
        if not password.strip():
            raise HTTPException(status_code=400,detail="Senha não pode conter apenas espaços")
        
        if len(password) < 8 or len(password) > 30:
            raise HTTPException(status_code=400,detail="Senha deve conter no mínimo 8 e no máximo 30 caracteres")