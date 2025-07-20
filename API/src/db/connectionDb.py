import mysql.connector
from dotenv import load_dotenv
load_dotenv()
import os

class ConnectionDB:

    def __init__(self):
        self.HOST_DATABASE     = os.environ["HOST_DATABASE"] 
        self.PORT_DATABASE     = os.environ["PORT_DATABASE"]
        self.USER_DATABASE     = os.environ["USER_DATABASE"]
        self.PASSWORD_DATABASE = os.environ["PASSWORD_DATABASE"]
        self.NAME_DATABASE     = os.environ["NAME_DATABASE"]
        self.myCursor = None
        self.myDb = None

    def createConnection(self) -> None:
        print("self.HOST_DATABASE ",self.HOST_DATABASE)
        print("self.PORT_DATABASE ",self.PORT_DATABASE)
        print("self.PASSWORD_DATABASE ",self.PASSWORD_DATABASE)
        self.myDb = mysql.connector.connect(host=self.HOST_DATABASE,port=self.PORT_DATABASE,user=self.USER_DATABASE,password=self.PASSWORD_DATABASE,database=self.NAME_DATABASE)
        self.myCursor = self.myDb.cursor()
    
    def closeConnection(self) -> None:
        if self.myCursor:
            self.myCursor.close()
        if self.myDb:
            self.myDb.close()


if __name__ == "__main__":
    connection = ConnectionDB()
    connection.createConnection()
    print("Conexão com o banco de dados estabelecida com sucesso!")
    connection.closeConnection()
