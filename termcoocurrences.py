# Catching term re-occurrences where the two terms are frequently in the same tweet
# Different from bigrams as bigrams often have to be together

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

# f is the file pointer to the JSON data set
fname = 'python.json'
with open(fname, 'r') as f:
    for line in f: 
        tweet = json.loads(line)
        terms_only = [term for term in preprocess(tweet['text']) 
                      if term not in stop 
                      and not term.startswith(('#', '@'))]
     
        # Build co-occurrence matrix
        for i in range(len(terms_only)-1):            
            for j in range(i+1, len(terms_only)):
                w1, w2 = sorted([terms_only[i], terms_only[j]])                
                if w1 != w2:
                    com[w1][w2] += 1


com_max = []
# For each term, look for the most common co-occurrent terms
for t1 in com:
    t1_max_terms = sorted(com[t1].items(), key=operator.itemgetter(1), reverse=True)[:5]
    for t2, t2_count in t1_max_terms:
        com_max.append(((t1, t2), t2_count))
# Get the most frequent co-occurrences (in this case, it's the top 5)
terms_max = sorted(com_max, key=operator.itemgetter(1), reverse=True)
print(terms_max[:5])