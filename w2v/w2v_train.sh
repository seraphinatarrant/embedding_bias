#!/usr/bin/env bash

# set it to fail at first error
set -o errexit

# source my bashrc
source ~/.bashrc
# activate the project environment
conda activate bias_env

mkdir -p /disk/scratch/s1303513

echo Copying data over to scratch space
# copy data over from headnode to scratch space
rsync -av ./data/wiki_new_final.txt /disk/scratch/s1303513/wiki_new_final.txt

echo Executing python script
python ./git2/embedding_bias/w2v/train_w2v_embeddings.py /disk/scratch/s1303513/wiki_new_final.txt /disk/scratch/s1303513/w2v_vectors.txt

mkdir -p embeddings/w2v

echo Copying models back to headnode
rsync -av /disk/scratch/s1303513/w2v_vectors.txt ./embeddings/w2v/

echo Deleting data and model from scratch space
rm -r /disk/scratch/s1303513/*
