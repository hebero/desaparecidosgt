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
departamentos1 = dict()
departamentos2 = dict()
locatedKeys = set()
tweetRepo = TweetsRepository()
class RetweetFromThird(tweepy.StreamListener):
    def __init__(self, api):
        """
        The stream get tweets what contain the keywords in hashtag
        """
        self.api = api
        self.me = api.me()
    def quoted_tweet(self, tweet):
        try:
            tweetId = tweet.id
            tweetUser = tweet.user.screen_name
            getHashtags = self.getHashTag(tweet.text.lower())
            quotedTweet = "https://twitter.com/{}/status/{}".format(tweetUser, tweetId)
            tweetText = "Ayúdanos a encontrar esta persona compartiendo esta información {}".format(getHashtags)
            self.api.update_status(tweetText, attachment_url=quotedTweet)
        except Exception as e:
            logger.error("")

    def on_status(self, tweet):
        #time.sleep(120)
        logger.info(f"Processing tweet with id: {tweet.id}")
        if tweet.in_reply_to_status_id is not None or tweet.user.id == self.me.id:
            return
        tweetText = tweet.text.lower()
        hasJumps = any(jumps in tweetText for jumps in jump)
        isLocated = any(locatedWord in tweetText for locatedWord in locatedKeys)
        if isLocated:
            if not tweetRepo.isLocated(tweet.id):
                tweetRepo.InsertNewTweet(tweet.id, tweet.created_at)
        if not tweet.retweeted and not hasJumps and tweet.created_at > since:
            try:
                if not tweetRepo.isRetweeted(tweet.id):
                    tweetRepo.InsertNewTweet(tweet.id, tweet.created_at)
                    if (tweet.retweeted_status is None):
                        self.quoted_tweet(tweet)
                    else:
                        if(not tweetRepo.isRetweeted(tweet.retweeted_status.id)):
                            self.quoted_tweet(tweet.retweeted_status)
                    tweet.retweet()
            except Exception as e:
                tweetRepo.InsertNewTweet(tweet.id, tweet.created_at)
                logger.error("Error on retweet", exc_info=True)
                time.sleep(300)
    
    def on_error(self, status):
        logger.error("Error on retweet ",status)
        #wait if twitter return 420 error
        time.sleep(3600)


    def getHashTag(self, tweetText):
        hashtag = ""
        setOfText = tweetText.split(' ')
        for index in range(len(setOfText)):
            word = setOfText[index]
            if word in departamentos1:
                hashtag = departamentos1[word]
                break
        if hashtag == "":
            
            for index in range(len(setOfText)):
                word = setOfText[index]
                if (index - 1) > 0:
                    wholeWord = setOfText[index -1] + ' ' + word
                    if any(deparamento in wholeWord for deparamento in departamentos2):
                        hashtag = departamentos2[wholeWord]
                        break
        
        return hashtag



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
    since = datetime.datetime(2021, 6, 15)
    keyRepo = keyWordsRepository()
    jump = keyRepo.getKeyWords("jump")
    locatedKeys = keyRepo.getKeyWords("located")
    hashtags = keyRepo.getKeyWords("key")
    departamentos1 = keyRepo.getDepartamentosByWords(1)
    departamentos2 = keyRepo.getDepartamentosByWords(2)
    print("hashtags: ")
    print(hashtags)
    print("departamentos:")
    print(departamentos1)
    print(departamentos2)

    main(keywords=hashtags)
        
            
