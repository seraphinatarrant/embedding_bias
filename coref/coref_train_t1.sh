#!/usr/bin/env bash

# set to fail at first error
set -o errexit

# source my bashrc
source ~/.bashrc
# activate allennlp environment
conda activate allennlp

rm -r /disk/scratch/s1303513/corefcheck/results_ft_ar_t1_check

mkdir -p /disk/scratch/s1303513/corefcheck
mkdir -p /disk/scratch/s1303513/corefcheck/train
mkdir -p /disk/scratch/s1303513/corefcheck/test
mkdir -p /disk/scratch/s1303513/corefcheck/dev

echo Copying data to scratch space
# Copy train, test, and dev data from headnode to scratch space
rsync -av ./allennlp/data/train/train.english.v4_gold_conll /disk/scratch/s1303513/corefcheck/train/train.english.v4_gold_conll
rsync -av ./allennlp/data/test/test.english.v4_gold_conll /disk/scratch/s1303513/corefcheck/test/test.english.v4_gold_conll
rsync -av ./allennlp/data/dev/dev.english.v4_gold_conll /disk/scratch/s1303513/corefcheck/dev/dev.english.v4_gold_conll

rsync -av ./embeddings/ft/ar_vectors/ft_ar_t1_check_vectors.txt /disk/scratch/s1303513/corefcheck/ft_ar_t1_check_vectors.txt

export COREF_TRAIN_DATA_PATH=/disk/scratch/s1303513/corefcheck/train/train.english.v4_gold_conll
export COREF_TEST_DATA_PATH=/disk/scratch/s1303513/corefcheck/test/test.english.v4_gold_conll
export COREF_DEV_DATA_PATH=/disk/scratch/s1303513/corefcheck/dev/dev.english.v4_gold_conll

echo Training coreference model
allennlp train ./git2/embedding_bias/coref/coref_config_file_t1 -s /disk/scratch/s1303513/corefcheck/results_ft_ar_t1_check

echo Copying model files back to headnode
rsync -av /disk/scratch/s1303513/corefcheck/results_* ./
echo Deleting data and results from scratch space
rm -r /disk/scratch/s1303513/corefcheck
