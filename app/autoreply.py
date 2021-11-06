from TweetsRepository import TweetsRepository
from random import paretovariate
import tweepy
import datetime
import logging
from initApi import start_api
from keyWordsRepository import keyWordsRepository
import time


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
jump = []
keyRepo = None
tweetRepo = TweetsRepository()
since  = None
def reply_mentions(api, since_id):
    try:
        logger.info("new metion")
        new_since_id = since_id
        for tweet in tweepy.Cursor(api.mentions_timeline,
        since_id=since_id).items():
            new_since_id = max(tweet.id, new_since_id)
            if tweet.in_reply_to_status_id is not None:
                new_since_id = max(tweet.id, new_since_id)
                parentTweet = api.get_status(tweet.in_reply_to_status_id)
                tweetText = parentTweet.text.lower()
                hasJumpsWords = hasAnyKeyWord(jump, tweetText)

                if(hasAnyKeyWord(locatedKeys, tweetText)):
                    if not tweetRepo.isLocated(parentTweet.id):
                        tweetRepo.InsertNewLocatedTweet(parentTweet.id, tweetText, parentTweet.created_at)
                
                if not (hasJumpsWords)\
                        and len(tweet.entities['urls']) > 0 and since < parentTweet.created_at:
                    try:
                        if not tweetRepo.isRetweeted(parentTweet.id):
                            tweetRepo.InsertNewTweet(parentTweet.id, parentTweet.created_at)
                            parentTweet.retweet()
                            logger.info("auto reply...")
                    except Exception as e:
                        logger.error("Error on retweet", exc_info=True)
                        logger.error(e.message)
            else:
                if not tweet.retweeted and len(tweet.entities['urls']) > 0:
                    try:
                        if not tweetRepo.isRetweeted(tweet.id) and since < tweet.created_at:
                            tweetRepo.InsertNewTweet(tweet.id, tweet.created_at)
                            tweet.retweet()
                    except Exception as e:
                        tweetRepo.InsertNewTweet(tweet.id, tweet.created_at)
                        logger.error("Error on retweet", exc_info=True)
                        logger.error(e.message)
    except Exception as e:
        logger.error("General error")
        return new_since_id
    return new_since_id

def on_error(self, status):
    logger.error(status)

def main():
    logger.info("start auto reply...")
    since = datetime.datetime(2021,3,15)
    api = start_api()
    since_id = 1
    while True:
        since_id = reply_mentions(api, since_id)
        logger.info("Waiting...")
        time.sleep(120)

def hasAnyKeyWord(keys, text):
    return any(key in text for key in keys)

if __name__ == "__main__":
    since = datetime.datetime(2021, 3, 15)
    keyRepo = keyWordsRepository()
    jump = keyRepo.getKeyWords("jump")
    locatedKeys = keyRepo.getKeyWords("located")
    main()