import tweepy
import logging
from initApi import start_api
import time


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def reply_mentions(api, since_id):
    logger.info("new metion")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
     since_id=since_id).items():
        if tweet.in_reply_to_status_id is not None:
            parentTweet = api.get_status(tweet.in_reply_to_status_id)
            if not parentTweet.retweeted:
                try:
                    parentTweet.retweet()
                except Exception as e:
                    logger.error("Error on retweet", exc_info=True)
            logger.info("Retweeting...")
        else:
            if not tweet.retweeted:
                try:
                    tweet.retweet()
                except Exception as e:
                    logger.error("Error on retweet", exc_info=True)
    return new_since_id

def on_error(self, status):
    logger.error(status)

def main():
    api = start_api()
    since_id = 1
    while True:
        since_id = reply_mentions(api, since_id)
        logger.info("Waiting...")
        time.sleep(120)

if __name__ == "__main__":
    main()