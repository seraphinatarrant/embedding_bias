# This part runs WEAT for the basic embeddings
similarity_type="cosine"
language="es"

conda init bash


for emb in "ft" "w2v" ; do

	embeddings_path="../data/embeddings/${emb}_embeddings.300.vec"

	# This activates the environment with tensorflow
#	conda activate tf-gpu-cuda8
#    for test_number in "1" "2" "6" "7" "8" "9" ; do
#        python xweat/weat.py \
#            --test_number $test_number \
#            --permutation_number 1000000 \
#            --output_file ../results/xweat/${emb}_test${test_number}_cased.res \
#            --lower True \
#            --use_glove False \
#            --is_vec_format True \
#            --lang $language \
#            --embeddings $embeddings_path \
#            --similarity_type $similarity_type |& tee ../results/xweat/${emb}_test${test_number}_cased.out
#    done

	# This activates the environment with gensim
	conda activate gensim
#	for task in 1 ; do
#		data_path="../data/hateval2019/"
#		results_path="../results/cnn/task${task}_${emb}.txt"
#		data="task${task}_"
#		data_name="${data}es_"
#
#		results_g1="../results/cnn/task${task}_${emb}_g1.txt"
#		results_g2="../results/cnn/task${task}_${emb}_g2.txt"
#
#
#		python ./cnn/main.py \
#				-embeddings=$embeddings_path \
#				-data-path=$data_path \
#				-data-name=$data_name
#	
#		python ./cnn/main.py \
#				-test \
#				-embeddings=$embeddings_path \
#				-data-path=$data_path \
#				-data-name=$data_name \
#				-results-path=$results_path \
#				-snapshot="cnn/snapshot/best_steps_model.pt"
#	
#		python ./cnn/main.py \
#				-test \
#				-embeddings=$embeddings_path \
#				-data-path=$data_path \
#				-data-name=$data_name \
#				-results-path=$results_g1 \
#				-snapshot="cnn/snapshot/best_steps_model.pt" \
#				-use-half=True \
#				-first-half=True
#	
#		python ./cnn/main.py \
#				-test \
#				-embeddings=$embeddings_path \
#				-data-path=$data_path \
#				-data-name=$data_name \
#				-results-path=$results_g2 \
#				-snapshot="cnn/snapshot/best_steps_model.pt" \
#				-use-half=True
#	done

	for task in 2 ; do
		data_path="../data/hateval2019/"
		results_path="../results/cnn/task${task}_${emb}.txt"
		data="task${task}_"
		data_name="${data}es_"

		results_g1="../results/cnn/task${task}_${emb}_g1.txt"
		results_g2="../results/cnn/task${task}_${emb}_g2.txt"


		python ./cnn2/main.py \
				-embeddings=$embeddings_path \
				-data-path=$data_path \
				-data-name=$data_name \
				-label="HS"
		python ./cnn2/main.py \
				-embeddings=$embeddings_path \
				-data-path=$data_path \
				-data-name=$data_name \
				-label="TR"
		python ./cnn2/main.py \
				-embeddings=$embeddings_path \
				-data-path=$data_path \
				-data-name=$data_name \
				-label="AG"
	
		python ./cnn2/main.py \
				-test \
				-embeddings=$embeddings_path \
				-data-path=$data_path \
				-data-name=$data_name \
				-results-path=$results_path \
				-snapshot="cnn2/snapshot/best_steps_model" \
				-label="HS"
	
		python ./cnn2/main.py \
				-test \
				-embeddings=$embeddings_path \
				-data-path=$data_path \
				-data-name=$data_name \
				-results-path=$results_g1 \
				-snapshot="cnn2/snapshot/best_steps_model" \
				-use-half=True \
				-first-half=True \
				-label="HS"
	
		python ./cnn2/main.py \
				-test \
				-embeddings=$embeddings_path \
				-data-path=$data_path \
				-data-name=$data_name \
				-results-path=$results_g2 \
				-snapshot="cnn2/snapshot/best_steps_model" \
				-use-half=True \
				-label="HS"
	done


done


