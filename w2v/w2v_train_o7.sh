#!/usr/bin/env bash

# set it to fail at first error
set -o errexit

# source my bashrc
source ~/.bashrc
# activate the project environment
conda activate bias_env

mkdir -p /disk/scratch/s1303513/over_7

echo Copying data over to scratch space
# copy data over from headnode to scratch space
rsync -av db_data/db_overbias_data_7.txt /disk/scratch/s1303513/over_7/db_overbias_data_7.txt

echo Executing python script
python ./git2/embedding_bias/w2v/train_w2v_embeddings.py /disk/scratch/s1303513/over_7/db_overbias_data_7.txt /disk/scratch/s1303513/over_7/db_o_7_vectors_w2v.txt


echo Copying models back to headnode
rsync -av /disk/scratch/s1303513/over_7/db_o_7_vectors_w2v.txt ./

echo Deleting data and model from scratch space
rm -r /disk/scratch/s1303513/over_7/
