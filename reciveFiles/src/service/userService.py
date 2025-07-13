import ast
import uuid
from src.service.emailService import sendEmail
from src.models.user import UpdatePassword, User, UserDatas,Userlogin
from src.repository.userRepository import UserRepository
from fastapi import HTTPException
from src.security.hash.hashService import createHashForPassword,isPasswordEqualDB
from src.security.jwt.jwtService import createJwtToken,validateJwtToken
from datetime import datetime
import re
import random

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
    
    def updateUserDatas(self,user:UserDatas,token:str) -> None:

        self.validateEmail(user.userEmail)
        self.validateName(user.userName)
        
        userId = None
        try:
            userId = self.getUserId(token)
        except Exception as e:
            raise HTTPException(status_code=400,detail="Ocorreu um erro ao obter id do usuário")
        
        try:
            self.userRepository.updateUserDatas(userId,user.userName,user.userEmail)
        except Exception as e:
            raise HTTPException(status_code=400,detail="Não foi possível atualizar os dados do usuário")
        
        return {"message":"dados atualizados com sucesso"}
        
    def getUserId(self,token:str) -> bytes:
        try:
            token = ast.literal_eval(token)['token']
        except Exception as e:
            raise ValueError("Ocorreu um erro ao obter token")
        datas = None
        
        datas = validateJwtToken(token)

   
        if datas is None or datas["userEmail"] is None:
            raise ValueError("erro ao validar token")
        userEmail = datas["userEmail"]
        
        try:
            row = self.userRepository.getUserId(userEmail)
            if row is None or row[0] is None:
                raise ValueError("erro ao consultar banco para validar usuário, dados nulos")
            return row[0]
        except Exception as e:
            raise ValueError("Ocoreru um erro ao acessar banco de dados para obter token do usuário")

    def sendCodeToUser(self,email:str) -> None:
        self.validateEmail(email)

        userId = None

        try:
            userId = self.userRepository.getUserId(email=email)
        except Exception as e:
            raise HTTPException(status_code=400,detail="Ocorreu um erro ao obter id do usuário")
        
        if userId is None or userId[0] is None:
            raise HTTPException(status_code=400,detail="Email não encontrado")
        
        code = self.generateCode()
        
        try:
            self.userRepository.createCodeUser(userId[0],code)
        except Exception as e:
            raise HTTPException(status_code=400,detail=f"Ocorreu um erro ao registrar o código {e}")
        
        try:
            sendEmail(code,email)
        except Exception as e:
            raise HTTPException(status_code=400,detail="Ocorreu um erro ao enviar codigo para o email")
        
        return {"message":"código enviado com sucesso"}
    
    def validateCode(self,email:str,code:int) -> None:

        try:
            row = self.userRepository.getCodeById(email,code)
        except Exception as e:
            raise HTTPException(status_code=400,detail=f"Ocorreu um erro ao obter o código {e}")
        
        if row is None or row[0] is None or row[1] is None:
            raise HTTPException(status_code=400,detail="O código informado está incorreto")
        
        if int(row[0]) != code:
            raise HTTPException(status_code=400,detail="O código informado está incorreto")
        
        expiresAt = row[1]
        if datetime.now() > expiresAt:
            raise HTTPException(status_code=400,detail="Código expirou")
        
        return {"message":"código correto"}


    def updatePassword(self, datasPassword:UpdatePassword) -> None:

        self.validateEmail(datasPassword.email)

        try:
            self.validateCode(datasPassword.email,datasPassword.code)
        except Exception as e:
            raise HTTPException(status_code=400,detail="O código informado não é valido, solicite outro para alterar a senha")

        try:
            passwordHash = createHashForPassword(datasPassword.password)
            self.userRepository.updateUserPassword(datasPassword.email,passwordHash)
        except Exception as e:
            raise HTTPException(status_code=400,detail=f"Ocorreu um erro ao atualizar senha, tente novamente {e}")

        return {"message":"senha atualizada com sucesso"}
    
    def isTokenValid(self,token:str) -> dict:
        try:
            self.getUserId(token)
        except Exception as e:
            raise HTTPException(status_code=401,detail="Token informadonão está associado a um login")
        
        return {"message":"sucesso"}

    def getUserDatas(self,token:str) -> UserDatas:
        userId = None
        try:
            userId = self.getUserId(token)
        except Exception as e:
            raise HTTPException(status_code=401,detail="Token informadonão está associado a um login")
        
        row = None
        try:
            row = self.userRepository.getUserData(userId)
        except Exception as e:
            raise HTTPException(status_code=400,detail="Ocorreu um erro ao obter dados do usuário")
        
        if row is None or row[0] is None or row[1] is None:
            raise HTTPException(status_code=400,detail="Não foi possível obter todos os dados do usuário")
        
        return UserDatas(userName=row[0],userEmail=row[1])
    
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
    
    def generateCode(self) -> int:
        return (random.randint(10000, 90000) + random.randint(11, 9999))