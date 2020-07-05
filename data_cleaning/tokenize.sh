#!/usr/bin/env bash
set -o errexit

source ~/.bashrc

conda activate bias_env

mkdir -p /disk/scratch/s1303513
echo Copying data over
rsync -av /home/s1303513/data/enwiki-latest-pages-articles_preprocessed.txt /disk/scratch/s1303513/wiki_data_preprocessed.txt

echo Executing python script
python /home/s1303513/git2/embedding_bias/data_cleaning/tokenise_corpus.py /disk/scratch/s1303513/wiki_data_preprocessed.txt /disk/scratch/s1303513/wiki_data_preprocessed_tok.txt

echo Copying final data back
rsync -av /disk/scratch/s1303513/wiki_data_preprocessed_tok.txt /home/s1303513/data/wiki_data_preprocessed_tok.txt

echo Deleting from scratch space

rm /disk/scratch/s1303513/wiki_data_preprocessed_tok.txt
rm /disk/scratch/s1303513/wiki_data_preprocessed.txt
