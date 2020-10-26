#!/usr/bin/env bash

# $1 path to the folder containing the training data
# $2 path to the embeddings
# $3 embedding file name
# $4 name for the experiment
# $5 path where the results wll be stored
# $6 is the path to a particular experiment

training_head=$1
embeddings_head=$2
emb_name=$3
experiment_name=$4
results_head=$5
exp_path=$6

# set it to fail at first error
set -o errexit

# source my bashrc
source ~/.bashrc
# activate the project environment
conda activate gensim

echo Creating a temp forder in scratch
temp=$exp_path/cnn_temp
data_name="task2_es_"
data_path=$temp/data
out_path=$temp/out
emb_path=$data_path/$emb_name
mkdir -p $temp
mkdir -p $data_path
mkdir -p $out_path

echo Copying data to scratch space
rsync -av $training_head/ $data_path
rsync -av $embeddings_head/ $data_path
ls $data_path

# Setting the results files
name="task2_${experiment_name}"
results_path=$out_path/${name}.txt
results_g1=$out_path/${name}_g1.txt
results_g2=$out_path/${name}_g2.txt

# We train the CNN
# ISSUE: the model is *not* saved on scratch!
echo Training CNN
python ./cnn2/main.py \
	-embeddings=$emb_path \
	-data-path=$data_path/ \
	-data-name=$data_name \
	-label="HS"
python ./cnn2/main.py \
	-embeddings=$emb_path \
	-data-path=$data_path/ \
	-data-name=$data_name \
	-label="TR"
python ./cnn2/main.py \
	-embeddings=$emb_path \
	-data-path=$data_path/ \
	-data-name=$data_name \
	-label="AG"

# We evaluate on the whole dataset
echo Evaluating
python ./cnn2/main.py \
	-test \
	-embeddings=$emb_path \
	-data-path=$data_path/ \
	-data-name=$data_name \
	-results-path=$results_path \
	-snapshot="./cnn/snapshot/best_steps_model" \
	-label="HS"

# We evaluate on group 1
echo Evaluating on group 1
python ./cnn2/main.py \
	-test \
	-embeddings=$emb_path \
	-data-path=$data_path/ \
	-data-name=$data_name \
	-results-path=$results_g1 \
	-snapshot="./cnn/snapshot/best_steps_model" \
	-use-half=True \
	-first-half=True \
	-label="HS"

# We evaluate on group 2
echo Evaluationg on group 2
python ./cnn2/main.py \
	-test \
	-embeddings=$emb_path \
	-data-path=$data_path/ \
	-data-name=$data_name \
	-results-path=$results_g2 \
	-snapshot="./cnn/snapshot/best_steps_model" \
	-use-half=True \
	-label="HS"

echo Copying results to the headnode
rsync -av $out_path/ $results_head

echo Deleting data from scratch space
rm -r $temp/*
