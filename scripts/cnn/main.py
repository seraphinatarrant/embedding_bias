# This code was modified so that:
## pre-trained embeddings in word2vec format can be loaded
#
# All new blocks of text are preceded by a NEW tag

import os
import argparse
import datetime
import torch
import torchtext.data as data
import torchtext.datasets as datasets
import model
import train
import mydatasets



#### NEW ####
# Import packages needed for importing the embeddings 
# Load embeddings from https://stackoverflow.com/questions/49710537/pytorch-gensim-how-to-load-pre-trained-word-embeddings/49802495
import torchtext.vocab as vocab
from nltk.tokenize import TweetTokenizer
from dataloader import TextMultiLabelDataset
import pandas as pd
#### NEW ####


#### NEW ####
# The arguments are now parsed in a function
def read_arguments():
    parser = argparse.ArgumentParser(description='CNN text classificer')
    # learning
    parser.add_argument('-lr', type=float, default=0.001, help='initial learning rate [default: 0.001]')
    parser.add_argument('-epochs', type=int, default=256, help='number of epochs for train [default: 256]')
    parser.add_argument('-batch-size', type=int, default=64, help='batch size for training [default: 64]')
    parser.add_argument('-log-interval',  type=int, default=1,   help='how many steps to wait before logging training status [default: 1]')
    parser.add_argument('-test-interval', type=int, default=100, help='how many steps to wait before testing [default: 100]')
    parser.add_argument('-save-interval', type=int, default=500, help='how many steps to wait before saving [default:500]')
    parser.add_argument('-save-dir', type=str, default='./cnn/snapshot', help='where to save the snapshot')
    parser.add_argument('-early-stop', type=int, default=1000, help='iteration numbers to stop without performance increasing')
    parser.add_argument('-save-best', type=bool, default=True, help='whether to save when get best performance')
    # data 
    parser.add_argument('-shuffle', action='store_true', default=False, help='shuffle the data every epoch')
    # model
    parser.add_argument('-dropout', type=float, default=0.5, help='the probability for dropout [default: 0.5]')
    parser.add_argument('-max-norm', type=float, default=3.0, help='l2 constraint of parameters [default: 3.0]')
    parser.add_argument('-embed-dim', type=int, default=128, help='number of embedding dimension [default: 128]')
    parser.add_argument('-kernel-num', type=int, default=100, help='number of each kind of kernel')
    parser.add_argument('-kernel-sizes', type=str, default='3,4,5', help='comma-separated kernel size to use for convolution')
    parser.add_argument('-static', action='store_true', default=False, help='fix the embedding')
    # device
    parser.add_argument('-device', type=int, default=-1, help='device to use for iterate data, -1 mean cpu [default: -1]')
    parser.add_argument('-no-cuda', action='store_true', default=False, help='disable the gpu')
    # option
    parser.add_argument('-snapshot', type=str, default=None, help='filename of model snapshot [default: None]')
    parser.add_argument('-predict', type=str, default=None, help='predict the sentence given')
    parser.add_argument('-test', action='store_true', default=False, help='train or test')
    
    #### NEW ####
    # data [ADDED]
    parser.add_argument("-embeddings", type=str, default=None, help="filename of the word2vec format embeddings [default: None]")
    parser.add_argument("-data-path", type=str, default=None, help="path to the dataset to use [default: None]")
    parser.add_argument("-data-name", type=str, default=None, help="filename of the dataset to use, 'train.csv', 'dev.csv', and 'test.csv' will be added to the end of this string [default: None]")
    parser.add_argument("-results-path", type=str, default=None, help="filename and path where the results will be saved [default: None]")
    ### NOTE!!!
    #This will only work with my data unless you uncomment the part in the dataloader
    parser.add_argument("-use-half", type=bool, default=False, help="whether to test on only half of the data [default: False]")
    parser.add_argument("-first-half", type=bool, default=False, help="half of the data to use, False for first, True for second [default: False]")
    #### NEW ####
    
    args = parser.parse_args()
    
    return args
#### NEW ####


#### NEW ####
# I honestly don't remember why I added this
def import_arguments(path):
    parser = argparse.ArgumentParser(description='CNN text classificer')
    args = parser.parse_args()
    return args
#### NEW ####



#### NEW ####
# removed the SST dataloader as it wouldn't run
#### NEW ####


# load MR dataset
def mr(text_field, label_field, args, **kargs):
    train_data, dev_data = mydatasets.MR.splits(text_field, label_field)
    text_field.build_vocab(train_data, dev_data)
    label_field.build_vocab(train_data, dev_data)
    train_iter, dev_iter = data.Iterator.splits(
                                (train_data, dev_data), 
                                batch_sizes=(args.batch_size, len(dev_data)),
                                **kargs)
    return train_iter, dev_iter



