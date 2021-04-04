import os
import logging
from mysql.connector import connect, Error
class keyWordsRepository:
    config = None
    def __init__(self):
        self.config = {
            "host": "localhost",
            "user": "root" ,#os.getenvt("SQLUSER"),
            "password": "root" ,#os.getenvt("SQLUSER"),
            "database" : "desaparecidosgt"
        }

    def getKeyWords(self, type):
        genSet = []
        query = "SELECT WORDS FROM KEYWORDS WHERE WTYPE = '" + type + "'"
        sqlConnection = connect(**self.config)
        if sqlConnection.is_connected():
            print("db connection ok")
        with sqlConnection.cursor() as cursor: 
            cursor.execute(query)
            result = cursor.fetchall()
            for row in result:
                genSet.append(row[0])
        return genSet
