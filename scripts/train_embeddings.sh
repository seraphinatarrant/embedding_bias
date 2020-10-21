#!/usr/bin/env bash

# $1 is the path to the training data
# $2 is the path to the embeddings

# set to fail at first error
set -o errexit

# source activate
source ~/.bashrc

# activate the project environment
conda activate gensim

echo Creating a file in scratch space...
mkdir -p /disk/scratch/v1rmuoz/embedding_temp

echo Copying data over to scratch space
# copy data over from headnode to scratch space
rsync -av $1 /disk/scratch/v1rmarc5/fasttext_temp/training_data.txt
