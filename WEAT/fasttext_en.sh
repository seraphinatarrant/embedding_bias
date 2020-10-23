#!/usr/bin/env bash

## COMMAND LINE ARGUMENTS
# $1: word embeddings in w2v format
# $2: save directory for WEAT results


## arguments for weat.py
#parser.add_argument("--test_number", type=int, help="Number of the weat test to run", required=False)
#parser.add_argument("--permutation_number", type=int, default=None,
#                     help="Number of permutations (otherwise all will be run)", required=False)
#  parser.add_argument("--output_file", type=str, default=None, help="File to store the results)", required=False)
#  parser.add_argument("--lower", type=bool, default=False, help="Whether to lower the vocab", required=False)
#  parser.add_argument("--similarity_type", type=str, default="cosine", help="Which similarity function to use",
#                      required=False)
#  parser.add_argument("--embedding_file", type=str)


#for similarity_type in "cosine" "csls" ; do
for similarity_type in "cosine" ; do
    for test_number in 6 7 8 ; do
        echo $similarity_type
        echo $test_number
        python WEAT/XWEAT/weat.py \
            --test_number $test_number \
            --permutation_number 1000000 \
            --output_file $2/fasttext_en_${similarity_type}_${test_number}.res \
            --lower False \
            --use_glove False \
	    --is_vec_format True \
            --embeddings $1 \
            --similarity_type $similarity_type |& tee ./results/fasttext_en_${similarity_type}_${test_number}.out
    done
done
