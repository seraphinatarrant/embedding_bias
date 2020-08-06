#!/usr/bin/env bash

conda activate allennlp

mkdir -p /disk/scratch/s1303513/evalcheck

rsync -av --progress ./git2/embedding_bias/coref/evaluation_data/test_type1_anti_stereotype.v4_auto_conll /disk/scratch/s1303513/evalcheck/test_type1_anti_stereotype.v4_auto_conll
rsync -av --progress ./git2/embedding_bias/coref/evaluation_data/test_type1_pro_stereotype.v4_auto_conll /disk/scratch/s1303513/evalcheck/test_type1_pro_stereotype.v4_auto_conll
rsync -av --progress ./git2/embedding_bias/coref/evaluation_data/test_type2_anti_stereotype.v4_auto_conll /disk/scratch/s1303513/evalcheck/test_type2_anti_stereotype.v4_auto_conll
rsync -av --progress ./git2/embedding_bias/coref/evaluation_data/test_type2_pro_stereotype.v4_auto_conll /disk/scratch/s1303513/evalcheck/test_type2_pro_stereotype.v4_auto_conll



rsync -av ./results_ft_ar_t1_check/model.tar.gz /disk/scratch/s1303513/evalcheck/model.tar.gz


allennlp evaluate /disk/scratch/s1303513/evalcheck/model.tar.gz /disk/scratch/s1303513/evalcheck/test_type1_anti_stereotype.v4_auto_conll --output-file /disk/scratch/s1303513/evalcheck/type1_anti_results_t1_check.txt

allennlp evaluate /disk/scratch/s1303513/evalcheck/model.tar.gz /disk/scratch/s1303513/evalcheck/test_type1_pro_stereotype.v4_auto_conll --output-file /disk/scratch/s1303513/evalcheck/type1_pro_results_t1_check.txt

allennlp evaluate /disk/scratch/s1303513/evalcheck/model.tar.gz /disk/scratch/s1303513/evalcheck/test_type2_anti_stereotype.v4_auto_conll --output-file /disk/scratch/s1303513/evalcheck/type2_anti_results_t1_check.txt

allennlp evaluate /disk/scratch/s1303513/evalcheck/model.tar.gz /disk/scratch/s1303513/evalcheck/test_type2_pro_stereotype.v4_auto_conll --output-file /disk/scratch/s1303513/evalcheck/type2_pro_results_t1_check.txt


rsync -av --progress /disk/scratch/s1303513/evalcheck/type1_anti_results_t1_check.txt ./allennlp/results_new/w2v/evaluation/type1_anti_results_bl_w2v.txt
rsync -av --progress /disk/scratch/s1303513/evalcheck/type1_pro_results_t1_check.txt ./allennlp/results_new/w2v/evaluation/type1_pro_results_bl_w2v.txt
rsync -av --progress /disk/scratch/s1303513/evalcheck/type2_anti_results_t1_check.txt ./allennlp/results_new/w2v/evaluation/type2_anti_results_bl_w2v.txt
rsync -av --progress /disk/scratch/s1303513/evalcheck/type2_pro_results_t1_check.txt ./allennlp/results_new/w2v/evaluation/type2_pro_results_bl_w2v.txt

rm -r /disk/scratch/s1303513/evalcheck