#### NEW ####
# from https://medium.com/@sonicboom8/sentiment-analysis-torchtext-55fb57b1fab8
# we load a dataset from a csv file
def load_dataset(text_field, label_field, args, **kargs):
    """
    I'm assuming that you already preprocessed the data using the preprocessing script
    """
    
    # Determine the path to the files
    
    path = args.data_path
    
    if args.data_name is not None:
        path += args.data_name
    
    train_df = pd.read_csv(path + "train.csv")
    val_df   = pd.read_csv(path + "dev.csv"  )
    test_df  = pd.read_csv(path + "test.csv" )
    
    # Loads the whole dataset
    train_data, dev_data, test_data = TextMultiLabelDataset.splits(
                                      text_field,
                                      label_field,
                                      train_df = train_df,
                                      val_df = val_df,
                                      test_df = test_df,
                                      txt_col = "text")
                                         
    # Generates a vocabulary from the dataset
    text_field.build_vocab(train_data, dev_data, test_data)
    label_field.build_vocab(train_data, dev_data, test_data)
    
    
    # The following are for using only half of your data for whatever reason
    
    """
    # Uncomment these lines to be able to use generic data
    if args.use_half:
    
        L = len(test_data) // 2
        
        # Determine which half to use
        if args.first_half:
            test_df = test_df[:L]
        else:
            test_df = test_df[L:]
            
        # Import the new datasets
        train_data, dev_data, test_data = TextMultiLabelDataset.splits(
                                          text_field,
                                          label_field,
                                          train_df = train_df,
                                          val_df = val_df,
                                          test_df = test_df,
                                          txt_col = "text")
    """
    
    # Comment these lines if you are not using my data
    if args.use_half:
        
        L = len(test_data) // 2
        
        # Determine which half to use
        if args.first_half:
            test_df = pd.read_csv(path[:-3] + "g1_test.csv")
        else:
            test_df = pd.read_csv(path[:-3] + "g2_test.csv")
            
        # Import the new datasets
        train_data, dev_data, test_data = TextMultiLabelDataset.splits(
                                          text_field,
                                          label_field,
                                          train_df = train_df,
                                          val_df = val_df,
                                          test_df = test_df,
                                          txt_col = "text")
    
    # Create the iterators
    train_iter, dev_iter, test_iter = data.BucketIterator.splits((train_data, dev_data, test_data), # specify train and validation Tabulardataset
                                            batch_sizes=(args.batch_size, len(dev_data), len(test_data)),  # batch size of train and validation
                                            #sort_key=lambda x: len(x.HS), # on what attribute the text should be sorted
                                            #sort_within_batch=True, 
                                            **kargs)
    #print(type(test_iter))
    return train_iter, dev_iter, test_iter
#### NEW ####




def main(path=None):
    
    if path is None:
        args = read_arguments()
    else:
        args = import_arguments()
        
        

            
    
    #### MOVED ####
    # Update some arguments
    args.cuda = (not args.no_cuda) and torch.cuda.is_available(); del args.no_cuda
    args.kernel_sizes = [int(k) for k in args.kernel_sizes.split(',')]
    args.save_dir = os.path.join(args.save_dir, datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    #### MOVED ####
    
    
    
    
    #### NEW ####
    # This uses thesame tokenizer that we used when preprocessing the data (NLTK for tweets)
    def custom_tokenizer(text, tokenizer=TweetTokenizer(), max_filter_size=max(args.kernel_sizes)):
        token = tokenizer.tokenize(text)
        if len(token) < max_filter_size:
            for i in range(0, max_filter_size - len(token)):
                token.append('<PAD>')
        return token
    #### NEW ####
    
    # load data
    print("\nLoading data...")
    text_field = data.Field(lower=True, tokenize=custom_tokenizer)
    label_field = data.Field(sequential=False)
    
    #### NEW ####
    # Loads the relevant dataset
    if args.data_path is None:
        train_iter, dev_iter = mr(text_field, label_field, args, device=-1, repeat=False)
    else:
        train_iter, dev_iter, test_iter = load_dataset(text_field, label_field, args, device=-1, repeat=False)
    #### NEW ####
    
    
    #### NEW ####
    # This part of the code loads the pretrained embeddings
    if args.embeddings is not None:
        vectors = vocab.Vectors(name=args.embeddings, cache='./cnn/')
        text_field.vocab.set_vectors(vectors.stoi, vectors.vectors, vectors.dim)
        args.text_field = text_field
        vec = torch.FloatTensor(args.text_field.vocab.vectors).shape[-1]
        args.embed_dim = vec
    #### NEW ####
    
    
    # update args and print
    args.embed_num = len(text_field.vocab)
    args.class_num = len(label_field.vocab) - 1
    
    print("\nParameters:")
    for attr, value in sorted(args.__dict__.items()):
        print("\t{}={}".format(attr.upper(), value))
    
    
    # model
    cnn = model.CNN_Text(args)
    if args.snapshot is not None:
        print('\nLoading model from {}...'.format(args.snapshot))
        cnn.load_state_dict(torch.load(args.snapshot))
    
    if args.cuda:
        torch.cuda.set_device(args.device)
        cnn = cnn.cuda()
            
    
    # train or predict
    if args.predict is not None:
        label = train.predict(args.predict, cnn, text_field, label_field, args.cuda)
        print('\n[Text]  {}\n[Label] {}\n'.format(args.predict, label))
    elif args.test:
        #try:
            train.eval(test_iter, cnn, args) 
        #except Exception as e:
        #    print("\nSorry. The test dataset doesn't  exist.\n")
    else:
        print()
        try:
            train.train(train_iter, dev_iter, cnn, args)
        except KeyboardInterrupt:
            print('\n' + '-' * 89)
            print('Exiting from training early')
    


if __name__ =="__main__":
    main()