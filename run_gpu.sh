# This code should run on any computer with a gpu

# Here go the arguments. If I have the time/energy, I'll change it so the script accepts arguments from command line
clean_data=false
retrain_embs=false
attract_repel=true
embedding_type="ft"	# This should be a value between "ft" and "w2v"
weat_test=1		# Determine the WEAT test to run
exp_name="exp"

# Here go the paths to things
config_path="./attract_repel/config/"		# This is path to the attract-repel configuration
wordlist_path="./linguistic_constraints/test1"	# This is the path to the attract-repel lists might add another
						# script to automatize generating them later

# Other variables
similarity_type="cosine"
language="es"		# This could change depending on the new modified WEAT

# We first go to the scripts folder, as everything else assumes you are running it from there
cd scripts

# We determine if we are going to clean the data
if $clean_data; then
	python ./data_cleaning/hateval_cleaning.py
fi

# We can retrain the embeddings
if $retrain_embs; then
	python ./embeddings/generate_embedding.py
fi

# Generate the attract-repel config file
python ./attract_repel/generate_cfg.py $config_path $wordlist_path

for emb in "ft" "w2v" ; do
	for mod in "more" "less" ; do

		# Run attract-repel
		if $attract_repel; then
			config="exp_${mod}_${emb}.cfg"
			config_path_complete="${config_path}${config}"
			python ./attract_repel/code/attract-repel.py $config_path_complete
		fi

		name="${emb}_exp_${mod}"

		# Transform the embeddings from glove format to word2vec format
		path="../data/embeddings/${name}_embeddings.300."
		python -m gensim.scripts.glove2word2vec --input ${path}txt --output ${path}vec

		res_path="../results/xweat/${name}_test${weat_test}_cased."

		# Run the established weat test
		python xweat/weat.py \
		        --test_number $weat_test \
		        --permutation_number 1000000 \
		        --output_file ${res_path}res \
		        --lower True \
		        --use_glove False \
		        --is_vec_format True \
		        --lang $language \
		        --embeddings ${path}vec \
		        --similarity_type $similarity_type |& tee ${res_path}out
		done

		# Run hateval task 1
		for task in 1 ; do
			data_path="../data/hateval2019/"
			embeddings="${path}vec"
			results_path="../results/cnn/task${task}_${name}.txt"
			data="task${task}_"
			data_name="${data}es_"

			group1="${data}g1_"
			group2="${data}g2_"
			results_g1="../results/cnn/task${task}_${name}_g1.txt"
			results_g2="../results/cnn/task${task}_${name}_g2.txt"

			# Train
			python ./cnn/main.py \
					-embeddings=$embeddings \
					-data-path=$data_path \
					-data-name=$data_name

			# Test on whole dataset
			python ./cnn/main.py \
					-test \
					-embeddings=$embeddings \
					-data-path=$data_path \
					-data-name=$data_name \
					-results-path=$results_path \
					-snapshot="cnn/snapshot/best_steps_model.pt"

			# Test on group 1
			python ./cnn/main.py \
					-test \
					-embeddings=$embeddings \
					-data-path=$data_path \
					-data-name=$data_name \
					-results-path=$results_g1 \
					-snapshot="cnn/snapshot/best_steps_model.pt" \
					-use-half=True \
					-first-half=True

			# Test on group 2
			python ./cnn/main.py \
					-test \
					-embeddings=$embeddings \
					-data-path=$data_path \
					-data-name=$data_name \
					-results-path=$results_g2 \
					-snapshot="cnn/snapshot/best_steps_model.pt" \
					-use-half=True
		done

		# Run hateval task 2
		# *Task 2 is kinda sus*
		for task in 2 ; do
			data_path="../data/hateval2019/"
			embeddings="${path}vec"
			results_path="../results/cnn/task${task}_${name}.txt"
			data="task${task}_"
			data_name="${data}es_"

			group1="${data}g1_"
			group2="${data}g2_"
			results_g1="../results/cnn/task${task}_${name}_g1.txt"
			results_g2="../results/cnn/task${task}_${name}_g2.txt"

			# Train the different pieces of the network
			python ./cnn2/main.py \
					-embeddings=$embeddings \
					-data-path=$data_path \
					-data-name=$data_name \
					-label="HS"
			python ./cnn2/main.py \
					-embeddings=$embeddings \
					-data-path=$data_path \
					-data-name=$data_name \
					-label="TR"
			python ./cnn2/main.py \
					-embeddings=$embeddings \
					-data-path=$data_path \
					-data-name=$data_name \
					-label="AG"
	
			# Test on the whole dataset
			python ./cnn2/main.py \
					-test \
					-embeddings=$embeddings \
					-data-path=$data_path \
					-data-name=$data_name \
					-results-path=$results_path \
					-snapshot="cnn2/snapshot/best_steps_model" \
					-label="HS"
	
			# Test on group 1
			python ./cnn2/main.py \
					-test \
					-embeddings=$embeddings \
					-data-path=$data_path \
					-data-name=$data_name \
					-results-path=$results_g1 \
					-snapshot="cnn2/snapshot/best_steps_model" \
					-use-half=True \
					-first-half=True \
					-label="HS"
	
			# Test on group 2
			python ./cnn2/main.py \
					-test \
					-embeddings=$embeddings \
					-data-path=$data_path \
					-data-name=$data_name \
					-results-path=$results_g2 \
					-snapshot="cnn2/snapshot/best_steps_model" \
					-use-half=True \
					-label="HS"
		done

	done
done

