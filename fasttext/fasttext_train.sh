#!/usr/bin/env bash

### COMMAND LINE ARGUMENTS
# $1 = path to training data (text file)
# $2 = path to folder where embeddings should be saved


# set it to fail at first error
set -o errexit

# source my bashrc
source ~/.bashrc
# activate the project environment
conda activate bias_env

echo Creating a file in scratch space
mkdir -p /disk/scratch/s1303513/fasttext_temp

echo Copying data over to scratch space
# copy data over from headnode to scratch space
rsync -av $1 /disk/scratch/s1303513/fasttext_temp/training_data.txt

echo Executing python script
python train_ft_embeddings.py /disk/scratch/s1303513/fasttext_temp/training_data.txt /disk/scratch/s1303513/fasttext_temp/ft_vectors_w2vformat.txt

echo Copying models back to headnode
rsync -av /disk/scratch/s1303513/fasttext_temp/ft_vectors_w2vformat.txt $2

echo Deleting data and model from scratch space
rm -r /disk/scratch/s1303513/fasttext_temp/*
