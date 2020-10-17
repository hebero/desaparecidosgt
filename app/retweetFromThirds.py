# app/retweetFromThird.py
import tweepy
import logging
import time
from initApi import start_api
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
history = set()
jump = ["localizada", "localización", "localizado"]
hashtags = ["#IsabelClaudina", "#AlertaIsabelClaudina", "#AlertaAlbaKeneth", "#AlbaKeneth", "#desaparecidosgt", "#botaparecegt"]
class RetweetFromThird(tweepy.StreamListener):
    def __init__(self, api):
        """
        Init stream and listening from twitter with
        certian words
        """
        self.api = api
        self.me = api.me()
    def on_status(self, tweet):
        time.sleep(2)
        logger.info(f"Processing tweet with id: {tweet.id}")
        if tweet.in_reply_to_status_id is not None or tweet.user.id == self.me.id:
            return
        if not tweet.retweeted and not any(jumps in tweet.text.lower() for jumps in jump):
            try:
                if tweet.id not in history:                    
                    tweet.retweet()
                    history.add(tweet.id)
            except Exception as e:
                history.add(tweet.id)
                logger.error("Error on retweet", exc_info=True)
                time.sleep(3)
    
    def on_error(self, status):
        logger.error("Error on retweet ",status)
        time.sleep(3600)

def main(keywords):
    try:
        time.sleep(3)
        api = start_api()
    
        tweets_listener = RetweetFromThird(api=api)
        stream = tweepy.Stream(api.auth, tweets_listener)
        stream.filter(track=keywords)
    except Exception as e:
        logger.error(e)
        time.sleep(3)
        main(keywords=hashtags)

if __name__ == "__main__":
    main(keywords=hashtags)
        
            
