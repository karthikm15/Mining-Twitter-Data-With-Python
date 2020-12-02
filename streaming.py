# Learning how to stream data in Twitter with a particular keyword

import tweepy
from tweepy import OAuthHandler # for validating the account
from tweepy import Stream # for streaming the data continuusly
from tweepy.streaming import StreamListener
import json
 
consumer_key = 'aweqbVqjyMOEktkyBd7JbGZZs'
consumer_secret = 'dIBiyn0ckpXwbtxb6uhIJ2fFlmfHykMs5DOjza7HCVmTrBkhVE'
access_token = '1318630502794866688-wzTRtwsYDkqUzPBAjFAnXMyLzyHDoS'
access_secret = 'UctZYwgOvsBtP9Jf6gf3iaEc8LZ26k1sgO4oBs48D10sG'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

# Used for gathering alll the particular tweets about an event using the StreamListener() library
# The example below is working with the #python hastag but this can easily be modified

class MyListener(StreamListener):
 
    def on_data(self, data):
        try:
            with open('python.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
        return True
 
    def on_error(self, status):
        print(status)
        return True

# After creatinga the class, it creates an instance using our authentication tokens
# Next, it filters based on the certain keyword
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=['#python'])