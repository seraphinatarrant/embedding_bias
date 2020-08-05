#!/usr/bin/env bash

conda activate allennlp

mkdir -p /disk/scratch/s1303513

rsync -av --progress ./git2/embedding_bias/coref/evaluation_data/test_type1_anti_stereotype.v4_auto_conll /disk/scratch/s1303513/test_type1_anti_stereotype.v4_auto_conll
rsync -av --progress ./git2/embedding_bias/coref/evaluation_data/test_type1_pro_stereotype.v4_auto_conll /disk/scratch/s1303513/test_type1_pro_stereotype.v4_auto_conll
rsync -av --progress ./git2/embedding_bias/coref/evaluation_data/test_type2_anti_stereotype.v4_auto_conll /disk/scratch/s1303513/test_type2_anti_stereotype.v4_auto_conll
rsync -av --progress ./git2/embedding_bias/coref/evaluation_data/test_type2_pro_stereotype.v4_auto_conll /disk/scratch/s1303513/test_type2_pro_stereotype.v4_auto_conll



rsync -av ./allennlp/results_new/ft/results_t2/model.tar.gz /disk/scratch/s1303513/model.tar.gz


allennlp evaluate /disk/scratch/s1303513/model.tar.gz /disk/scratch/s1303513/test_type1_anti_stereotype.v4_auto_conll --output-file /disk/scratch/s1303513/type1_anti_results_t2-test.txt

allennlp evaluate /disk/scratch/s1303513/model.tar.gz /disk/scratch/s1303513/test_type1_pro_stereotype.v4_auto_conll --output-file /disk/scratch/s1303513/type1_pro_results_t2-test.txt

allennlp evaluate /disk/scratch/s1303513/model.tar.gz /disk/scratch/s1303513/test_type2_anti_stereotype.v4_auto_conll --output-file /disk/scratch/s1303513/type2_anti_results_t2.txt

allennlp evaluate /disk/scratch/s1303513/model.tar.gz /disk/scratch/s1303513/test_type2_pro_stereotype.v4_auto_conll --output-file /disk/scratch/s1303513/type2_pro_results_t2.txt


rsync -av --progress /disk/scratch/s1303513/type1_anti_results_bl_w2v.txt ./allennlp/results_new/w2v/evaluation/type1_anti_results_bl_w2v.txt
rsync -av --progress /disk/scratch/s1303513/type1_pro_results_bl_w2v.txt ./allennlp/results_new/w2v/evaluation/type1_pro_results_bl_w2v.txt
rsync -av --progress /disk/scratch/s1303513/type2_anti_results_bl_w2v.txt ./allennlp/results_new/w2v/evaluation/type2_anti_results_bl_w2v.txt
rsync -av --progress /disk/scratch/s1303513/type2_pro_results_bl_w2v.txt ./allennlp/results_new/w2v/evaluation/type2_pro_results_bl_w2v.txt

rm /disk/scratch/s1303513/*
