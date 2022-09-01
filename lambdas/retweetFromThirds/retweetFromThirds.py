import tweepy
import logging
import time
import datetime
import json
import os
logger =  logging.getLogger()

def lambda_handler(event, context):
    c_key = os.getenv("CONSUMER_KEY")
    c_secret = os.getenv("CONSUMER_SECRET")
    a_token = os.getenv("ACCESS_TOKEN")
    a_token_secrete = os.getenv("ACCESS_TOKEN_SECRET")
    auth = tweepy.OAuthHandler(c_key, c_secret)
    auth.set_access_token(a_token,a_token_secrete)
    twApi = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    try:
        twApi.verify_credentials()
        logging.info("verify successfull")

        tweets_listener = RetweetFromThird(api=twApi)
        stream = tweepy.Stream(twApi.auth, tweets_listener)
        stream.filter(track=keywords)
        
    except Exception as e:
        logger.error("error creating the api. Info: ", exc_info=True)
        raise e
    logger.info("Logged in twitter api")

class RetweetFromThird(tweepy.StreamListener):
    def __init__(self, api):
        """
        The stream get tweets what contain the keywords in hashtag
        """
        self.api = api
        self.me = api.me()
    def quoted_tweet(self, tweet, isAlbaKeneth):
        try:
            if(not tweet.user.screen_name =="botaparecegt"):
                names = "esta persona"
                tweetId = tweet.id
                tweetUser = tweet.user.screen_name
                if isAlbaKeneth==True:
                    names = self.getNameAlbaKeneth(tweet.full_text)
                getHashtags = self.getHashTag(tweet.full_text.lower())
                
                    
                quotedTweet = "https://twitter.com/{}/status/{}".format(tweetUser, tweetId)
                tweetText = " ❗ Ayúdanos a encontrar a {} compartiendo su información ❗{} ".format(names,getHashtags)
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
        hasBlockedWords = hasAnyKey(jump, tweetText)
        isIsabelClaudina = hasAnyKey(isabelClaudinaKeys, tweetText)
        isAlbaKeneth = hasAnyKey(albaKenethKeys, tweetText)
        isMe = tweet.user.screen_name == "botaparecegt"
        isLocated = hasAnyKey(locatedKeys,tweetText)
        if isLocated and not isMe:
            if not tweetRepo.isLocated(tweet.id):
                tweetRepo.InsertNewLocatedTweet(tweet.id,tweetText, tweet.created_at)
        elif not hasBlockedWords and not isLocated and tweet.created_at > since and not isMe:
            try:
                if not tweetRepo.isRetweeted(tweet.id):
                    tweetRepo.InsertNewTweet(tweet.id, tweet.created_at)
                    if(isAlbaKeneth or isabelClaudinaKeys):
                        if (hasattr(tweet,'retweeted_status') and tweet.retweeted_status is None):
                            self.quoted_tweet(full_tweet, isAlbaKeneth)
                        else:
                            if(not tweetRepo.isRetweeted(tweet.retweeted_status.id)):
                                originalTweet = self.api.get_status(tweet.retweeted_status.id, tweet_mode='extended')
                                print(originalTweet)
                                self.quoted_tweet(originalTweet, isAlbaKeneth)
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
        
    def getNameAlbaKeneth(self, tweetText):
        txt = str(tweetText)
        names = ""
        indexOfSeparetor = txt.find(' ⚠ |')
        firstDot = txt.find('.')
        if(indexOfSeparetor > 0 and firstDot > 0):
            indexOfSeparetor = indexOfSeparetor + 5
            names = txt[indexOfSeparetor:firstDot]
            return names


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


def hasAnyKey(setOfKeys, text):
    return any(key.lower() in text for key in setOfKeys)

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
        raise 