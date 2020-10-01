This is the code for my dissertation project, "Exploring the Relationship Between Intrinsic and Extrinsic Bias in Spanish Word Embeddings". This document and the project proposal can be found in `./documents`.


## Prerequisites

In order to run the experiments I used for my project, you need:

* Tweets extracted from the Twitter API. There are some mirrors in [archive.org](https://archive.org/details/archiveteam-twitter-stream-2019-03).
	* These should go into the `./data/archive/[DATE]` path.
	* If you use data from any other month, you might have to modify some of the preprocessing scripts, unless you save it in the wrong path.
* A hate speech classification dataset. My code assumes that you are using the [HatEval](http://hatespeechdata.com/competitions.codalab.org/competitions/19935) dataset, but you can find many more at the [hatespeechdata](http://hatespeechdata.com/) list.
	* If you use any other dataset, you might have to modify some of the preprocessing scripts.
	* If the dataset has different tags, you should probably remove any reference to the `./scripts/cnn2` path in any of the scripts executed.
	* I tested my code with binary classification. I'm pretty sure it works with more classes, but I would recommend you to check [Mugdha's version of the code](https://github.com/seraphinatarrant/embedding_bias/tree/Mugdha) in that case. 
* For some parts of the code you _will_ need a GPU. More specifically, the extinsic metric.

Finally, the environment you are using needs to have these packages:

**TODO**


## Preparing the data

Before running any of the scripts, make sure you have the data in the correct paths. Then use the notebooks in `./scripts/data_cleaning/`. These are numbered and have instructions on how to run them.


## Running the MSc experiments

To run my experiments, you only need to use the `run_msc.sh` script after having prepared the data. Due to some issues that I had with the environments, they'll assume that your current environment is called **NAME** and has pytorch and gensim installed and that you have an environment called `tf-gpu-cuda8` which has tensorflow installed. This isn't ideal, I know, but that's how I had to do it back then.


## Running new experiments

This will be done through the `run.sh` script. **TODO**


## Citing

If you use this code, cite **TODO**.

You should also probably cite the data you are using and the people whose code this was based on. Note that many of these were modified for this project. Most of these changes are commented on the code:

* [Preprocessing script](https://github.com/seraphinatarrant/embedding_bias/tree/Mugdha) by Mugdha Pandya.
* [XWEAT](https://github.com/anlausch/XWEAT) by Anne Lauscher and Goran Glavaš.
* [Attract-repel](https://github.com/nmrksic/attract-repel) by Mile Mrkšić. The version used here was [updated](https://github.com/seraphinatarrant/embedding_bias/tree/Rebecca) to work in Python 3 by Rebecca Marchant.
* The CNN proposed by Yoon Kim. The particular [implementation](https://github.com/Shawn1993/cnn-text-classification-pytorch) we used was the one by github user Shawn1993.
	* Note that the code in `./scripts/CNN/` is a modified version where you can load pretrained embeddings in word2vec format and with a special data loader.
	* The code in `./scripts/CNN/` is a heavily modified version designed for subtask B of the HatEval classification task. Be careful if using this.