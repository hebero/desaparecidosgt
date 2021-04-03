import tweepy
import os
import logging
from mysql.connector import connect, Error

logger =  logging.getLogger()

sqlConnection = getConnection()
keyWords = []

def getConnection():
    try:
        with connect(
            host="localhost",
            user= os.getenv("SQLUSER"),
            password = os.getenv("SQLPASS"),
        ) as connection:
            return connection
    except Error as e:
        raise e

def getKeyWords():
    query = "SELECT WORDS FROM KEYWORDS"
    with sqlConnection.cursor() as cursor: 
        cursor.execute(query)
        result = cursor.fetchall()
        for row in result:


def start_api():
    #get keys from os registry
    c_key = os.getenv("CONSUMER_KEY")
    c_secret = os.getenv("CONSUMER_SECRET")
    a_token = os.getenv("ACCESS_TOKEN")
    a_token_secrete = os.getenv("ACCESS_TOKEN_SECRET")
    auth = tweepy.OAuthHandler(c_key, c_secret)
    auth.set_access_token(a_token,a_token_secrete)
    twApi = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
     
    try:
        twApi.verify_credentials()
        logging.info("verify successfull")
    except Exception as e:
        logger.error("error creating the api. Info: ", exc_info=True)
        raise e
    logger.info("Logged in twitter api")
    return twApi
