for similarity_type in "cosine" ; do
    for language in "es" ; do
        for test_number in 3 4 5 6 10; do
            python weat.py \
                --test_number $test_number \
                --permutation_number 1000000 \
                --output_file ./results/w2v_wiki_${language}_${similarity_type}_${test_number}_cased.res \
                --lower True \
                --use_glove False \
                --is_vec_format True \
                --lang $language \
                --embeddings \
                ../Twitter/test_embeddings \
                --similarity_type $similarity_type |& tee ./results/w2v_wiki_${language}_${similarity_type}_${test_number}_cased.out
        done
    done
done
