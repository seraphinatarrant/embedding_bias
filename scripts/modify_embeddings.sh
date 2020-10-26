#!/usr/bin/env bash

# $1 how to modify the embeddings (currently accepts onyl attr-rep)
# $2 path to the lists of words
# $3 name of the files of the list of words (will add _ant.txt and _syn.txt at the end)
# $4 path to the embeddings
# $5 embeddings file to modify
# $6 name for the experiment
# $7 is the path for a particular experiment

method=$1
words_head=$2
ant_list="${3}_ant.txt"
syn_list="${3}_syn.txt"
embeddings_head=$4
embeddings=$5
exp_name=$6
exp_path=$4

# set it to fail at first error
set -o errexit

# source my bashrc
source ~/.bashrc
# activate the tensorflow environment
conda activate tf-gpu-cuda8

echo Creating a temp folder in scratch...
temp=$exp_path/mod_temp
words_path=$temp/constraints
emb_path=$temp/emb
cfg_file=$temp/${exp_name}.cfg
out_embed=${exp_name}_$embeddings
mkdir -p $temp
mkdir -p $words_path
mkdir -p $emb_path

echo Copying data to scratch space
rsync -av $words_head/$ant_list $words_path
rsync -av $words_head/$syn_list $words_path
rsync -av $embeddings_head/${embeddings}.vec $emb_path/${embeddings}.vec

# Updating the paths to the linguistic constraints
ant_list=$words_path/$ant_list
syn_list=$words_path/$syn_list

# If we ever use other embedding modification method, all of this should be in an if statement
echo Generating the configuration file
python ./attract_repel/generate_cfg.py $ant_list $syn_list $emb_path $embeddings $exp_name $cfg_file

echo Running the attract-repel script
python ./attract_repel/code/attract-repel.py $cfg_file

# We activate the project environment
conda activate gensim

# Transform the embeddings from glove format to word2vec
path=$emb_path/${out_embed}.
python -m gensim.scripts.glove2word2vec --input ${path}txt --output ${path}vec

echo ""
echo ""
ls $emb_path
echo ${path}vec
echo ""
echo ""

echo Copying the embeddings to the headnode
rsync -av ${path}vec $embeddings_head/

echo Deleting data from scratch space
rm -r $temp/*
