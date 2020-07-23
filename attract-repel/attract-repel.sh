#!/usr/bin/env bash

set -o errexit

source ~/.bashrc

conda activate bias_env

mkdir -p /disk/scratch/s1303513

echo copying data to scratch space

rsync -av ./embeddings/ft_new_vectors.txt /disk/scratch/s1303513/ft_new_vectors.text

rsync -av ./a_r/weat6_ant_t1.txt /disk/scratch/s1303513/
rsync -av ./a_r/weat6_syn_t1.txt /disk/scratch/s1303513/

rsync -av ./a_r/weat6_ant_t2.txt /disk/scratch/s1303513/
rsync -av ./a_r/weat6_syn_t2.txt /disk/scratch/s1303513/

rsync -av ./a_r/weat7_ant_t3.txt /disk/scratch/s1303513/
rsync -av ./a_r/weat7_syn_t3.txt /disk/scratch/s1303513/

rsync -av ./a_r/weat7_ant_t4.txt /disk/scratch/s1303513/
rsync -av ./a_r/weat7_syn_t4.txt /disk/scratch/s1303513/

rsync -av ./a_r/weat8_ant_t5.txt /disk/scratch/s1303513/
rsync -av ./a_r/weat8_syn_t5.txt /disk/scratch/s1303513/

rsync -av ./a_r/weat8_ant_t6.txt /disk/scratch/s1303513/
rsync -av ./a_r/weat8_syn_t6.txt /disk/scratch/s1303513/

echo AR test 1

python3 ./a_r/attract-repel/code/attract-repel.py ./a_r/attract-repel/config/experiment_parameters_t1.cfg

echo AR test 2

python3 ./a_r/attract-repel/code/attract-repel.py ./a_r/attract-repel/config/experiment_parameters_t2.cfg

echo AR test 3

python3 ./a_r/attract-repel/code/attract-repel.py ./a_r/attract-repel/config/experiment_parameters_t3.cfg

echo AR test 4

python3 ./a_r/attract-repel/code/attract-repel.py ./a_r/attract-repel/config/experiment_parameters_t4.cfg

echo AR test 5

python3 ./a_r/attract-repel/code/attract-repel.py ./a_r/attract-repel/config/experiment_parameters_t5.cfg

echo AR test 6

python3 ./a_r/attract-repel/code/attract-repel.py ./a_r/attract-repel/config/experiment_parameters_t6.cfg

echo copying vectors back

rsync -av /disk/scratch/s1303513/ar_vectors_* ./embeddings/ar_vectors/

echo deleting data from scratch space

rm /disk/scratch/s1303513/*
