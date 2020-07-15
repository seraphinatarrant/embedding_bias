from gensim.models.fasttext import FastText as FT_gensim
import argparse
import sys

# Load gensim fasttext model
model = FT_gensim.load(sys.argv[1])
# save model in word2vec format
model.wv.save_word2vec_format(sys.argv[2])

