from gensim import utils
import gensim.models
import sys



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
    sentences=MyIter()
    model = gensim.models.Word2Vec(size=300, window=5, min_count=5, sg=1)
    print('Building the vocabulary')
    model.build_vocab(sentences=sentences)
    total_examples = model.corpus_count
    print('Training the model')
    model.train(sentences=sentences, total_examples=total_examples, epochs=model.epochs, total_words=model.corpus_total_words)

    print('Saving model to specified filepath')
    save_file = sys.argv[2]
    model.wv.save_word2vec_format(save_file)



if __name__ == '__main__':
    main()
