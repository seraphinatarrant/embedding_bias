#!/usr/bin/env bash

## COMMAND LINE ARGUMENTS
# $1: trained coreference resolution model (model.tar.gz)
# $2: folder where the results will be saved

export STUDENT_ID=$(whoami)

# activate allennlp environment
conda activate allennlp

# create a folder
mkdir -p /disk/scratch/${STUDENT_ID}/coref_evaluate

# copy the winobias evaluation data into scratch space
rsync -av ./evaluation_data/test_type1_anti_stereotype.v4_auto_conll /disk/scratch/${STUDENT_ID}/coref_evaluate/test_type1_anti_stereotype.v4_auto_conll
rsync -av ./evaluation_data/test_type1_pro_stereotype.v4_auto_conll /disk/scratch/${STUDENT_ID}/coref_evaluate/test_type1_pro_stereotype.v4_auto_conll
rsync -av ./evaluation_data/test_type2_anti_stereotype.v4_auto_conll /disk/scratch/${STUDENT_ID}/coref_evaluate/test_type2_anti_stereotype.v4_auto_conll
rsync -av ./evaluation_data/test_type2_pro_stereotype.v4_auto_conll /disk/scratch/${STUDENT_ID}/coref_evaluate/test_type2_pro_stereotype.v4_auto_conll


# copy the trained coreference model into scratch space
rsync -av $1 /disk/scratch/${STUDENT_ID}/coref_evaluate/model.tar.gz

# evaluate the model on the four different sets of evaluation data
allennlp evaluate /disk/scratch/${STUDENT_ID}/coref_evaluate/model.tar.gz /disk/scratch/${STUDENT_ID}/coref_evaluate/test_type1_anti_stereotype.v4_auto_conll --output-file /disk/scratch/${STUDENT_ID}/coref_evaluate/type1_anti_results.txt
allennlp evaluate /disk/scratch/${STUDENT_ID}/coref_evaluate/model.tar.gz /disk/scratch/${STUDENT_ID}/coref_evaluate/test_type1_pro_stereotype.v4_auto_conll --output-file /disk/scratch/${STUDENT_ID}/coref_evaluate/type1_pro_results.txt
allennlp evaluate /disk/scratch/${STUDENT_ID}/coref_evaluate/model.tar.gz /disk/scratch/${STUDENT_ID}/coref_evaluate/test_type2_anti_stereotype.v4_auto_conll --output-file /disk/scratch/${STUDENT_ID}/coref_evaluate/type2_anti_results.txt
allennlp evaluate /disk/scratch/${STUDENT_ID}/coref_evaluate/model.tar.gz /disk/scratch/${STUDENT_ID}/coref_evaluate/test_type2_pro_stereotype.v4_auto_conll --output-file /disk/scratch/${STUDENT_ID}/coref_evaluate/type2_pro_results.txt

# copy the results to the specified folder
rsync -av /disk/scratch/${STUDENT_ID}/coref_evaluate/type1_anti_results.txt $2/type1_anti_results.txt
rsync -av /disk/scratch/${STUDENT_ID}/coref_evaluate/type1_pro_results.txt $2/type1_pro_results.txt
rsync -av /disk/scratch/${STUDENT_ID}/coref_evaluate/type2_anti_results.txt $2/type2_anti_results.txt
rsync -av /disk/scratch/${STUDENT_ID}/coref_evaluate/type2_pro_results.txt $2/type2_pro_results.txt

# remove data from scratch space
rm -r /disk/scratch/${STUDENT_ID}/coref_evaluate
