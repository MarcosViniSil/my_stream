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