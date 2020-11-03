#!/usr/bin/env bash

# $1 is the test to run
# $2 is the path to the location of the embeddings
# $3 is the name of the embedding file (skip the .vec part)
# $4 is the path to the results
# $5 is the language
# $6 is the path for a particular experiment
# $7 is the name of the experiment

weat_test=$1
embedding_head=$2
embedding_file=$3
results_head=$4
language=$5
exp_path=$6
exp_name=$7

# set to fail at first error
set -o errexit

# source activate
source ~/.bashrc

# activate the project environment
conda activate gensim

echo Creating a temp folder in scratch space...
temp=$exp_path/weat_temp
emb_path=$temp/data
out_path=$temp/results
res_path=$out_path/${embedding_file}_${exp_name}
mkdir -p $temp
mkdir -p $emb_path
mkdir -p $out_path

echo Copying data to scratch space...
rsync -av $embedding_head/${embedding_file}.vec $emb_path

echo Running WEAT script...
python xweat/weat.py \
	--test_number $weat_test \
	--permutation_number 100000 \
	--output_file ${res_path}.res \
	--lower True \
	--use_glove False \
	--is_vec_format True \
	--lang $language \
	--embeddings $emb_path/${embedding_file}.vec \
	--similarity_type cosine |& tee ${res_path}.out

echo Copying results back to headnode...
rsync -av $out_path/ $results_head

echo Deleting data from scratch space...
rm -r $temp/* 
