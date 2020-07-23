from gensim.scripts.glove2word2vec import glove2word2vec
import sys

if __name__ == "__main__":
    # first argument is input file in glove format
    # second argument is output file in w2v format
    glove2word2vec(sys.argv[1], sys.argv[2])