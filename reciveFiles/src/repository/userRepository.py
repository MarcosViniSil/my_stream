from datetime import datetime, timedelta
import uuid
from uuid import UUID
import mysql.connector
from mysql.connector import errorcode
from src.db.connectionDb import ConnectionDB
from src.models.user import User


class UserRepository:
    
    def __init__(self, db: ConnectionDB):
        self.Db = db

    def createUser(self,user:User) -> None:
        userId = uuid.uuid4().bytes

        self.Db.createConnection()

        sql = """
                INSERT INTO tb_user (userId,userName,userRole,userEmail,userPassword) VALUES (%s,%s,%s,%s,%s);
        """
        try:
            self.Db.myCursor.execute(sql, (userId,user.name,'USER',user.email,user.password))
            self.Db.myDb.commit()
            self.Db.closeConnection()

        except mysql.connector.IntegrityError as e:
            if e.errno == errorcode.ER_DUP_ENTRY:  
                self.Db.closeConnection()
                raise ValueError("E-mail já cadastrado.")
            else:
                self.Db.closeConnection()
                raise ValueError(f"Erro inesperado ao criar usuário: {e}")
        except Exception as e:
            self.Db.closeConnection()
            raise ValueError(f"Erro inesperado ao criar usuário: {e}")
        
    def getHashedPassword(self,email:str) -> dict:

        self.Db.createConnection()

        sql = """
                SELECT userPassword FROM tb_user WHERE userEmail = %s; 
        """
        try:
            self.Db.myCursor.execute(sql, (email,))
            row = self.Db.myCursor.fetchone()
            self.Db.myDb.commit()
            self.Db.closeConnection()

            return row

        except Exception as e:
            print(e)
            raise ValueError("Erro ao verificar dados para login", e)
        
    def getUserId(self,email:str) -> dict:

        self.Db.createConnection()

        sql = """
                SELECT userId FROM tb_user WHERE userEmail = %s; 
        """
        try:
            self.Db.myCursor.execute(sql, (email,))
            row = self.Db.myCursor.fetchone()
            self.Db.myDb.commit()
            self.Db.closeConnection()

            return row

        except Exception as e:
            print(e)
            raise ValueError("Erro ao verificar dados para login", e)
        
    def getUserData(self,userId:bytes) -> dict:

        self.Db.createConnection()

        sql = """
                SELECT userName,userEmail FROM tb_user WHERE userId = %s; 
        """
        try:
            self.Db.myCursor.execute(sql, (userId,))
            row = self.Db.myCursor.fetchone()
            self.Db.myDb.commit()
            self.Db.closeConnection()

            return row

        except Exception as e:
            print(e)
            raise ValueError("Erro ao verificar dados para login", e)


    def updateUserDatas(self,userId:bytes,userName:str,userEmail:str) -> None:

        self.Db.createConnection()

        sql = """
                UPDATE tb_user SET userName = %s, userEmail = %s WHERE userId = %s; 
        """
        try:
            self.Db.myCursor.execute(sql, (userName,userEmail,userId))
            self.Db.myDb.commit()
            self.Db.closeConnection()

        except Exception as e:
            print(e)
            raise ValueError("Erro ao atualizar dados do usuário", e)
        
    
    def createCodeUser(self,userId:bytes,code:int) -> None:
        codeId = uuid.uuid4().bytes

        self.Db.createConnection()
        codeType = 0
        createdAt = datetime.now()
        expiresAt = createdAt + timedelta(minutes=5)
        isCodeUsed = False

        sql = """
                INSERT INTO tb_userCodeVerification (userCodeId,code,codeType,createdAt,expiresAt,isCodeUsed,idUser) VALUES (%s,%s,%s,%s,%s,%s,%s);
        """
        try:
            self.Db.myCursor.execute(sql, (codeId,code,codeType,createdAt,expiresAt,isCodeUsed,userId))
            self.Db.myDb.commit()
            self.Db.closeConnection()

        except Exception as e:
            self.Db.closeConnection()
            raise ValueError(f"Ocorreu um erro ao registrar código {e}")
    
    def getCodeById(self,userId:bytes,code:int) -> dict:

        self.Db.createConnection()

        sql = """
                SELECT code,expiresAt FROM tb_userCodeVerification WHERE idUser = %s AND code = %s; 
        """
        try:
            self.Db.myCursor.execute(sql, (userId,code))
            row = self.Db.myCursor.fetchone()
            self.Db.myDb.commit()

            return row

        except Exception as e:
            print(e)
            raise ValueError("Erro ao obter código", e)
        finally:
            self.Db.closeConnection()

        
    def updateUserPassword(self,email:str,newPassword:str) -> None:

        self.Db.createConnection()

        sql = """
                UPDATE tb_user SET userPassword = %s WHERE userEmail = %s; 
        """
        try:
            self.Db.myCursor.execute(sql, (newPassword,email))
            self.Db.myDb.commit()
            self.Db.closeConnection()

        except Exception as e:
            print(e)
            raise ValueError("Erro ao atualizar dados do usuário", e)