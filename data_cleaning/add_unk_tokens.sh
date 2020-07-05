#!/usr/bin/env bash

# set it to fail at first error
set -o errexit

# source my bashrc
source ~/.bashrc
# activate the project environment
conda activate bias_env

mkdir -p /disk/scratch/s1303513

mkdir -p /disk/scratch/s1303513/token_data

echo Copying data over
rsync -av /home/s1303513/data/wiki_data_preprocessed_tok.txt /disk/scratch/s1303513/token_data/wiki_data_preprocessed_tok.txt

echo Executing python script

python /home/s1303513/git2/embedding_bias/data_cleaning/general_preprocessing.py /disk/scratch/s1303513/token_data/ --unk [UNK] --threshold 10

echo Copying data back to home

rsync -av /disk/scratch/s1303513/token_data/wiki_data_preprocessed_tok.txt /home/s1303513/data/wiki_data_final.txt

echo Removing data from scratch space

rm -r /disk/scratch/s1303513/token_data/
