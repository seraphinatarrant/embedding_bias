"""
A script to tokenise an entire corpus and write it to a text file.
Takes input corpus as first argument, out file as second argument.
"""

from nltk import tokenize
import sys


def tokenise_corpus(infile, outfile):
    with open(infile, 'r', encoding='utf-8') as infile:
        with open(outfile, 'w') as outfile:
            for line in infile:
                tok_line = tokenize.word_tokenize(line, 'english')
                outfile.write(' '.join(tok_line))
                outfile.write('\n')


if __name__ == "__main__":
    tokenise_corpus(sys.argv[1], sys.argv[2])