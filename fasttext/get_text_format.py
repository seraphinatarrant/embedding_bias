"""
Script to take a gensim fasttext model and return a text file with a word on each line followed by its embedding.
"""
from gensim.models.fasttext import FastText as FT_gensim
import sys


# pass the model in as first argument
model = FT_gensim.load(sys.argv[1])

# pass vocab file as second argument
vec_file = sys.argv[2]

with open(vec_file, 'w') as out_file:
    for token in model.wv.vocab.keys():
        out_file.write(token)
        out_file.write(' ')
        for dim_val in model.wv[token]:
            out_file.write(str(dim_val))
            out_file.write(' ')

        out_file.write('\n')
