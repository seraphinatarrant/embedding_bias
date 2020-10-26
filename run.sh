#!/usr/bin/env bash

set -o errexit

# Variables that should probably be command line arguments
language="es"
weat_test=1
embedding="w2v"
constraints="test1_more"
experiment_name="Pipeline_Test"

# Here go certain flags
clean_data=false
retrain_embs=false
attract_repel=true

# Paths to stuff
emb_train_data=../data/archive/2019_03/tweets_processed.tsv
emb_path=../data/embeddings
weat_out=../results/xweat
cnn_train_data=../data/hateval2019
cnn_out=../results/cnn
cnn2_out=${cnn_out}2
att_rep_const=../scripts/attract_repel/linguistic_constraints

# Each experiment will have its own randomly determined path so that they don't clash with each other
RANDOM=$$
exp_path=/disk/scratch/${USER}/$RANDOM

echo Creating the folder for the experiment
mkdir -p $exp_path

# Go to scripts
cd ./scripts

# Do note that neither of these were made with slurm in mind!
# This one is not memory intensive *at all*
# We determine if we are going to clean the data
if $clean_data; then
	echo About to clean the hateval dataset
	python ./data_cleaning/hateval_cleaning.py
fi

# We can retrain the embeddings
emb_name="${embedding}_embeddings.300"
if $retrain_embs; then
	echo About to train the embeddings
	bash ./train_embeddings.sh $emb_train_data $emb_path $embedding $exp_path
fi

# We can run attract-repel
if $attract_repel; then
	echo About to run attract-repel
	bash ./modify_embeddings.sh "attr-rep" $att_rep_const $constraints $emb_path $emb_name $experiment_name $exp_path
	emb_name=${experiment_name}_${emb_name}
fi

# Run the given WEAT test(s)
echo About to run WEAT test $weat_test
bash ./run_weat.sh $weat_test $emb_path $emb_name $weat_out $language $exp_path

# We add the .vec termination to the embedding name
emb_file=${emb_name}.vec

# Train the CNN for subtask 1
echo About to train the subtask 1 network
bash ./run_cnn.sh $cnn_train_data $emb_path $emb_file $experiment_name $cnn_out $exp_path

# Train the CNN for subtask 2
echo About to train the subtask 2 network
bash ./run_cnn2.sh $cnn_train_data $emb_path $emb_file $experiment_name $cnn2_out $exp_path

echo Experiment successful!
echo Removing temporary files
rm -r $exp_path
