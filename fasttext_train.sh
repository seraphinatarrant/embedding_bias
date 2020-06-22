#!/usr/bin/env bash

# set it to fail at first error
set -o errexit

# source my bashrc
source ~/.bashrc
# activate the project environment
conda activate bias_env
# set up my student id variable
export STUDENT_ID=${whoami}

# copy data over from headnode to scratch space
rsync -avzh ./data/enwiki-latest-pages-articles_preprocessed.txt /disk/scratch/${STUDENT_ID}/wiki_data_preprocessed.txt

python train_ft_embeddings.py /disk/scratch/${STUDENT_ID}/wiki_data_preprocessed.txt /disk/scratch/${STUDENT_ID}/fasttext.model

mkdir ./models

rsync -avzh /disk/scratch/${STUDENT_ID}/fasttext.model ./models/fasttext.model

rm /disk/scratch/${STUDENT_ID}/fasttext.model
