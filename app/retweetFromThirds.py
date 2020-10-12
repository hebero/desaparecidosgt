# app/retweetFromThird.py
import tweepy
import logging
from initApi import start_api
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class RetweetFromThird(tweepy.StreamListener):
    def __init__(self, api):
        """
        Init stream and listening from twitter with
        certian words
        """
        self.api = api
        self.me = api.me()
    def on_status(self, tweet):
        logger.info(f"Processing tweet with id: {tweet.id}")
        if tweet.in_reply_to_status_id is not None or tweet.user.id == self.me.id:
            return
        if not tweet.favorited:
            return 
        if not tweet.retweeted:
            try:
                tweet.retweet()
            except Exception as e:
                logger.error("Error on retweet", exc_info=True)
    
    def on_error(self, status):
        logger.error(status)

def main(keywords):
    api = start_api()
    tweets_listener = RetweetFromThird(api=api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=keywords, languages=["es"])

if __name__ == "__main__":
    main(keywords=["albakeneth", "alertaalbakeneth"])
        
            