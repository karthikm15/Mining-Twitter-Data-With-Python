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

# Makes the 
with open('python.json', 'r') as f:
    line = f.readline()
    tweet = json.loads(line) 
    print(json.dumps(tweet, indent=1)) 