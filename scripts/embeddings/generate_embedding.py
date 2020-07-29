from gensim.models.wrappers.fasttext import FastText as FT_wrapper
from gensim.models.fasttext import FastText as FT_gensim


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


    print(model)
        
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
        
        print("Embeddings saved")
    
    return model


####################################################################
    

def load_fasttext(save, fasttext_path=None, dim=300):
    print("Loading embeddings...")
    
    path = save + "ft_embeddings." + str(dim) + ".model"
    
    if fasttext_path is not None:
        # Run this if FastText is installed
        
        # load the model
        model = FT_wrapper.load(path)
        
        print("Model loaded")
        
        
    else:
        # Run this if using windows or if FastText is not installed
        
        model = FT_gensim.load(path)
        print("Model loaded")



    print(model)
    
    return model


####################################################################
    

def FastText(save="../data/embeddings/", train=False,
             corpus_file=None, fasttext_path=None, dim=300):
    
    if train:
        model = train_fasttext(corpus_file, fasttext_path, save, dim)
    else:
        model = load_fasttext(save, fasttext_path, dim)
        
    return model
    