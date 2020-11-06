#!/usr/bin/env bash

## COMMAND LINE ARGUMENTS
# $1: original trained word embeddings
# $2: path to save folder for the results

export STUDENT_ID=$(whoami)

# set to exit at first error
set -o errexit

source ~/.bashrc

# activate the project environment
conda activate bias_env

# make a dedicated directory in the scratch space of the cluster node
mkdir -p /disk/scratch/${STUDENT_ID}/attractrepel

echo copying data to scratch space
# copy the original embedding vectors into this new directory
rsync -av $1 /disk/scratch/${STUDENT_ID}/attractrepel/original_vectors.txt


# copy the synonym and antonym sets for each of WEAT 6, 7, 8
# for each WEAT the first test e.g. t1 contains the synonym and antonym sets necessary for debiasing, the second test (e.g. t2) is for overbiasing
rsync -av ./weat6_ant_t1.txt /disk/scratch/${STUDENT_ID}/attractrepel/
rsync -av ./weat6_syn_t1.txt /disk/scratch/${STUDENT_ID}/attractrepel/

rsync -av ./weat6_ant_t2.txt /disk/scratch/${STUDENT_ID}/attractrepel/
rsync -av ./weat6_syn_t2.txt /disk/scratch/${STUDENT_ID}/attractrepel/

rsync -av ./weat7_ant_t3.txt /disk/scratch/${STUDENT_ID}/attractrepel/
rsync -av ./weat7_syn_t3.txt /disk/scratch/${STUDENT_ID}/attractrepel/

rsync -av ./weat7_ant_t4.txt /disk/scratch/${STUDENT_ID}/attractrepel/
rsync -av ./weat7_syn_t4.txt /disk/scratch/${STUDENT_ID}/attractrepel/

rsync -av ./weat8_ant_t5.txt /disk/scratch/${STUDENT_ID}/attractrepel/
rsync -av ./weat8_syn_t5.txt /disk/scratch/${STUDENT_ID}/attractrepel/

rsync -av ./weat8_ant_t6.txt /disk/scratch/${STUDENT_ID}/attractrepel/
rsync -av ./weat8_syn_t6.txt /disk/scratch/${STUDENT_ID}/attractrepel/



# Running the attract-repel algorithm in the debiasing and overbiasing direction for each WEAT test
# Saves the new vectos as ar_vectors_t1 etc


echo AR test 1 \(WEAT 6 debias\)

python3 ./attract-repel/attract-repel_new.py ./experiment_parameters_t1.cfg

echo AR test 2 \(WEAT 6 overbias\)

python3 ./attract-repel/attract-repel_new.py ./experiment_parameters_t2.cfg

echo AR test 3 \(WEAT 7 debias\)

python3 ./attract-repel/attract-repel_new.py ./experiment_parameters_t3.cfg

echo AR test 4 \(WEAT 7 overbias\)

python3 ./attract-repel/attract-repel_new.py ./experiment_parameters_t4.cfg

echo AR test 5 \(WEAT 8 debias\)

python3 ./attract-repel/attract-repel_new.py ./experiment_parameters_t5.cfg

echo AR test 6 \(WEAT 8 overbias\)

python3 ./attract-repel/attract-repel_new.py ./experiment_parameters_t6.cfg

echo copying vectors back to headnode

rsync -av /disk/scratch/${STUDENT_ID}/attractrepel/ar_vectors_* $2

echo deleting data from scratch space

rm /disk/scratch/${STUDENT_ID}/attractrepel/*
