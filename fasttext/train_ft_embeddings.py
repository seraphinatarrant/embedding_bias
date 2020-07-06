from gensim.models.fasttext import FastText as FT_gensim
from gensim import utils
import tempfile
import sys


## Construct an iterator to iterate over lines in the data
## Data passed in as first argument

class MyIter(object):
    def __iter__(self):
        path = sys.argv[1]
        with utils.open(path, 'r', encoding='utf-8') as fin:
            for line in fin:
                yield line.split(' ')

## Train the model

def main():
    print('Instantiating the model')
    model = FT_gensim(size=100, window=5, min_count=5, sg=1)  # instantiate the skipgram model
    print('Building the vocabulary')
    model.build_vocab(sentences=MyIter())
    total_examples = model.corpus_count
    print('Training the model')
    model.train(sentences=MyIter(), total_examples=total_examples, epochs=model.epochs, total_words = model.corpus_total_words)  # train the model

    ## Save the model (can be loaded using gensim)
    ## Save file passed in as second argument
    print('Saving the model to specified filepath')
    save_file = sys.argv[2]
    model.save(save_file)
    # print('Saving the model')
    # with tempfile.NamedTemporaryFile(prefix='saved_model_gensim-', delete=False) as tmp:
    #     model.save(tmp.name, separately=[])


if __name__ == '__main__':
    main()
