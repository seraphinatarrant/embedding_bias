#!/usr/bin/env bash

# set to fail at first error
set -o errexit

# source my bashrc
source ~/.bashrc
# activate allennlp environment
conda activate allennlp

rm -rf /disk/scratch/s1303513/d8

mkdir -p /disk/scratch/s1303513/d8
mkdir -p /disk/scratch/s1303513/d8/train
mkdir -p /disk/scratch/s1303513/d8/test
mkdir -p /disk/scratch/s1303513/d8/dev

echo Copying data to scratch space
# Copy train, test, and dev data from headnode to scratch space
rsync -av ./allennlp/data/train/train.english.v4_gold_conll /disk/scratch/s1303513/d8/train/train.english.v4_gold_conll
rsync -av ./allennlp/data/test/test.english.v4_gold_conll /disk/scratch/s1303513/d8/test/test.english.v4_gold_conll
rsync -av ./allennlp/data/dev/dev.english.v4_gold_conll /disk/scratch/s1303513/d8/dev/dev.english.v4_gold_conll

rsync -av ./embeddings/w2v/db_vectors/db_d_8_w2v_gl.txt /disk/scratch/s1303513/d8/db_d_8_w2v_gl.txt

export COREF_TRAIN_DATA_PATH=/disk/scratch/s1303513/d8/train/train.english.v4_gold_conll
export COREF_TEST_DATA_PATH=/disk/scratch/s1303513/d8/test/test.english.v4_gold_conll
export COREF_DEV_DATA_PATH=/disk/scratch/s1303513/d8/dev/dev.english.v4_gold_conll

echo Training coreference model
allennlp train ./git2/embedding_bias/coref/coref_config_file_t5 -s /disk/scratch/s1303513/d8/results_d8_w2v
echo Copying model files back to headnode
rsync -av /disk/scratch/s1303513/d8/results_* ./
echo Deleting data and results from scratch space
rm -r /disk/scratch/s1303513/d8/
