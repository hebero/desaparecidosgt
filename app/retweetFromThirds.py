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
            if(not tweet.user.screen_name =="botaparecegt"):
                tweetId = tweet.id
                tweetUser = tweet.user.screen_name
                getHashtags = self.getHashTag(tweet.full_text.lower())
                quotedTweet = "https://twitter.com/{}/status/{}".format(tweetUser, tweetId)
                tweetText = "Ayúdanos a encontrar esta persona compartiendo esta información {}".format(getHashtags)
                self.api.update_status(tweetText, attachment_url=quotedTweet)

        except Exception as e:
            logger.error("error on creating quoted tweet")
            logging.critical(e,exc_info=True)


    def on_status(self, tweet):
        #time.sleep(120)
        logger.info(f"Processing tweet with id: {tweet.id}")
        if tweet.in_reply_to_status_id is not None or tweet.user.id == self.me.id:
            return
        full_tweet  = self.api.get_status(tweet.id, tweet_mode='extended')
        tweetText = full_tweet.full_text.lower()

        hasJumps = any(jumps in tweetText for jumps in jump)
        isMe = tweet.user.screen_name == "botaparecegt"
        isLocated = any(locatedWord in tweetText for locatedWord in locatedKeys)
        if isLocated and not isMe:
            if not tweetRepo.isLocated(tweet.id):
                tweetRepo.InsertNewLocatedTweet(tweet.id,tweetText, tweet.created_at)
        if not tweet.retweeted and not hasJumps and tweet.created_at > since and not isMe:
            try:
                if not tweetRepo.isRetweeted(tweet.id):
                    tweetRepo.InsertNewTweet(tweet.id, tweet.created_at)
                    if (tweet.retweeted_status is None):
                        self.quoted_tweet(full_tweet)
                    else:
                        if(not tweetRepo.isRetweeted(tweet.retweeted_status.id)):
                            originalTweet = self.api.get_status(tweet.retweeted_status.id, tweet_mode='extended')
                            print(originalTweet)
                            self.quoted_tweet(originalTweet)
                    tweet.retweet()
            except Exception as e:
                tweetRepo.InsertNewTweet(tweet.id, tweet.created_at)
                logging.critical(e,exc_info=True)
                logger.error("Error on retweet", exc_info=True)
                time.sleep(300)
    
    def on_error(self, status):
        logger.error("Error on retweet ",status)
        #wait if twitter return 420 error
        time.sleep(3600)


    def getHashTag(self, tweetText):
        hashtag = ""
        tweetText = tweetText.replace('.', '')
        tweetText = tweetText.replace(',', '')
        tweetText = tweetText.replace('\n', ' ')
        setOfText = tweetText.split(' ')
        print(setOfText)
        for index in range(len(setOfText)):
            word = setOfText[index]
            print(word)
            if any(departamento1 in word for departamento1 in departamentos1):
                print(hashtag)
                hashtag = departamentos1[word]
                break
        if hashtag == "":
            
            for index in range(len(setOfText)):
                word = setOfText[index]
                if (index - 1) > 0:
                    wholeWord = setOfText[index -1] + ' ' + word
                    print(wholeWord)
                    if any(deparamento in wholeWord for deparamento in departamentos2):
                        hashtag = departamentos2[wholeWord]
                        print(hashtag)
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
        
            
