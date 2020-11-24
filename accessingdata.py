# Learning how to access data like tweets, followers, and messages using the tweepy library

import tweepy
from tweepy import OAuthHandler
import json
 
consumer_key = 'aweqbVqjyMOEktkyBd7JbGZZs'
consumer_secret = 'dIBiyn0ckpXwbtxb6uhIJ2fFlmfHykMs5DOjza7HCVmTrBkhVE'
access_token = '1318630502794866688-wzTRtwsYDkqUzPBAjFAnXMyLzyHDoS'
access_secret = 'UctZYwgOvsBtP9Jf6gf3iaEc8LZ26k1sgO4oBs48D10sG'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

# Check the profile's timeline with these keys

def process_or_store(tweet):
    print(json.dumps(tweet))

for status in tweepy.Cursor(api.home_timeline).items(10):
    process_or_store(status.text)