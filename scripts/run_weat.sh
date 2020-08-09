similarity_type="cosine"
language="es"

# Choose between 1 2 6 7 8 9
test_embs=1

# Choose between "ft" "w2v"
embeddings="ft"

for mod in "more" "less" ; do
    for test_number in 1 2 6 7 8 9 ; do
        python xweat/weat.py \
            --test_number $test_number \
            --permutation_number 1000000 \
            --output_file ../results/${embeddings}_${test_embs}${mod}_test${test_number}_cased.res \
            --lower True \
            --use_glove False \
            --is_vec_format True \
            --lang $language \
            --embeddings \
            ../data/embeddings/${embeddings}_t${test_embs}_${mod}_embeddings.300.txt \
            --similarity_type $similarity_type |& tee ../results/${embeddings}_${test_embs}${mod}_test${test_number}_cased.out
    done
done

