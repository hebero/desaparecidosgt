from logging import Logger
import tweepy
import logging
from initApi import start_api
import json

logging.basicConfig(level= logging.INFO)
logger = logging.getLogger()

class RetweetFromTimeline():
    def __init__(self, api):
        """
        Read timeline and applies retweets
        """
        self.api = api
        self.me = api.me()
    def on_status(self,tweet):
        logger.info(f"readed from timeline:{tweet.id}")
        if tweet.in_reply_to_status_id is not None or tweet.user.id == self.me.id:
            return
        if not tweet.retweeted:
            try:
                tweet.


