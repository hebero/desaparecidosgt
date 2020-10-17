import tweepy
import logging
from initApi import start_api
import time


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
history = set()
keywords = ["viendo", "estaba", "ojo", "iniciativa"]
def reply_mentions(api, since_id):
    logger.info("new metion")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
     since_id=since_id).items():
        time.sleep(10)
        if tweet.in_reply_to_status_id is not None:
            try:
                parentTweet = api.get_status(tweet.in_reply_to_status_id)

                if not parentTweet.retweeted and not (any(keyword in parentTweet.text.lower() for keyword in keywords )):
                    try:
                        if parentTweet.id not in history:
                            parentTweet.retweet()
                            history.add(parentTweet.id)
                            logger.info("auto reply...")
                    except Exception as e:
                        history.add(parentTweet.id)
                        logger.error("Error on retweet", exc_info=True)
            except Exception as e:
                logger.error(e)
        else:
            if not tweet.retweeted:
                try:
                    if tweet.id not in history:
                        tweet.retweet()
                        history.add(tweet.id)
                except Exception as e:
                    history.add(tweet.id)
                    logger.error("Error on retweet", exc_info=True)
    return new_since_id

def on_error(self, status):
    logger.error(status)
    raise Exception("error of cursor")

def main():
    logger.info("start auto reply...")
    api = start_api()
    since_id = 1
    while True:
        try:
            since_id = reply_mentions(api, since_id)
            logger.info("Waiting...")
            time.sleep(120)
        except Exception as e:
            logger.error("Error on main process", e)
            time.sleep(60)
            main()

if __name__ == "__main__":
    main()
