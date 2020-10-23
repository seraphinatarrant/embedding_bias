#!/usr/bin/env bash

## COMMAND LINE ARGUMENTS
# $1: training data (connll format, from OntoNotes 5.0)
# $2: test data (connll format, from OntoNotes 5.0)
# $3: dev data (connll format, from OntoNotes 5.0)
# $4: word embeddings in glove format
# $5: config file
# $6: path to location where resulting model should be saved

export STUDENT_ID=$(whoami)

# set to fail at first error
set -o errexit

# source my bashrc
source ~/.bashrc
# activate allennlp environment
conda activate allennlp

mkdir -p /disk/scratch/${STUDENT_ID}/coref
mkdir -p /disk/scratch/${STUDENT_ID}/coref/train
mkdir -p /disk/scratch/${STUDENT_ID}/coref/test
mkdir -p /disk/scratch/${STUDENT_ID}/coref/dev

echo Copying data to scratch space
# Copy train, test, and dev data from headnode to scratch space

rsync -av $1 /disk/scratch/${STUDENT_ID}/coref/train/train.english.v4_gold_conll
rsync -av $2 /disk/scratch/${STUDENT_ID}/coref/test/test.english.v4_gold_conll
rsync -av $3 /disk/scratch/${STUDENT_ID}/coref/dev/dev.english.v4_gold_conll

#rsync -av ./allennlp/data/train/train.english.v4_gold_conll /disk/scratch/${STUDENT_ID}/coref/train/train.english.v4_gold_conll
#rsync -av ./allennlp/data/test/test.english.v4_gold_conll /disk/scratch/${STUDENT_ID}/coref/test/test.english.v4_gold_conll
#rsync -av ./allennlp/data/dev/dev.english.v4_gold_conll /disk/scratch/${STUDENT_ID}/coref/dev/dev.english.v4_gold_conll

rsync -av $4 /disk/scratch/${STUDENT_ID}/coref/vectors.txt

export COREF_TRAIN_DATA_PATH=/disk/scratch/${STUDENT_ID}/coref/train/train.english.v4_gold_conll
export COREF_TEST_DATA_PATH=/disk/scratch/${STUDENT_ID}/coref/test/test.english.v4_gold_conll
export COREF_DEV_DATA_PATH=/disk/scratch/${STUDENT_ID}/coref/dev/dev.english.v4_gold_conll

echo Training coreference model
allennlp train $5 -s /disk/scratch/${STUDENT_ID}/coref/results

echo Copying model files back to specified filepath
rsync -av /disk/scratch/${STUDENT_ID}/coref/results_* $6
echo Deleting data and results from scratch space
rm -r /disk/scratch/${STUDENT_ID}/coref/
