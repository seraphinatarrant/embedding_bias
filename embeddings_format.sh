#!/usr/bin/env bash

# $1 Name of the embeddings file
emb_name = $1

# set it to fail at first error
set -o errexit

# source my bashrc
source ~/.bashrc

# We activate the project environment
conda activate gensim

# Each experiment will have its own randomly determined path so that they don't clash with each other
RANDOM=$$
exp_path=/disk/scratch/${USER}/$RANDOM

# Set the path for the old embedding files
emb_old=../data/old_embeddings

emb_path=../data/embeddings

echo Creating a temp folder in scratch...
temp=$exp_path
mkdir -p $temp

echo Copying data to scratch space
rsync -av $emb_old/$emb_name ${emb_name}.old

# Transform the embeddings from glove format to word2vec
old_path=$temp/${emb_name}.old
new_path=$temp/$emb_name
python -m gensim.scripts.glove2word2vec --input $old_path --output $new_path

echo Copying data back to head node
rsync -av $new_path $emb_path/$emb_name

