#!/bin/bash
# COREF
python display_data.py -r results/coref_results_all.csv -o single_experiment_graphs/coref -coref -single_experiment_plots -sep_weat
# HSD EN
python display_data.py -r results/hsd_en.csv -o single_experiment_graphs/hsd_en -hsd_en -single_experiment_plots -sep_weat

# HSD ES
python display_data.py -r results/results_es_metrics_migrants.csv -o single_experiment_graphs/hsd_es_migrant -hsd_es -hsd_es_exclude "gender" -single_experiment_plots
python display_data.py -r results/results_es_metrics_gender.csv -o single_experiment_graphs/hsd_es_gender -hsd_es -hsd_es_exclude "migrant" -single_experiment_plots
