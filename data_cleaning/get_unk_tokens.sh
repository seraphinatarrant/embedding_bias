#!/usr/bin/env bash

# set it to fail at first error
set -o errexit

# source my bashrc
source ~/.bashrc
# activate the project environment
conda activate bias_env

mkdir -p /disk/scratch/s1303513
echo Copying data over
rsync -av /home/s1303513/data/enwiki-latest-pages-articles_preprocessed.txt /disk/scratch/s1303513/wiki_data_preprocessed.txt
echo Executing python script
python /home/s1303513/git2/embedding_bias/data_cleaning/final_preprocess.py /disk/scratch/s1303513/wiki_data_preprocessed.txt
echo Copying final data back
rsync -av /disk/scratch/s1303513/wiki_data_preprocessed_final.txt /home/s1303513/data/enwiki-latest-pages-articles_preprocessed_final.txt
echo Deleting data from scratch space
rm /disk/scratch/s1303513/wiki_data_preprocessed_final.txt
rm /disk/scratch/s1303513/wiki_data_preprocessed.txt
