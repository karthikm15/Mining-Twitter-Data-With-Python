import pandas
import json
import vincent

from collections import defaultdict
import operator 
import json # necessary for extracting the JSON file containing the Python info
from collections import Counter # keeping track of all the frequencies
import re # joining necessary parts like hashtags and emotes together
import string
from nltk import bigrams # will take a list of tokens and produce a list of tuples using adjacent tokens

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords # explicitly for removing stop words
 
com = defaultdict(lambda : defaultdict(int))
punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'RT', '...', '1', 'via']

# Catching for certain emoticons so that it doesn't split
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""
 
# Catching additional keywords (like URLs and hash-tags)
regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
 
    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]
 
# Allowing spaces to be ignored and catching uppercases/lowercases   
tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

# Catching all tokens in a string and returns as a list 
def tokenize(s):
    return tokens_re.findall(s)
 
# Making sure that emoticons are not lowercased
def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens


dates_python= []
# f is the file pointer to the JSON data set
fname = 'python.json'
with open(fname, 'r') as f:
	for line in f:
	    tweet = json.loads(line)
	    # let's focus on hashtags only at the moment
	    terms_hash = [term for term in preprocess(tweet['text']) if term.startswith('#')]
	    # track when the hashtag is mentioned
	    if '#python' in terms_hash:
	        dates_python.append(tweet['created_at'])
 
# a list of "1" to count the hashtags
ones = [1]*len(dates_python)
# the index of the series
idx = pandas.DatetimeIndex(dates_python)
# the actual series (at series of 1s for the moment)
python = pandas.Series(ones, index=idx)
 
# Resampling / bucketing
per_minute = python.resample('1Min').sum().fillna(0)

time_chart = vincent.Line(python)
time_chart.axis_titles(x='Time', y='Freq')

time_chart.to_json('time_chart.json', html_out=True, html_path='timeseries.html')