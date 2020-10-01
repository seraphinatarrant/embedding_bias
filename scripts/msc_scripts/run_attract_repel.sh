# Basically what this does is run the attract repel script. You must give the name of a file in the attract-repel/config folder to be able to run this.

source ~/miniconda3/etc/profile.d/conda.sh
conda activate gensim

# These lines generate the lists of synonims and antonyms
python xweat/generate_lists.py

# This line generates the config files
python msc_scripts/generate_cfg.py

# Choose between 1 2 6 7 8 9
test_embs=$1


similarity_type="cosine"
language="es"

for emb in "ft" "w2v" ; do
	for mod in "more" "less" ; do

		# This activates the environment with tensorflow
		conda activate tf-gpu-cuda8

		config="test${test_embs}_${mod}_${emb}.cfg"
		config_path="./attract_repel/config/${config}"
		python ./attract_repel/code/attract-repel.py $config_path


		# This activates the environment with gensim
		conda activate gensim

		name="${emb}_t${test_embs}_${mod}"

		# Transform the embeddings from glove format to word2vec format
		path="../data/embeddings/${name}_embeddings.300."

		python -m gensim.scripts.glove2word2vec --input ${path}txt --output ${path}vec


		for test_number in 1 2 6 7 8 9 ; do
			res_path="../results/xweat/${name}_test${test_number}_cased."

		    python xweat/weat.py \
		        --test_number $test_number \
		        --permutation_number 1000000 \
		        --output_file ${res_path}res \
		        --lower True \
		        --use_glove False \
		        --is_vec_format True \
		        --lang $language \
		        --embeddings ${path}vec \
		        --similarity_type $similarity_type |& tee ${res_path}out
		done

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


			python ./cnn/main.py \
					-embeddings=$embeddings \
					-data-path=$data_path \
					-data-name=$data_name

			python ./cnn/main.py \
					-test \
					-embeddings=$embeddings \
					-data-path=$data_path \
					-data-name=$data_name \
					-results-path=$results_path \
					-snapshot="cnn/snapshot/best_steps_model.pt"

			python ./cnn/main.py \
					-test \
					-embeddings=$embeddings \
					-data-path=$data_path \
					-data-name=$data_name \
					-results-path=$results_g1 \
					-snapshot="cnn/snapshot/best_steps_model.pt" \
					-use-half=True \
					-first-half=True

			python ./cnn/main.py \
					-test \
					-embeddings=$embeddings \
					-data-path=$data_path \
					-data-name=$data_name \
					-results-path=$results_g2 \
					-snapshot="cnn/snapshot/best_steps_model.pt" \
					-use-half=True
		done

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
	
			python ./cnn2/main.py \
					-test \
					-embeddings=$embeddings \
					-data-path=$data_path \
					-data-name=$data_name \
					-results-path=$results_path \
					-snapshot="cnn2/snapshot/best_steps_model" \
					-label="HS"
	
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

