# app/retweetFromThird.py
import tweepy
import logging
import time
from initApi import start_api
import json


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
hashtags = ["#IsabelClaudina", "#AlertaIsabelClaudina", "#AlertaAlbaKeneth", "#AlbaKeneth", "#desaparecidosgt", "#botaparecegt"]
class RetweetFromThird(tweepy.StreamListener):
    def __init__(self, api):
        """
        The stream get tweets what contain the keywords in hashtag
        """
        self.api = api
        self.me = api.me()
    def on_status(self, tweet):
        time.sleep(120)
        logger.info(f"Processing tweet with id: {tweet.id}")
        if tweet.in_reply_to_status_id is not None or tweet.user.id == self.me.id:
            return
        if not tweet.retweeted:
            try:
                tweet.retweet()
            except Exception as e:
                logger.error("Error on retweet", exc_info=True)
                time.sleep(300)
    
    def on_error(self, status):
        logger.error("Error on retweet ",status)
        #wait if twitter return 420 error
        time.sleep(3600)

def main(keywords):
    time.sleep(3600)
    api = start_api()
    tweets_listener = RetweetFromThird(api=api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=keywords)

def loadKeyWords():


if __name__ == "__main__":

    main(keywords=hashtags)
        
            
