#!/usr/bin/env bash

# Here go certain flags
clean_data=false
retrain_embs=false

# set to fail at first error
set -o errexit

# Go to scripts
cd ./scripts

# Do note that neither of these were made with slurm in mind!
# This one is not memory intensive *at all*
# We determine if we are going to clean the data
if $clean_data; then
	python ./data_cleaning/hateval_cleaning.py
fi

# Do note that neither of these were made with slurm in mind!
# This one does take some time, though
# We can retrain the embeddings
if $retrain_embs; then
	python ./embeddings/generate_embedding.py
fi