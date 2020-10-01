## Preface
This is an implementation of [Convolutional Neural Networks for Sentence Classification](https://arxiv.org/abs/1408.5882) by Kim. It is a modified version of Shawn1993's [code](https://github.com/Shawn1993/cnn-text-classification-pytorch) implementation on PyTorch. I added the possibility of using your own pretrained embeddings and of importing your own datasets from a CSV.

## Requirements
* python 3
* pytorch > 0.1
* torchtext > 0.1
* numpy
* nltk
* pandas
* sklearn


## Parameters

If you run the help option:
```
python3 main.py -h
```

You will get the following list of parameters

```
CNN text classificer

optional arguments:
  -h, --help            show this help message and exit
  -batch-size N         batch size for training [default: 50]
  -lr LR                initial learning rate [default: 0.01]
  -epochs N             number of epochs for train [default: 10]
  -dropout              the probability for dropout [default: 0.5]
  -max_norm MAX_NORM    l2 constraint of parameters
  -cpu                  disable the gpu
  -device DEVICE        device to use for iterate data
  -embed-dim EMBED_DIM
  -static               fix the embedding
  -kernel-sizes KERNEL_SIZES
                        Comma-separated kernel size to use for convolution
  -kernel-num KERNEL_NUM
                        number of each kind of kernel
  -class-num CLASS_NUM  number of class
  -shuffle              shuffle the data every epoch
  -num-workers NUM_WORKERS
                        how many subprocesses to use for data loading
                        [default: 0]
  -log-interval LOG_INTERVAL
                        how many batches to wait before logging training
                        status
  -test-interval TEST_INTERVAL
                        how many epochs to wait before testing
  -save-interval SAVE_INTERVAL
                        how many epochs to wait before saving
  -predict PREDICT      predict the sentence given
  -snapshot SNAPSHOT    filename of model snapshot [default: None]
  -save-dir SAVE_DIR    where to save the checkpoint
  
New Parameters
  -embeddings           filename of the word2vec format embeddings [default: None]
  -data-path            path to the dataset to use [default: None]
  -data-name            filename of the dataset to use, 'train.csv', 'dev.csv', and 'test.csv' will be added to the end of this string [default: None]
  -results-path         filename and path where the results will be saved [default: None]
  -use-half             whether to test on only half of the data [default: False]
  -first-half           half of the data to use, False for first, True for second [default: False]
````


## Train
Run `main.py` to train the model.

Parameters to use:

* Use the `embeddings` parameter to set the location of the embeddings in word2vec format.
* The `data-path` and `data-name` parameters set the location of the dataset. If not specified, you will use a preset dataset.

## Test
If you have a test set, you can run tests using `main.py` and the `test` argument.

Parameters to use:

* Use the `embeddings` parameter to set the location of the embeddings in word2vec format.
* The `data-path` and `data-name` parameters set the location of the dataset. If not specified, you will use a preset dataset.
* `snapshot` determines where the model gets loaded from and if it isn't assigned, the test will be done using only the default initiation values to very poor results.
* To save your metrics to a text file, specify the path using the `results-path` part of the dataset.
* If for some reason you want to only use half of the dataset, set `use-half` to true. Then set `first-half` to true if using the first half or ommit it otherwise.

## Predict
If you want to predict a sentence, pass the parameter `predict` with its value being the phrase you want it to predict.

Parameters to use:

* Use the `embeddings` parameter to set the location of the embeddings in word2vec format.
* The `data-path` and `data-name` parameters set the location of the dataset. If not specified, you will use a preset dataset.
* `snapshot` determines where the model gets loaded from and if it isn't assigned, the test will be done using only the default initiation values to very poor results.