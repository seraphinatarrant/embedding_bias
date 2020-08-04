from gensim.models.wrappers.fasttext import FastText as FT_wrapper
from gensim.models.fasttext import FastText as FT_gensim
from gensim.models import Word2Vec


####################################################################


def train_fasttext(corpus_file, fasttext_path=None, save="../data/embeddings/",
                   dim=300):
    """
    
    Input:
        corpus_file:
            the path to the file that has the embedding training dataset.
        fasttext_path:
            path to the FastText executable. If not given, we use the gensim
            reimplementation instead.
        save:
            the directory where the embeddings will be saved.
        dim:
            number of dimensions for the embeddings.
            
    Output:
        A file with the embeddings both in gensim format and in word2vec format.
        It also returns the model itself.
        
    """    
    
    print("Generating embeddings...")
    
    if fasttext_path is not None:
        # Run this if FastText is installed
        
        print("FastText wrapper loaded")
        
        # Set FastText home to the path to the FastText executable
        ft_home = fasttext_path
        
        print("\nCreating embeddings model...")

        # train the model
        model = FT_wrapper.train(ft_home, corpus_file, sg=1, size=dim)
        
        print("Model created and trained")
        
        
    else:
        # Run this if using windows or if FastText is not installed
        
        print("Gensim implementation loaded")

        print("\nCreating embeddings model...")
        model = FT_gensim(size=dim,sg=1)
        print("Model created")

        # build the vocabulary
        print("\nGenerating vocabulary...")
        model.build_vocab(corpus_file=corpus_file)
        print("Vocabulary generated")

        # train the model
        print("\nTraining embeddings model")
        model.train(
                    corpus_file=corpus_file, epochs=model.epochs,
                    total_examples=model.corpus_count, total_words=model.corpus_total_words
                   )
        print("Model trained:")


    print(model, "\n")
        
    # saving a model
    if save is not None:
        path = save + "ft_embeddings." + str(dim)
        model.save(path + ".model")
        
        model.wv.save_word2vec_format(path + ".vec")
        
        gg = open(path+".txt",'w', encoding="utf8")
        for token in model.wv.vocab.keys():
            string = token
            for value in model.wv[token]:
                string += " " + str(value)
            gg.write(string+'\n')
        gg.close()
        
        print("Embeddings saved\n")
        
    print("")
    
    return model
    

##############################################################################
    

def train_word2vec(corpus_file, save="../data/embeddings/", dim=300):
    """
    
    Input:
        corpus_file:
            the path to the file that has the embedding training dataset.¿
        save:
            the directory where the embeddings will be saved.
        dim:
            number of dimensions for the embeddings.
            
    Output:
        A file with the embeddings both in gensim format and in word2vec format.
        It also returns the model itself.
        
    """    
    
    print("Generating embeddings...")
        
    print("\nCreating embeddings model...")
    model = Word2Vec(size=dim,sg=1)
    print("Model created")

    # build the vocabulary
    print("\nGenerating vocabulary...")
    model.build_vocab(corpus_file=corpus_file)
    print("Vocabulary generated")

    # train the model
    print("\nTraining embeddings model")
    model.train(
                corpus_file=corpus_file, epochs=model.epochs,
                total_examples=model.corpus_count, total_words=model.corpus_total_words
               )
    print("Model trained:")


    print(model, "\n")
    
        
    # saving a model
    if save is not None:
        path = save + "w2v_embeddings." + str(dim)
        model.save(path + ".model")
        
        model.wv.save_word2vec_format(path + ".vec")
        
        gg = open(path+".txt",'w', encoding="utf8")
        for token in model.wv.vocab.keys():
            string = token
            for value in model.wv[token]:
                string += " " + str(value)
            gg.write(string+'\n')
        gg.close()
        
        print("Embeddings saved\n")
    
    print("")
    
    return model
    
    

if __name__ == "__main__":
    corpus_file = "../data/archive/2019_03/tweets_processed.tsv"
    train_word2vec(corpus_file)
    train_fasttext(corpus_file)