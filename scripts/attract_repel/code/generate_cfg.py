#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 02:56:18 2020

@author: s1983961
"""



path = "attract_repel/config/test"
embed_path_1 = "../data/embeddings/"
embed_path_2 = "_embeddings.300."
tests = [1,2,6,7,8,9]
mods = ["more","less"]
embeddings = ["ft", "w2v"]

for embedding in embeddings:
    embed_path = embed_path_1 + embedding + embed_path_2 + "vec"
    for test in tests:
        for mod in mods:
            
            config_path = path + str(test) + "_" + mod + "_" + embedding + ".cfg"
            out_embed = embed_path_1 + embedding + "_t" + str(test) + "_" + mod + embed_path_2 + "txt"
            
            with open(config_path, "w", encoding="utf-8") as f:
                f.write("[experiment]\n")
                f.write("\n")
                f.write("log_scores_over_time=False\n")
                f.write("print_simlex=True\n")
                f.write("\n")
                f.write("[data]\n")
                f.write("\n")
                f.write("distributional_vectors = " + embed_path + "\n")
                f.write("\n")
                f.write("antonyms = [attract_repel/linguistic_constraints/test" + str(test) + "_" + mod + "_ant.txt]\n")
                f.write("synonyms = [attract_repel/linguistic_constraints/test" + str(test) + "_" + mod + "_syn.txt]\n")
                f.write("\n")
                f.write("output_filepath = " + out_embed + "\n")
                f.write("\n")
                f.write("[hyperparameters]\n")
                f.write("\n")
                f.write("attract_margin = 0.6\n")
                f.write("repel_margin = 0.0\n")
                f.write("batch_size = 50\n")
                f.write("l2_reg_constant = 0.000000001\n")
                f.write("max_iter = 5\n")