import tweepy
import os
import logging

logger =  logging.getLogger()

def start_api():
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
    logger.info("Ok :D")
    return twApi
