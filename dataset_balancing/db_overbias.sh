#!/usr/bin/env bash

# set to fail at first error
set -o errexit

# source my bashrc
source ~/.bashrc

conda activate bias_env

mkdir -p /disk/scratch/s1303513/overbias

echo Copying data to scratch space

rsync -av ./data/wiki_new_final_copy.txt /disk/scratch/s1303513/overbias/wiki_new_final_copy.txt

echo Executing python script

python ./git2/embedding_bias/dataset_balancing/db_overbias.py /disk/scratch/s1303513/overbias/wiki_new_final_copy.txt /disk/scratch/s1303513/overbias/db_overbias_data_7.txt 7

echo Copying data back to home directory

rsync -av /disk/scratch/s1303513/overbias/db_overbias_data_7.txt ./db_overbias_data_7.txt

echo Executing python script

python ./git2/embedding_bias/dataset_balancing/db_overbias.py /disk/scratch/s1303513/overbias/wiki_new_final_copy.txt /disk/scratch/s1303513/overbias/db_overbias_data_8.txt 8

echo Copying data back to home directory

rsync -av /disk/scratch/s1303513/overbias/db_overbias_data_8.txt ./db_overbias_data_8.txt

rm /disk/scratch/s1303513/overbias/*
