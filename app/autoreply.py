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
        
        if any(keyword in tweet.text.lower() for keyword in keywords):
            logger.info("Retweeting...")
            tweet.retweet()
    return new_since_id

def main():
    api = start_api()
    since_id = 1
    while True:
        since_id = reply_mentions(api, ["ayuda", "busca", "perdida", "perdido"], since_id)
        logger.info("Waiting...")
        time.sleep(120)

if __name__ == "__main__":
    main()