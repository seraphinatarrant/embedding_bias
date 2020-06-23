#!/usr/bin/env bash

# set it to fail at first error
set -o errexit

# source my bashrc
source ~/.bashrc
# activate the project environment
conda activate bias_env
# set up my student id variable
export STUDENT_ID=${whoami}

rsync -av /home/${STUDENT_ID}/data/enwiki-latest-pages-articles_preprocessed.txt /disk/scratch/${STUDENT_ID}/wiki_data_preprocessed.txt

python /home/${STUDENT_ID}/git2/embedding_bias/data_cleaning/final_preprocess.py /disk/scratch/${STUDENT_ID}/wiki_data_preprocessed.txt

rsync -av /disk/scratch/${STUDENT_ID}/wiki_data_preprocessed_final.txt /home/${STUDENT_ID}/data/enwiki-latest-pages-articles_preprocessed_final.txt

rm /disk/scratch/${STUDENT_ID}/wiki_data_preprocessed_final.txt
