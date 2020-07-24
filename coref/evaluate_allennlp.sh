#!/usr/bin/env bash

conda activate allennlp

mkdir -p /disk/scratch/s1303513

rsync -av --progress ./git2/embedding_bias/coref/evaluation_data/test_type1_anti_stereotype.v4_auto_conll /disk/scratch/s1303513/test_type1_anti_stereotype.v4_auto_conll
rsync -av --progress ./git2/embedding_bias/coref/evaluation_data/test_type1_pro_stereotype.v4_auto_conll /disk/scratch/s1303513/test_type1_pro_stereotype.v4_auto_conll
rsync -av --progress ./git2/embedding_bias/coref/evaluation_data/test_type2_anti_stereotype.v4_auto_conll /disk/scratch/s1303513/test_type2_anti_stereotype.v4_auto_conll
rsync -av --progress ./git2/embedding_bias/coref/evaluation_data/test_type2_pro_stereotype.v4_auto_conll /disk/scratch/s1303513/test_type2_pro_stereotype.v4_auto_conll



rsync -av ./allennlp/results_new/results_t2/model.tar.gz /disk/scratch/s1303513/model.tar.gz


allennlp evaluate /disk/scratch/s1303513/model.tar.gz /disk/scratch/s1303513/test_type1_anti_stereotype.v4_auto_conll --output-file /disk/scratch/s1303513/type1_anti_results_t6.txt

allennlp evaluate /disk/scratch/s1303513/model.tar.gz /disk/scratch/s1303513/test_type1_pro_stereotype.v4_auto_conll --output-file /disk/scratch/s1303513/type1_pro_results_t6.txt

allennlp evaluate /disk/scratch/s1303513/model.tar.gz /disk/scratch/s1303513/test_type2_anti_stereotype.v4_auto_conll --output-file /disk/scratch/s1303513/type2_anti_results_t6.txt

allennlp evaluate /disk/scratch/s1303513/model.tar.gz /disk/scratch/s1303513/test_type2_pro_stereotype.v4_auto_conll --output-file /disk/scratch/s1303513/type2_pro_results_t6.txt


rsync -av --progress /disk/scratch/s1303513/type1_anti_results_t1.txt ./allennlp/results/evaluation/type1_anti_results_t1.txt
rsync -av --progress /disk/scratch/s1303513/type1_pro_results_t1.txt ./allennlp/results/evaluation/type1_pro_results_t1.txt
rsync -av --progress /disk/scratch/s1303513/type2_anti_results_t1.txt ./allennlp/results/evaluation/type2_anti_results_t1.txt
rsync -av --progress /disk/scratch/s1303513/type2_pro_results_t1.txt ./allennlp/results/evaluation/type2_pro_results_t1.txt

rm /disk/scratch/s1303513/*
