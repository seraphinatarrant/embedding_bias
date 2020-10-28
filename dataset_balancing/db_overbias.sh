#!/usr/bin/env bash

### COMMAND LINE ARGUMENTS
# $1: original dataset
# $2: path to save file for balanced dataset

# set to fail at first error
set -o errexit

export STUDENT_ID=$(whoami)

# source my bashrc
source ~/.bashrc

conda activate bias_env

mkdir -p /disk/scratch/${STUDENT_ID}/db_overbias

echo Copying data to scratch space

rsync -av $1 /disk/scratch/${STUDENT_ID}/db_overbias/original_data.txt

echo Executing python script for WEAT test 6

python ./git2/embedding_bias/dataset_balancing/db_overbias.py /disk/scratch/${STUDENT_ID}/db_overbias/original_data.txt /disk/scratch/${STUDENT_ID}/db_overbias/db_overbias_data_6.txt 6

echo Copying WEAT 6 data back to home directory

rsync -av /disk/scratch/${STUDENT_ID}/db_overbias/db_overbias_data_6.txt $2/db_overbias_data_6.txt

echo Executing python script for WEAT test 7

python ./git2/embedding_bias/dataset_balancing/db_overbias.py /disk/scratch/${STUDENT_ID}/db_overbias/original_data.txt /disk/scratch/${STUDENT_ID}/db_overbias/db_overbias_data_7.txt 7

echo Copying WEAT 7 data back to home directory

rsync -av /disk/scratch/${STUDENT_ID}/db_overbias/db_overbias_data_7.txt $2/db_overbias_data_7.txt

echo Executing python script for WEAT test 8

python ./git2/embedding_bias/dataset_balancing/db_overbias.py /disk/scratch/${STUDENT_ID}/db_overbias/original_data.txt /disk/scratch/${STUDENT_ID}/db_overbias/db_overbias_data_8.txt 8

echo Copying WEAT 8 data back to home directory

rsync -av /disk/scratch/${STUDENT_ID}/db_overbias/db_overbias_data_8.txt $2/db_overbias_data_8.txt

rm /disk/scratch/${STUDENT_ID}/db_overbias/*
