# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 16:14:41 2020

@author: Rimusa
"""

import re
import pandas as pd

from nltk.tokenize import TweetTokenizer


#################################################################################

def fetch_longtweet(df, size=-1):
    """
    
    Input: a dataframe obtained from raw twitter data
    
    Output: the unabbreviated twitter text as a pandas Series
    
    Note, this assumes that you just joined the code from my previous tsv files
    
    """
    
    # Select the text of the Tweets
    tweets = df["text"]

    # Initialize one list with all of the actual Tweets
    text_tweets = []

    for i, tweet in enumerate(tweets[0:size]):
        
        # If there is no extended Tweet information, keep the text
        if not df["extended_tweet"].iloc[i]:
            text = tweet
            
        # If there is extended Tweet information, use the extended text
        else:
            text = df["extended_tweet"].iloc[i]
            text = ast.literal_eval(text)
            text = text["full_text"]

        # Add the chosen text to the list
        text_tweets.append(text)
        
        # This is so the user doesn't get bored
        if (i % 10000) == 0:
            print(i,"of",len(tweets[0:size]),"Tweets fetched...")
            
    # This is so the user doesn't get bored
    print(len(tweets[0:size]),"of",len(tweets[0:size]),"Tweets fetched...")
    
    # Return a pandas Series
    return pd.Series(text_tweets)





##################################################################################

"""
The following code is based on Mugdha's preprocessing script (https://github.com/
seraphinatarrant/embedding_bias/tree/Mugdha) it has been modified to be more
reusable (e.g. it accepts any kind of iterable instead of just files). All of
these assume that the input consists of an iterable data that includes only strings
that represent the Tweet text.
"""


def clean_tweet(text, vocab, tokenizer=TweetTokenizer()):
    """
    
    Input: a Tweet in string format and a dictionary containing the vocabulary
    
    Output: the cleaned and tokenized Tweet and the updated vocabulary
    
    """
    
    # If the Tweet has no text, it returns no tokens
    if text == '\n':
        return [], vocab
    
    # Turn the text into lowercase
    tweet = text.lower()
    
    # Different kinds of special tokens that we can find
    tweet = re.sub(r'\#', " <HASH> ", tweet)                   # hashtags
    tweet = re.sub(r'\@.[a-zA-Z0-9]\S+', " <MENTION> ", tweet) # mentions
    tweet = re.sub(r'https?:\/\/.\S*', " <URL> ", tweet)       # url
    tweet = re.sub(r"\n", " ", tweet)                          # linebreaks
    tweet = re.sub(r'\s+'," ",tweet)                           # extra space
    tweet = re.sub(r"\"","\'",tweet)                           # change " to '
    
    # Tokenize the cleaned string
    tokens = tokenizer.tokenize(tweet)
    
    # Add the token counts into the vocabulary
    for token in tokens:
        if token in vocab.keys():
            vocab[token] += 1
        else:
            vocab[token] = 1

    # Return both the tokenized tweet and the vocabulary
    return tokens, vocab


def preprocess_tweet(text, vocab, tokenizer=TweetTokenizer()):
    """
    
    Input: a Tweet in string format and a vocabulary
    
    Output: the tokenized tweet where we substitute all oov words with
    the <UNK> token.
    
    """
    
    # Tokenize the Tweet
    tokens = tokenizer.tokenize(text)
    
    # This function replaces oov tokens with <UNK>
    def replace_token(token):
        if token in vocab:
            return token
        else:
            return "<UNK>"
    
    # Maps the previous list on the tokenized Tweet
    tokens = list(map(replace_token, tokens))
    
    return tokens


#####################


def cleaner(data, threshold=0, gen_vocab=True):
    """
    
    Input: an iterable that gives out Tweets as strings and the value under which
    we consider words to be oov.
    
    Output: a list of cleaned Tweets as strings and the vocabulary
    
    """
    
    # Initialize the vocabulary and the list of cleaned Tweets
    vocab = dict()
    cleaned_tweets = []
    
    # Initialize the progress counter
    tot = len(data)
    counter = 0
    
    
    for tweet in data:
        
        # Cleans the Tweet and turns it back into a string
        text, vocab = clean_tweet(tweet, vocab)
        cleaned_tweets.append(" ".join(text))
        
        # This part is so the user doesn't get bored
        counter += 1
        if (len(cleaned_tweets)%10000) == 0:
            print(counter, "of", tot, "Tweets cleaned")
            
    print(tot, "of", tot, "Tweets cleaned")
        
    if gen_vocab:
        # Generate the vocabulary
        vocab_fin=['<UNK>']
        for key in vocab.keys():
            # If a word has a lower occurrence than the given threshold,
            # it is considered to be oov.
            if vocab[key]>=threshold:
                vocab_fin.append(key)
        
    return cleaned_tweets, vocab_fin



def preprocessor(data, vocab=None):
    """
    
    Input:  an iterable that gives out Tweets as strings and a dictionary
    containing our vocabulary.
    
    Output: a list of all the preprocessed Tweets
    
    """
    
    # If no vocabulary is given, it generates one from the data
    if vocab is None:
        data, vocab = cleaner(data, 10)
        
    # Initialize the list of preprocessed Tweets and the progress counter
    preprocessed = []
    tot = len(data)
    counter = 0
    
    
    for tweet in data:
        
        # Preprocess the Tweet
        new_tweet = " ".join(preprocess_tweet(tweet, vocab))
        preprocessed.append(new_tweet)
        
        # This part is so the user doesn't get bored
        counter += 1
        if (counter%1000) == 0:
            print(counter, "of", tot, "Tweets processed")
      
    print(tot, "of", tot, "Tweets processed")
    
    return preprocessed

#############################




def preprocess_file(origin_path, save_path, file_type, column="text", vocab=None):
    """
    This program assumes that your input file contains only one tweet per line
    """
    
    print("Importing data...")
    
    if file_type == "txt":
        
        if origin_path[-3:] == "tsv":
            df = pd.read_csv(origin_path, header=None, index_col=False, sep="\t")
            ff = df.iloc[:,0].to_list()
            
        elif origin_path[-3:] == "csv":
            df = pd.read_csv(origin_path, header=None, index_col=False)
            ff = df.iloc[:,0].to_list()
            
        else:
            ff = open(origin_path,'r', encoding="utf8").readlines()
            
    elif file_type == "DataFrame":
        df = pd.read_csv(origin_path)
        ff = df[column]
        
    else:
        print("File type has to be 'txt' or 'DataFrame'")
        return None
    
    
    print("\nCleaning data...")
    if vocab is None:
        data, vocab = cleaner(ff)
        print("\nVocabulary generated")
    else:
        data, _ = cleaner(ff, gen_vocab=False)
        
    print("")
    print(len(vocab), "words in the vocabulary")
        
    print("\nPreprocessing data...")
    preprocessed = preprocessor(data, vocab)
    
    print("\nSaving data...")
    
    if file_type == "txt":
        gg = open(save_path,'w', encoding="utf8")
        for tweet in preprocessed:
            gg.write(tweet+'\n')
        gg.close()
    
    elif file_type == "DataFrame":
        df[column] = pd.Series(preprocessed)
        df.to_csv(save_path)
    
    print("Data successfully saved!")
    
    print("\n\n")
    
    return vocab