#!/usr/bin/env bash

# set to fail at first error
set -o errexit

# source my bashrc
source ~/.bashrc
# activate allennlp environment
conda activate allennlp

rm -rf /disk/scratch/s1303513/o7_ft

mkdir -p /disk/scratch/s1303513/o7_ft
mkdir -p /disk/scratch/s1303513/o7_ft/train
mkdir -p /disk/scratch/s1303513/o7_ft/test
mkdir -p /disk/scratch/s1303513/o7_ft/dev

echo Copying data to scratch space
# Copy train, test, and dev data from headnode to scratch space
rsync -av ./allennlp/data/train/train.english.v4_gold_conll /disk/scratch/s1303513/o7_ft/train/train.english.v4_gold_conll
rsync -av ./allennlp/data/test/test.english.v4_gold_conll /disk/scratch/s1303513/o7_ft/test/test.english.v4_gold_conll
rsync -av ./allennlp/data/dev/dev.english.v4_gold_conll /disk/scratch/s1303513/o7_ft/dev/dev.english.v4_gold_conll

rsync -av ./embeddings/ft/db_vectors/ft_o_7_gl.txt /disk/scratch/s1303513/o7_ft/ft_o_7_gl.txt

export COREF_TRAIN_DATA_PATH=/disk/scratch/s1303513/o7_ft/train/train.english.v4_gold_conll
export COREF_TEST_DATA_PATH=/disk/scratch/s1303513/o7_ft/test/test.english.v4_gold_conll
export COREF_DEV_DATA_PATH=/disk/scratch/s1303513/o7_ft/dev/dev.english.v4_gold_conll

echo Training coreference model
allennlp train ./git2/embedding_bias/coref/coref_config_file_t4 -s /disk/scratch/s1303513/o7_ft/results_o7_ft

echo Copying model files back to headnode
rsync -av /disk/scratch/s1303513/o7_ft/results_* ./
# echo Deleting data and results from scratch space
# rm -r /disk/scratch/s1303513/
