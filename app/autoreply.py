import tweepy
import logging
from initApi import start_api
import time
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def reply_mentions(api, keywords, since_id):
    logger.info("new metion")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
     since_id=since_id).items():
        if tweet.in_reply_to_status_id is not None:
            continue

def main():
    api = start_api()
    since_id =1
    while True:
        since_id = reply_mentions(api, [""], since_id)