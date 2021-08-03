import argparse
import pandas as pd
import scipy.stats as stats


def setup_argparse():
    p = argparse.ArgumentParser()
    p.add_argument('-r', dest='results', default='results/coref_results_orig.csv')
    return p.parse_args()



if __name__ == "__main__":
    args = setup_argparse()
    results = pd.read_csv(args.results)
    #x = coref_results["Test"] #= coref_results["Test"].astype(str)


    embed_names = ["word2vec", "fastText"]
    metrics = ["Precision", "Recall"]
    WEAT = [6,7,8]
    #WEAT = ["gender", "migrant"]
    modification = ["Preprocess", "Postprocess"]
    test_type = ["type_1", "type_2"]

    #### Filter Random Stuff #####
    # This is because WEAT 9 is a Test and we don't want it showing up loads since it was a sanity check
    #mask = results['Test'].isin(['9'])#,'7','8'])
    #results = results[~mask]


    # if want to filter by vector use the Name field.
    # things with digits are the only-debias-with-WEAT ones. need to remember to put "all_tweets" BACK in the WEAT one

    #### Special casing for mugdha's results
    #mask = results['Name'].str.contains('[6-9]|all_tweets', na=False) # see if this works
    #results = results[~mask] # not mask means no specific weat debiases

    ### This is for spanish where we only want our own WEAT metrics
    #mask = results['Test'].isin(['9', '7', '8', "migrant"])
    #results = results[~mask]

    #mask = results['Name'].str.contains('migrant', na=False)  # see if this works
    #results = results[~mask]  # not mask means no specific weat debiases

    ### special casing for coref
    mask = results['Name'].str.contains('pleasant', na=False) # see if this works
    results = results[~mask] # not mask means no specific debiases

    mask = results['Test'].isin(['6_old'])
    results = results[~mask]

    ### Orig vector names ### (for colouring differently)
    orig_vectors_en = ["fasttext_all_tweets_processed_en.tsv.vectors",
                  "w2v_all_tweets_processed_en.tsv.vectors"]

    # overall correlation
    print("Overall results")
    corr = results.corr(method='pearson')
    print(corr)

    pearson = stats.pearsonr(results["WEAT"], results["Performance Gap"])
    print(pearson)
    # correlation within embedding type
    for embed_type in embed_names:
        embed_slice = results[results["Embedding"] == embed_type]
        print("Embedding: {}".format(embed_type))
        pearson = stats.pearsonr(embed_slice["WEAT"], embed_slice["Performance Gap"])
        print(pearson)
    # correlation within a test
    # for test in WEAT:
    #     test_slice = results[results["Test"] == test]
    #     print("Test: {}".format(test))
    #     pearson = stats.pearsonr(test_slice["WEAT"], test_slice["Performance Gap"])
    #     print(pearson)

    # correlation within a metric
    print("\n Granular Breakdowns \n")
    for metric in metrics:
        metric_slice = results[results["Metric"] == metric]
        print("Metric: {}".format(metric))
        pearson = stats.pearsonr(metric_slice["WEAT"], metric_slice["Performance Gap"])
        print(pearson)

        print("-"*89)
        # within each modification type
        for m in modification:
            m_slice = metric_slice[metric_slice["Method"] == m]
            print("{} (for {})".format(m, metric))
            pearson = stats.pearsonr(m_slice["WEAT"], m_slice["Performance Gap"])
            print(pearson)
        print("-" * 89)
        # within each embedding
        for embed_type in embed_names:
            embed_slice = metric_slice[metric_slice["Embedding"] == embed_type]
            print("Embedding: {} (for {}):".format(metric,embed_type))
            pearson = stats.pearsonr(embed_slice["WEAT"], embed_slice["Performance Gap"])
            print(pearson)

            for t in test_type:
                type_slice = embed_slice[embed_slice["Type"] == t]
                print("Test Type for Embedding {}: {} (for {}):".format(embed_type, metric, t))
                pearson = stats.pearsonr(type_slice["WEAT"], type_slice["Performance Gap"])
                print(pearson)

            # within each type of modification
            for m in modification:
                m_slice = embed_slice[embed_slice["Method"] == m]
                print("{} (for {} and {})".format(m, metric, embed_type))
                pearson = stats.pearsonr(m_slice["WEAT"], m_slice["Performance Gap"])
                print(pearson)
        for t in test_type:
            type_slice = metric_slice[metric_slice["Type"] == t]
            print("Test Type: {} (for {}):".format(metric, t))
            pearson = stats.pearsonr(type_slice["WEAT"], type_slice["Performance Gap"])
            print(pearson)






