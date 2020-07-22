#!/usr/bin/env bash

# set it to fail at first error
set -o errexit

# source my bashrc
source ~/.bashrc
# activate the project environment
conda activate bias_env

echo Creating directories

mkdir -p /disk/scratch/s1303513

echo Copying data over
rsync -av /home/s1303513/data/wiki_new_tok.txt /disk/scratch/s1303513/wiki_new_tok.txt

echo Executing python script

python /home/s1303513/git2/embedding_bias/data_cleaning/final_preprocess.py /disk/scratch/s1303513/wiki_new_tok.txt

echo Copying data back to home

rsync -av /disk/scratch/s1303513/token_data/wiki_new_tok_final.txt /home/s1303513/data/wiki_new_final.txt

echo Removing data from scratch space

rm -r /disk/scratch/s1303513/*q
