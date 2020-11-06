#!/usr/bin/env bash

### COMMAND LINE ARGUMENTS
# $1 = path to training data (text file)
# $2 = path to file where embeddings should be saved (text file)

export STUDENT_ID=$(whoami)

# set it to fail at first error
set -o errexit

# source my bashrc
source ~/.bashrc
# activate the project environment (change this where necessary)
conda activate bias_env2

echo Creating a folder in scratch space
mkdir -p /disk/scratch/${STUDENT_ID}/fasttext_temp

echo Copying data over to scratch space
# copy data over from headnode to scratch space
rsync -av $1 /disk/scratch/${STUDENT_ID}/fasttext_temp/training_data.txt

echo Executing python script
python fasttext/train_ft_embeddings.py /disk/scratch/${STUDENT_ID}/fasttext_temp/training_data.txt /disk/scratch/${STUDENT_ID}/fasttext_temp/ft_vectors_w2vformat.txt

echo Copying models back to headnode
rsync -av /disk/scratch/${STUDENT_ID}/fasttext_temp/ft_vectors_w2vformat.txt $2

echo Deleting data and model from scratch space
rm -r /disk/scratch/${STUDENT_ID}/fasttext_temp/
