import os
import logging
from mysql.connector import connect, Error

class TweetsRepository():
    config = None
    setIds = []
    def __init__(self):
        self.config = {
            "host": "localhost",
            "user": os.getenvt("SQLUSER"),
            "password": os.getenvt("SQLUSER"),
            "database" : "desaparecidosgt"
        }
    
    def InsertNewTweet(self, id, date):
        
        with connect(**self.config) as connection:
            if connection.is_connected():
                with connection.cursor() as cursor:
                    if not (self.isRetweeted(id)):

                        query = "INSERT INTO ReTweets (id, created_at) values ('{}', '{}')" .format(id, date)
                        cursor.execute(query)
                        connection.commit()
                        connection.close()

    def InsertNewLocatedTweet(self, id, text, date):
        with connect(**self.config) as connection:
            if connection.is_connected():
                with connection.cursor() as cursor:
                    query = "INSERT INTO LocatedTweets(id, tweet_text, created_at) values ('{}','{}', '{}'".format(id, text, date)
                    cursor.execute(query)
                    connection.commit()
                    connection.close()

    def isRetweeted(self, id):
        with connect(**self.config) as connection:
            with connection.cursor() as cursor:
                query =  "SELECT id FROM ReTweets where id = '" + str(id) + "'"
                cursor.execute(query)
                result = cursor.fetchall()
                if len(result) == 0:
                    connection.close()
                    return False
                else:
                    connection.close()
                    return True
            
    def isLocated(self, id):
        with connect(**self.config) as connection:
            if connection.is_connected():
                with connection.cursor() as cursor:
                    query = "SELECT id FROM LocatedTweets WHERE id = '{}'".format(str(id))
                    cursor.execute(query)
                    result = cursor.fetchall()
                    if len(result)== 0:
                        connection.close()
                        return False
                    else:
                        connection.close()
                        return True


