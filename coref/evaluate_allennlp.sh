#!/usr/bin/env bash

conda activate allennlp

mkdir -p /disk/scratch/s1303513/evald6

rsync -av --progress ./git2/embedding_bias/coref/evaluation_data/test_type1_anti_stereotype.v4_auto_conll /disk/scratch/s1303513/evald6/test_type1_anti_stereotype.v4_auto_conll
rsync -av --progress ./git2/embedding_bias/coref/evaluation_data/test_type1_pro_stereotype.v4_auto_conll /disk/scratch/s1303513/evald6/test_type1_pro_stereotype.v4_auto_conll
rsync -av --progress ./git2/embedding_bias/coref/evaluation_data/test_type2_anti_stereotype.v4_auto_conll /disk/scratch/s1303513/evald6/test_type2_anti_stereotype.v4_auto_conll
rsync -av --progress ./git2/embedding_bias/coref/evaluation_data/test_type2_pro_stereotype.v4_auto_conll /disk/scratch/s1303513/evald6/test_type2_pro_stereotype.v4_auto_conll



rsync -av ./results_d6_w2v/model.tar.gz /disk/scratch/s1303513/evald6/model.tar.gz


allennlp evaluate /disk/scratch/s1303513/evald6/model.tar.gz /disk/scratch/s1303513/evald6/test_type1_anti_stereotype.v4_auto_conll --output-file /disk/scratch/s1303513/evald6/type1_anti_results_t1_d6.txt

allennlp evaluate /disk/scratch/s1303513/evald6/model.tar.gz /disk/scratch/s1303513/evald6/test_type1_pro_stereotype.v4_auto_conll --output-file /disk/scratch/s1303513/evald6/type1_pro_results_t1_d6.txt

allennlp evaluate /disk/scratch/s1303513/evald6/model.tar.gz /disk/scratch/s1303513/evald6/test_type2_anti_stereotype.v4_auto_conll --output-file /disk/scratch/s1303513/evald6/type2_anti_results_t1_d6.txt

allennlp evaluate /disk/scratch/s1303513/evald6/model.tar.gz /disk/scratch/s1303513/evald6/test_type2_pro_stereotype.v4_auto_conll --output-file /disk/scratch/s1303513/evald6/type2_pro_results_t1_d6.txt


rsync -av --progress /disk/scratch/s1303513/evald6/type1_anti_results_t1_d6.txt ./allennlp/results_new/w2v/evaluation/type1_anti_results_d6_w2v.txt
rsync -av --progress /disk/scratch/s1303513/evald6/type1_pro_results_t1_d6.txt ./allennlp/results_new/w2v/evaluation/type1_pro_results_d6_w2v.txt
rsync -av --progress /disk/scratch/s1303513/evald6/type2_anti_results_t1_d6.txt ./allennlp/results_new/w2v/evaluation/type2_anti_results_d6_w2v.txt
rsync -av --progress /disk/scratch/s1303513/evald6/type2_pro_results_t1_d6.txt ./allennlp/results_new/w2v/evaluation/type2_pro_results_d6_w2v.txt

rm -r /disk/scratch/s1303513/evald6
