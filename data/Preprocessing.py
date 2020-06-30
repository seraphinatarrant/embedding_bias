# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 16:14:41 2020

@author: Rimusa
"""

import re
import ast

import pandas as pd


###############################################################################


def tokenize(text, lowercase=True):
    
    """
    
    This is based on the code from Marco Bozanini's blog:
        https://marcobonzanini.com/2015/03/09/mining-twitter-data-with-python-part-2/
        
    It takes a Tweet in string format as an input and returns a tokenized
    version of it (i.e. a list of tokens).
    
    It lowercases everything and:
        
        1) Keeps certain kinds of emoticons together
        2) Keeps HTML tags as-is. I don't think that any twitter data from the
           API still has these, so I won't pre-process them.
        3) Keeps mentions and hasthags together with their respective symbol
        4) Takes accents into account, even those not within the language. For
           reference, the letters that can carry accents in Spanish are:
               á  é  í  ó  ú  ñ  ü
        5) Keeps multi-digit numbers together, along with their decimal values
        6) Keeps words that have - and ' together. Note that these are almost
           non-existent in Spanish, but are extremely important for English.
           
    """
    

    # Determine how emoticons can be made
    emoticons_str = r"""
        (?:
            [:=;] # Eyes
            [oO\-]? # Nose (optional)
            [D\)\]\(\]/\\OpP] # Mouth
        )"""

    # Determine the things that we will consider words
    regex_str = [
        emoticons_str,
        r'<[^>]+>', # HTML tags
        r'(?:@[\w_]+)', # @-mentions
        r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
        r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs

        r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
        r"(?:[a-zÀ-ÿ][a-zÀ-ÿ'\-_]+[a-zÀ-ÿ])", # words with - and '
        r'(?:[\w_]+)', # other words
        r'(?:\S)' # anything else
    ]

    # Compile the regular expressions
    tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
    emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

    
    # Lowercase and tokenize the text    
    new_text = tokens_re.findall(text)
    if lowercase:
        new_text = [token if emoticon_re.search(token) 
                          else token.lower()
                                                      for token in new_text]
    
        
    return new_text


###############################################################################


def preprocess(corpus, vocab,
               bos=True, eos=True,
               remove_mentions=False, remove_url=False,
               remove_hashtags=False, hashtag_token=True):
    """
    
    This function takes a list of strings (Tweets) and a vocabulary (any
    iterable where the item taken is the word) and preprocesses it according to
    various Boolean parameters. These are:
        
        bos
            Determines whether a <BOS> tag will be added at the beginning of
            each Tweet.
        
        eos
            Determines whether a <EOS> tag will be added at the end of each
            Tweet.
            
        remove_mentions
            If True, it will remove any token that begins with @. If False, it
            will add a <USR> tag in its place.
            
        remove_url
            If True, it will remove any url in the Tweet. If False, it will add
            a <URL> tag in its place.
            
        remove_hashtags
            If True, it will remove any token that begins with #. If false, the
            behavior will depend on the hashtag_token parameter.
            
        hashtag_token
            If True, it will add a <TAG> tag in place of any token that begins
            with #. If false, it will just remove the # from that token. This
            parameter is only relevant if remove_hashtags is False.
    
    Furthermore, this function removes line breaks and excessive spacing, while
    substituting any token that isn't in the vocabulary and in hasn't been
    substituted yet with an <UNK> tag.
    
    """
    
    # We tokenize the Tweets
    tokenized_tweets = list(map(tokenize,corpus))
    
    # Initialize a list for the preprocessed Tweets
    preprocessed_data = []
    
    # Initialize a counter so that the user doesn't get bored
    counter = 0
    print(counter,"of",len(tokenized_tweets),"Tweets processed...")
    
    # This will remove extra spaces
    space_pattern = "\s+"
        
    
    for tweet in tokenized_tweets:
        
        # Initialize the preprocessed Tweet
        new = []
        
        # Add <BOS> tag if given the argument
        if bos:
            new.append("<BOS>")
            
            
        for token in tweet:
            
            # Add <USR> tag if given the argument, otherwise, remove mentions
            if token[0] == "@":
                if remove_mentions:
                    continue
                else:
                    new.append("<USR>")
                    
            # Either add <TAG>, remove the # symbol or remove hashtags altogether
            elif token[0] == "#":
                if remove_hashtags:
                    continue
                elif hashtag_token:
                    new.append("<TAG>")
                elif len(token > 1):
                    new.append(token[1:])
                else:
                    continue
            
            # Add <URL> tag if given the argument, otherwise, remove urls
            elif token[0:4] == "http":
                if remove_url:
                    continue
                else:
                    new.append("<URL>")
                    
            # Remove linebreaks
            elif token == "\n":
                continue
                
            # Change " to ' (for data storage reasons)
            elif token == "\"":
                new.append("\'")
                    
            # Remove tokens not in the vocabulary
            else:
                if token in vocab:
                    new.append(token)
                else:
                    new.append("<UNK>")
                    
        # Add <EOS> tag if given the argument
        if eos:
            new.append("<EOS>")
         
        # Join the tokens
        new = " ".join(new)
        new = re.sub(space_pattern, " ", new)
        preprocessed_data.append(new)
        
        # This is so that the user does not get bored while the thing runs
        counter += 1
        if (counter % 10000) == 0:
            print(counter,"of",len(tokenized_tweets)," Tweets processed...")
    
    # This is so that the user does not get bored while the thing runs
    if (counter % 10000) != 0:
        print(len(tokenized_tweets),"of",len(tokenized_tweets),"Tweets processed...")
        
    return preprocessed_data


###############################################################################
    

def fetch_longtweet(df, size=-1):
    """
    
    Input: a dataframe obtained from raw twitter data
    
    Output: the unabbreviated twitter text both as a pandas Series
    
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


###############################################################################
    

def generate_vocab(text_tweets, threshold=10):
    """
    
    This generates a vocabulary from a list or pandas Series of Tweets. Then
    removes any element that appears less than the set threshold.
    
    """

    # Tokenize the Tweets
    tokenized_tweets = list(map(tokenize,text_tweets))
    
    # Initialize the vocabulary
    vocab = {}
    
    # Increment each token by 1 for each time it appears
    for line in tokenized_tweets:
        for word in line:
            if word in vocab.keys():
                vocab[word] += 1
            else:
                vocab[word] = 1
                
    keys = list(vocab.keys())
    
    # Remove keys that appear less than the fixed threshold
    for key in keys:
        if vocab[key] <= threshold:
            del vocab[key]
    
    return vocab