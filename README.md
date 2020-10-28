
This file outlines all the steps involved in running experiments for this project and the scripts needed for each step.

It is separated into 3 sections:
  1) Training the word embeddings
  2) Training the coreference resolution model and measuring bias in both the word embeddings and the output of the coreference resolution model
  3) Altering the word embeddings (to create new experiment conditions)

Section 1: Train word embeddings

Fasttext

Script: fasttext/fasttext_train.sh
> Input: (1) data text file, (2) path to save file for the trained embeddings
Output: trained fasttext embeddings in w2v format i.e. first line is <no. of words> <no. of dimensions>

Word2Vec

Script: w2v/w2v_train.sh
> Input: data text file, path to save file for the trained embeddings
> Output: trained fasttext embeddings in w2v format


Section 2: Train coreference resolution system and get bias metrics

Coreference resolution system (AllenNLP)

Install allennlp from source (via github) in editable mode
allennlp commit hash: 96ff585
allennlp-models commit hash: 37136f8

Script: coref/coref_train.sh
> Input: (1) Train data (2) Test data (3) Dev data (4) Word embeddings (glove format) (5) Path to save location of final model
> Output: Trained coreference resolution model


Measure WEAT

NB: if WEAT words are changed/added, they need to be changed/added within WEAT/weat.py, and the new test number can be added within WEAT/fasttext_en.sh

Script: WEAT/fasttext_en.sh
> Input: (1) Word embeddings in w2v format (2) Path to save folder for the results
> Output: WEAT score by test number for the given embeddings


Measure coreference bias
Script: coref/evaluate_allennlp.sh
> Input: (1) Trained coref model (model.tar.gz file output from allennlp train command) (2) Path to save folder for results
> Output: Evaluation metrics for the coreference resolution model on the four sets of Winobias test data


Section 3: Alter word embeddings

Attract-repel
Script: attract-repel/attract-repel.sh
The above script calls a python script which takes in a config file.
> Input (to config file) (1) original trained word embeddings (glove format) (2) text file with antonyms (3) Text file with synonyms (4) Path to save folder for the altered word embeddings
> Output: Altered word embeddings (text file)


Dataset balancing

NB: if WEAT words are changed/added, they need to be changed/added within dataset_balancing/db_debias.py and dataset_balancing/db_overbias.py

Debias script: dataset_balancing/db_debias.sh
> Input: (1) Original dataset text file (2) Path to save file for balanced (debiased) dataset
> Output: Balanced dataset (text file)

Overbias script: dataset_balancing/db_overbias.sh
> Input: (1) Original dataset text file (2) Path to save file for balanced (overbiased) dataset
> Output: Balanced dataset (text file)
