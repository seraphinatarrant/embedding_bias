#!/usr/bin/env bash

# set it to fail at first error
set -o errexit

# source my bashrc
source ~/.bashrc
# activate the project environment
conda activate bias_env

mkdir -p /disk/scratch/s1303513

echo Copying data over
rsync -av /home/s1303513/data/half_wiki_tok.txt /disk/scratch/s1303513/half_wiki_tok.txt

echo Executing python script
python /home/s1303513/git2/embedding_bias/data_cleaning/final_preprocess.py /disk/scratch/s1303513/half_wiki_tok.txt

echo Copying final data back
rsync -av /disk/scratch/s1303513/half_wiki_tok.txt /home/s1303513/data/wiki_data_final.txt

echo Deleting data from scratch space
rm /disk/scratch/s1303513/half_wiki_tok_final.txt
rm /disk/scratch/s1303513/half_wiki_tok.txt
