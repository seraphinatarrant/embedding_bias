from gensim.models.fasttext import FastText as FT_gensim
from gensim import utils
import tempfile
import sys


## Construct an iterator to iterate over lines in the data and yield just one line at a time
## Data passed in as first command line argument
class MyIter(object):
    """
    An iterator that yields documents (where corpus contains one document per line). Yields lists of str.
    """
    def __iter__(self):
        path = sys.argv[1]
        with utils.open(path, 'r', encoding='utf-8') as fin:
            for line in fin:
                yield line.split()


def main():
    print('Instantiating the model')
    # instantiate the skipgram model
    model = FT_gensim(size=300, window=5, min_count=5, sg=1)
    print('Building the vocabulary')
    # build the vocabulary from the sentences yielded by the iterator
    model.build_vocab(sentences=MyIter())
    total_examples = model.corpus_count
    print('Training the model')
    # train the model
    model.train(sentences=MyIter(), total_examples=total_examples, epochs=model.epochs, total_words=model.corpus_total_words)

    ## Save file passed in as second argument
    print('Saving the model to specified filepath')
    save_file = sys.argv[2]
    # model saved in the w2v format, i.e. the first line contains <no. of words> <no. of dimensions>
    model.wv.save_word2vec_format(save_file)


if __name__ == '__main__':
    main()
