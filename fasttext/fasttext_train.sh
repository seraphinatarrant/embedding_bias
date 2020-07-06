#!/usr/bin/env bash

# set it to fail at first error
set -o errexit

# source my bashrc
source ~/.bashrc
# activate the project environment
conda activate bias_env

mkdir -p /disk/scratch/s1303513

# copy data over from headnode to scratch space
rsync -av ./data/wiki_data_final.txt /disk/scratch/s1303513/wiki_data_final.txt

python train_ft_embeddings.py /disk/scratch/s1303513/wiki_data_final.txt /disk/scratch/s1303513/fasttext.model

mkdir ./models

rsync -av /disk/scratch/s1303513/ ./models/

rm -r /disk/scratch/s1303513/
