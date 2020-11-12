#!/usr/bin/env bash

# $1 path to the folder containing the training data
# $2 path to the embeddings
# $3 embedding file name
# $4 name for the experiment
# $5 path where the results wll be stored
# $6 is the particular path for this experiment

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
data_name="task1_es_"
data_path=$temp/data
out_path=$temp/out
emb_path=$data_path/$emb_name
mkdir -p $temp
mkdir -p $data_path
mkdir -p $out_path

echo Copying data to scratch space
rsync -av $training_head/ $data_path
rsync -av $embeddings_head/$emb_name $emb_path
ls $data_path

# Setting the results files
name="task1_${experiment_name}"
results_path=$out_path/${name}.txt
results_g1=$out_path/${name}_g1.txt
results_g2=$out_path/${name}_g2.txt

echo ""
echo ""
echo $emb_path
echo ""
ls $data_path
echo ""
echo ""

# We train the CNN
# ISSUE: the model is *not* saved on scratch!
echo Training CNN
python ./cnn/main.py \
	-embeddings=$emb_path \
	-data-path=$data_path/ \
	-data-name=$data_name \
	-no-display=True \
	-save-dir=$temp/

# We evaluate on the whole dataset
echo Evaluating
python ./cnn/main.py \
	-test \
	-embeddings=$emb_path \
	-data-path=$data_path/ \
	-data-name=$data_name \
	-results-path=$results_path \
	-snapshot="${temp}/best_steps_model.pt"

# We evaluate on group 1
echo Evaluating on group 1
python ./cnn/main.py \
	-test \
	-embeddings=$emb_path \
	-data-path=$data_path/ \
	-data-name=$data_name \
	-results-path=$results_g1 \
	-snapshot="${temp}/best_steps_model.pt" \
	-use-half=True \
	-first-half=True

# We evaluate on group 2
echo Evaluationg on group 2
python ./cnn/main.py \
	-test \
	-embeddings=$emb_path \
	-data-path=$data_path/ \
	-data-name=$data_name \
	-results-path=$results_g2 \
	-snapshot="${temp}/best_steps_model.pt" \
	-use-half=True

echo Copying results to the headnode
rsync -av $out_path/ $results_head

echo Deleting data from scratch space
rm -r $temp/*
