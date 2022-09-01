import os
import logging
import jsonpickle
from departamentos import departamentos
import tweepy
import boto3
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

logger = logging.getLogger()
logger.setLevel(logging.INFO)
patch_all()

deparpartamentos_ = departamentos()
c_key = os.getenv("CONSUMER_KEY")
c_secret = os.getenv("CONSUMER_SECRET")
a_token = os.getenv("ACCESS_TOKEN")
a_token_secrete = os.getenv("ACCESS_TOKEN_SECRET")
locatedKeys = ["#AlbaKeneth", "#AlertaAlbaKeneth", "#AlertaIsabelClaudina"]
a = deparpartamentos_.getDepartamentosBy(1)
jumps = ["love","kiss","ass","night","talented","mouth","calendar","sex","crazy","body","taste","masturbate","smell","fuck","doll","sexy","want","surprise"]
auth = tweepy.OAuthHandler(c_key, c_secret)
auth.set_access_token(a_token,a_token_secrete)
twApi = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

def lambda_handler(event, context):
    try:
        twApi.verify_credentials()
        logging.info("verify successfull")
        reply_mentions(twApi, 1)
    except Exception as e:
        logger.error("error creating the api. Info: ", exc_info=True)
        raise e
    logger.info("Logged in twitter api")

def reply_mentions(api):
    try:
        logger.info("new metion")
        for tweet in tweepy.Cursor(api.mentions_timeline).items():
            new_since_id = max(tweet.id, new_since_id)
            if tweet.in_reply_to_status_id is not None:
                new_since_id = max(tweet.id, new_since_id)
                parentTweet = api.get_status(tweet.in_reply_to_status_id)
                tweetText = parentTweet.text.lower()
                hasJumpsWords = hasAnyKeyWord(jumps, tweetText)

                if(hasAnyKeyWord(locatedKeys, tweetText)):
                #     if not tweetRepo.isLocated(parentTweet.id):
                #         tweetRepo.InsertNewLocatedTweet(parentTweet.id, tweetText, parentTweet.created_at)
                
                    if not (hasJumpsWords)\
                        and len(tweet.entities['urls']) > 0 and since < parentTweet.created_at:
                        try:
                        # if not tweetRepo.isRetweeted(parentTweet.id):
                        #     tweetRepo.InsertNewTweet(parentTweet.id, parentTweet.created_at)
                            parentTweet.retweet()

                            logger.info("auto reply...")
                        except Exception as e:
                            logger.error("Error on retweet", exc_info=True)
                            logger.error(e.message)
            else:
                if not tweet.retweeted and len(tweet.entities['urls']) > 0:
                    try:
                        tweet.retweet()
                    except Exception as e:
                        logger.error("Error on retweet", exc_info=True)
                        logger.error(e.message)
    except Exception as e:
        logger.error("General error")
        return new_since_id
    return new_since_id

def hasAnyKeyWord(keys, text):
    return any(key in text for key in keys)