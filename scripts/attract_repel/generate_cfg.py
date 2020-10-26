# This automatically generates the configuration lists for the experiments
import sys

# Determine the paths to the embeddings
ant = str(sys.argv[1])
syn = str(sys.argv[2])
embed_path = str(sys.argv[3])
embed_name = str(sys.argv[4])
exp_name = str(sys.argv[5])
config_path = str(sys.argv[6])

# Define the embeddings path
in_embed = embed_path + "/" + embed_name + ".vec"

# Define the paths for the configuration files and for the resulting embeddings
out_embed = embed_path + "/" + exp_name + "_" + embed_name + ".txt"

# Create the corresponding configuration file
with open(config_path, "w", encoding="utf-8") as f:
	f.write("[experiment]\n")
	f.write("\n")
	f.write("log_scores_over_time=False\n")
	f.write("print_simlex=True\n")
	f.write("\n")
	f.write("[data]\n")
	f.write("\n")
	f.write("distributional_vectors = " + in_embed + "\n")
	f.write("\n")
	f.write("antonyms = [" + ant + "]\n")
	f.write("synonyms = [" + syn + "]\n")
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
