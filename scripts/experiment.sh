#!/usr/bin/env bash

set -o errexit
export PYTHONHASHSEED=0

# Command line arguments
# $1 name of the experiment (for saving the results)
# $2 the WEAT test to run
# $3 is the name of the embedding to use
#    if creating new embeddings, use either "w2v" or "ft"
#    if using existing embeddings, use everything before the "_embeddings.300.vec" part of the filename
# $4 whether to clean the data
# $5 whether to retrain the embeddings
# $6 whether to run attract-repel
# $7 name of the linguistic constraints to use for attract-repel, before adding "_ant.txt" or "_syn.txt"
#    if not using attract-repel, just add "None" or any other dummy value.
# $8 whether to do a weat test


# Variables that should probably be command line arguments
language="es"
weat_test=$2
embedding=$3
constraints=$7
experiment_name=$1

# Here go certain flags
clean_data=$4
retrain_embs=$5
attract_repel=$6
run_weat_test=$8

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
if $run_weat_test; then
	echo About to run WEAT test $weat_test
	bash ./run_weat.sh $weat_test $emb_path $emb_name $weat_out $language $exp_path $experiment_name
fi

# We add the .vec termination to the embedding name
emb_file=${emb_name}.vec

# Train the CNN for subtask 1
echo About to train the subtask 1 network
bash ./run_cnn.sh $cnn_train_data $emb_path $emb_file $experiment_name $cnn_out $exp_path

# Train the CNN for subtask 2
#echo About to train the subtask 2 network
#bash ./run_cnn2.sh $cnn_train_data $emb_path $emb_file $experiment_name $cnn2_out $exp_path

echo Experiment successful!
echo Removing temporary files
rm -r $exp_path
