#!/usr/bin/env bash

# set to fail at first error
set -o errexit

# source my bashrc
source ~/.bashrc
# activate allennlp environment
conda activate allennlp

mkdir -p /disk/scratch/s1303513

echo Copying data to scratch space
# Copy train, test, and dev data from headnode to scratch space
rsync -av ./allennlp/data/train/train.english.v4_gold_conll /disk/scratch/s1303513/train/train.english.v4_gold_conll
rsync -av ./allennlp/data/test/test.english.v4_gold_conll /disk/scratch/s1303513/test/test.english.v4_gold_conll
rsync -av ./allennlp/data/dev/dev.english.v4_gold_conll /disk/scratch/s1303513/dev/dev.english.v4_gold_conll

export COREF_TRAIN_DATA_PATH=/disk/scratch/s1303513/train/train.english.v4_gold_conll
export COREF_TEST_DATA_PATH=/disk/scratch/s1303513/test/test.english.v4_gold_conll
export COREF_DEV_DATA_PATH=/disk/scratch/s1303513/dev/dev.english.v4_gold_conll

echo Training coreference model
allennlp train ./allennlp/allennlp-models/training_config/coref/coref.jsonnet -s /disk/scratch/s1303513/results_$(date '+%d%m-%H%M')

echo Copying model files back to headnode
rsync -av /disk/scratch/s1303513/results_* ./allennlp/results/
echo deleting data and results from scratch space
rm -r /disk/scratch/s1303513/