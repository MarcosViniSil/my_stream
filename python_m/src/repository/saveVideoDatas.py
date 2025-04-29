from fastapi import Depends
from src.db.connectionDb import ConnectionDB

class SaveVideoDatas:
    
    def __init__(self, db: ConnectionDB):
        self.Db = db


    def testCreation(self):
        self.Db.createConnection()
        sql = "CREATE TABLE tb_user2(id INT PRIMARY KEY);"
        self.Db.myCursor.execute(sql)
        self.Db.myDb.commit()
        self.Db.closeConnection()

if __name__ == "__main__":
    saveVideoDatas = SaveVideoDatas()
    saveVideoDatas.testCreation()