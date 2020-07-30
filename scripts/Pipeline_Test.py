from importlib import reload
from embeddings.generate_embedding import FastText as ft
from xweat.weat import weat


def main(retrain_embeddings=False):
    
    embeddings_corpus = "../data/archive/2019_03/tweets_processed.tsv"
    fasttext_path = None
    embedding_location = "../data/embeddings/"
    dim = 300
    lang = "es"
    results = "../results/"
    embeddings = "fasttext"
    
    xweat_similarity = ["cosine"]
    tests = [1,2,6,7,8,9]
    
    
    

    if embeddings == "fasttext":
        model_name = "ft"
        if retrain_embeddings:
            model = ft(
                       save = embedding_location,
                       train = retrain_embeddings,
                       corpus_file = embeddings_corpus,
                       fasttext_path = fasttext_path,
                       dim = dim,
                      )
    else:
        raise NotImplementedError
    
    word2vec_embeddings = embedding_location + model_name + "_embeddings." + \
                          str(dim) + ".vec"
    
    
    for similarity in xweat_similarity:
        for test in tests:
            
            print("Running XWEAT test", test, "with the", similarity, "similarity")
            
            output_file = results + "xweat/" + embeddings + "_" + lang + \
                          "_" + similarity + "_" + str(test) + "_lowercase.res"
                          
            weat(
                 test_number = test,
                 permutation_number = 1000000,
                 output_file = output_file,
                 lower = True,
                 use_glove = False,
                 is_vec_format = True,
                 lang = lang,
                 embeddings = word2vec_embeddings,
                 similarity_type = similarity,
                 )

    if retrain_embeddings:
        print(model)


if __name__ == "__main__":
    
    print("alo")
    main()