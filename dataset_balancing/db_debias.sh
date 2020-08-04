#!/usr/bin/env bash

# set to fail at first error
set -o errexit

# source my bashrc
source ~/.bashrc

conda activate bias_env

mkdir -p /disk/scratch/s1303513

echo Copying data to scratch space

rsync -av ./data/wiki_new_final_copy.txt /disk/scratch/s1303513/wiki_new_final_copy.txt

echo Executing python script

python ./git2/embedding_bias/dataset_balancing/db_debias.py /disk/scratch/s1303513/wiki_new_final_copy.txt /disk/scratch/s1303513/db_debias_data_7.txt 7

echo Copying data back to home directory

rsync -av /disk/scratch/s1303513/db_debias_data_7.txt ./db_debias_data_7.txt
