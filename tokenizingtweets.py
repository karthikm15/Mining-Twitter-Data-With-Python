# Tokenization: splitting a stream of text into smaller units called tokens

import nltk
nltk.download('punkt')

from nltk.tokenize import word_tokenize
 
tweet = 'Hi! This message will soon be tokenized into its individual components :)'
print(word_tokenize(tweet))