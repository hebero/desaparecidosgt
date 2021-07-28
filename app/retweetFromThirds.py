# app/retweetFromThird.py
from TweetsRepository import TweetsRepository
import tweepy
import logging
import time
import datetime
from initApi import start_api
from keyWordsRepository import keyWordsRepository
import json


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
sice =  None
jump = []
keyRepo = None
tweetRepo = TweetsRepository()
class RetweetFromThird(tweepy.StreamListener):
    def __init__(self, api):
        """
        The stream get tweets what contain the keywords in hashtag
        """
        self.api = api
        self.me = api.me()
    def on_status(self, tweet):
        #time.sleep(120)
        logger.info(f"Processing tweet with id: {tweet.id}")
        if tweet.in_reply_to_status_id is not None or tweet.user.id == self.me.id:
            return
        if not tweet.retweeted and not any(jumps in tweet.text.lower() for jumps in jump) and tweet.created_at > since:
            try:
                if not tweetRepo.isRetweeted(tweet.id):
                    tweetRepo.InsertNewTweet(tweet.id, tweet.created_at)
                    tweet.retweet()
            except Exception as e:
                tweetRepo.InsertNewTweet(tweet.id, tweet.created_at)
                logger.error("Error on retweet", exc_info=True)
                time.sleep(300)
    
    def on_error(self, status):
        logger.error("Error on retweet ",status)
        #wait if twitter return 420 error
        time.sleep(3600)

def main(keywords):
    #time.sleep(3600)
    try:
        api = start_api()
        tweets_listener = RetweetFromThird(api=api)
        stream = tweepy.Stream(api.auth, tweets_listener)
        stream.filter(track=keywords)
    except Exception as e:
        logger.error(e)
        time.sleep(3)
        main(keywords=hashtags)

if __name__ == "__main__":
    since = datetime.datetime(2021, 3, 15)
    keyRepo = keyWordsRepository()
    jump = keyRepo.getKeyWords("jump")
    hashtags = keyRepo.getKeyWords("key")
    main(keywords=hashtags)
        
            
