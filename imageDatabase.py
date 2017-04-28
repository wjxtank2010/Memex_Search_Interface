__author__ = 'infosense'
import sqlite3, os, datetime
from base64 import b64decode

# class UserTables:
#     def getTables(self):
#         return ['''
#                 user(
#                 userid INTEGER PRIMARY KEY,
#                 username TEXT,
#                 usercookie TEXT,
#                 password TEXT,
#                 create_time	datetime default current_timestamp
#                 )
#                 '''
#         ]

class DBHandler:
    def __init__(self, dbname, signal=0):
        if signal:
            if os.path.isfile(dbname):
                os.remove(dbname)
        self.conn = sqlite3.connect(dbname,detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        self.cur = self.conn.cursor()

    # def createTables(self, tables):
    #     for table in tables:
    #         self.createTable(table)

    def createTable(self,tableName):
        table = self.getTableByName(tableName)
        self.cur.execute("CREATE TABLE IF NOT EXISTS %s %s"%(tableName,table))

    def getTableByName(self,tableName):
        if tableName == "MemexImgTable":
            return  "(imgID INTEGER PRIMARY KEY,docID TEXT NOT NULL,origURL TEXT NOT NULL,imgPath TEXT NOT NULL)"

        elif tableName == "MemexdocImgTable":
            return  """(docID TEXT NOT NULL,
                        imgPath1 TEXT,
                        imgPath2 TEXT,
                        imgPath3 TEXT,
                        PRIMARY KEY(docID)"""

    def insert(self,tableName,data):
        cmd = ""
        #print(data)
        if tableName == "MemexImgTable":
            cmd = "INSERT INTO MemexImgTable (docID,origURL,imgPath) VALUES (\"%s\",\"%s\",\"%s\")"%data
            #print(cmd)
        elif tableName == "MemexdocImgTable":
            cmd = """INSERT INTO MemexdocImgTable (docID, imgPath1, imgPath2, imgPath3) VALUES (%s, %s, %s, %s)"""
        try:
            self.cur.execute(cmd)
        except:
            print(cmd)

    def rollback(self):
        self.conn.rollback()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()



if __name__ == "__main__":
    imgDir = "/data2/home/jw1498/image37"
    database = "MemexImage.db"
    db = DBHandler(database)
    db.createTable("MemexImgTable")
    for dir in os.listdir(imgDir):
        if not dir.startswith("."):
            partDir = os.path.join(imgDir,dir) #part_1
            for subPart in os.listdir(partDir):
                if not subPart.startswith("."):
                    subPartDir = os.path.join(partDir,subPart)
                    for subImgDir in os.listdir(subPartDir):
                        if not subImgDir.startswith("."):
                            imgSubDir = os.path.join(subPartDir,subImgDir)
                            #print(imgSubDir)
                            for file in os.listdir(imgSubDir):
                                delimiter = "URLDELM"
                                try:
                                    docID,originURL = file.split(delimiter)
                                    originURL = b64decode(originURL)
                                    imgPath = os.path.join(imgSubDir,file)
                                    row = (str(docID),str(originURL),str(imgPath))
                                    #rows.append(row)
                                    db.insert("MemexImgTable",row)
                                except:
                                    print(file)
                            db.commit()