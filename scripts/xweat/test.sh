for similarity_type in "cosine" ; do
    for language in "es" ; do
        for test_number in 1 2 6 7 8 9 ; do
            python weat.py \
                --test_number $test_number \
                --permutation_number 1000000 \
                --output_file ./results/w2v_wiki_${language}_${similarity_type}_${test_number}_cased.res \
                --lower True \
                --use_glove False \
                --is_vec_format True \
                --lang $language \
                --embeddings \
                ../../data/embeddings/ft_embeddings.300.vec \
                --similarity_type $similarity_type |& tee ./results/w2v_wiki_${language}_${similarity_type}_${test_number}_cased.out
        done
    done
done
