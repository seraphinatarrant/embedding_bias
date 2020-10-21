# This automatically generates the configuration lists for the experiments
import sys

# Determine the paths to the embeddings
path = str(sys.argv[0])
constraints = str(sys.argv[1])
embed_path_1 = "../data/embeddings/"
embed_path_2 = "_embeddings.300."

# Set the experiments that we will have
mods = ["more","less"]
embeddings = ["ft", "w2v"]


for embedding in embeddings:
    
    # Define the embeddings path
    embed_path = embed_path_1 + embedding + embed_path_2 + "vec"
    
    # For each experiment, we run this code
	for mod in mods:
		
		# Define the paths for the configuration files and for the resulting embeddings
		config_path = path + "exp_" + mod + "_" + embedding + ".cfg"
		out_embed = embed_path_1 + embedding + "_exp_" + mod + embed_path_2 + "txt"
		
		# Create the corresponding configuration file
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
			f.write("antonyms = [" + constraints + "_" + mod + "_ant.txt]\n")
			f.write("synonyms = [" + constraints + "_" + mod + "_syn.txt]\n")
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