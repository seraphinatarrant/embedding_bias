#!/usr/bin/python
# encoding=utf8

from collections import Counter
from itertools import chain
from nltk import tokenize
import sys


def count_in_file(filename):
    with open(filename, 'r', encoding='UTF8') as f:
        linewords = (line.split() for line in f)
        return dict(Counter(chain.from_iterable(linewords)))


def get_lowfreq_words(preprocessed_data):
    # with open(preprocessed_data) as f:
    lowfreq_set = set()
        # freq_dict = dict(Counter(tokenize.word_tokenize(f.read(), 'english', False)))
    freq_dict = count_in_file(preprocessed_data)
    for word in freq_dict.keys():
        if freq_dict[word] <= 10:
            lowfreq_set.add(word)

    return lowfreq_set


def add_unk_tokens(preprocessed_data):
    file_out = '{}_final.txt'.format(str(preprocessed_data)[:-4])
    print('Creating low freq set')
    lowfreq_set = get_lowfreq_words(preprocessed_data)
    with open(preprocessed_data, 'r') as f:
        with open(file_out, 'w') as o_f:
            print('Writing new lines to file')
            o_f.write('<UNK> ')
            for line in f.readlines():
                tokenized_version = line.split()
                for i in range(len(tokenized_version)):
                    if tokenized_version[i] in lowfreq_set:
                        tokenized_version[i] = '<UNK>'

                o_f.write(' '.join(tokenized_version))
                o_f.write('\n')


def main():
    print('Python script running')
    add_unk_tokens(sys.argv[1])
    print('Done!')


if __name__ == '__main__':
    main()