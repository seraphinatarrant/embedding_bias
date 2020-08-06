#!/usr/bin/env bash

# set it to fail at first error
set -o errexit

# source my bashrc
source ~/.bashrc
# activate the project environment
conda activate bias_env

mkdir -p /disk/scratch/s1303513/ft_d6

echo Copying data over to scratch space
# copy data over from headnode to scratch space
rsync -av ./db_data/db_debias_data_6.txt /disk/scratch/s1303513/ft_d6/db_debias_data_6.txt

echo Executing python script
python ./git2/embedding_bias/fasttext/train_ft_embeddings.py /disk/scratch/s1303513/ft_d6/db_debias_data_6.txt /disk/scratch/s1303513/ft_d6/ft_d_6_w2v.txt


echo Copying models back to headnode
rsync -av /disk/scratch/s1303513/ft_d6/ft_d_6_w2v.txt ./embeddings/ft/db_vectors/

echo Deleting data and model from scratch space
rm -r /disk/scratch/s1303513/ft_d6/*
