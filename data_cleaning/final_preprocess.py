from collections import Counter
from nltk import tokenize
import sys


def get_lowfreq_words(preprocessed_data):
    with open(preprocessed_data) as f:
        lowfreq_set = set()
        freq_dict = dict(Counter(tokenize.word_tokenize(f.read(), 'english', False)))
        for word in freq_dict.keys():
            if freq_dict[word] <= 2:
                lowfreq_set.add(word)

    return lowfreq_set



def add_unk_tokens(preprocessed_data):
    file_out = '{}_final.txt'.format(str(preprocessed_data)[:-4])
    with open(preprocessed_data, 'r') as f:
        with open(file_out, 'w') as o_f:
            o_f.write('<UNK> ')
            for line in f.readlines():
                tokenized_version = list(tokenize.word_tokenize(line, 'english', False))
                for i in range(len(tokenized_version)):
                    if tokenized_version[i] in get_lowfreq_words(preprocessed_data):
                        tokenized_version[i] = '<UNK>'

                o_f.write(' '.join(tokenized_version))
                o_f.write('\n')


def main():
    print('Getting unk tokens for {}'.format(sys.argv[1]))
    add_unk_tokens(sys.argv[1])


if __name__ == '__main__':
    main()
