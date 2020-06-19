from gensim.models.fasttext import FastText as FT_gensim
from gensim import utils
import re
import sys

## Construct an iterator to iterate over lines in the data
## Data passed in as first argument

class MyIter(object):
    def __iter__(self):
        path = sys.argv[1]
        with utils.open(path, 'r', encoding='utf-8') as fin:
            for line in fin:
                line = line.lower()
                line = re.sub(r'—', ' ', line)
                line = re.sub(r'[^[\w\s\']', '', line)
                # print(line.split())
                yield line.split()

## Train the model

def main():
    print('Instantiating the model')
    model = FT_gensim(size=4, window=3, min_count=1)  # instantiate the model
    print('Building the vocabulary')
    model.build_vocab(sentences=MyIter())
    total_examples = model.corpus_count
    print('Training the model')
    model.train(sentences=MyIter(), total_examples=total_examples, epochs=10)  # train the model

    ## Save the model (can be loaded using gensim)
    print('Saving the model to specified filepath')
    save_file = sys.argv[2]
    model.save(save_file)


if __name__ == '__main__':
    main()
