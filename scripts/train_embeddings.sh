#!/usr/bin/env bash

# $1 is the path to the training data
# $2 is the path to the embeddings
# $3 is the kind of embedding between ft and w2v
# $4 is the path for a particular experiment

train_data=$1
embedding_head=$2
embedding_kind=$3
exp_path=$4

# set to fail at first error
set -o errexit

# source activate
source ~/.bashrc

# activate the project environment
conda activate gensim

echo Creating a temp folder in scratch space...
temp=$exp_path/$embedding_temp
emb_path=$temp/embeddings
data_path=$temp/training_data.tsv
mkdir -p $temp
mkdir -p $emb_path

echo Copying data to scratch space...
# copy data over from headnode to scratch space
rsync -av $train_data $data_path

echo Running embedding training script...
python ./embeddings/generate_embedding.py $data_path $emb_path $embedding_kind

echo Copying embeddings back to headnode...
rsync -av $emb_path/ $embedding_head

echo Deleting data from scratch space...
rm -r $temp/*

pwd
