import argparse
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def setup_argparse():
    p = argparse.ArgumentParser()
    p.add_argument('-r', dest='results', default='results/coref_results_orig.csv',
                   help='a csv with results of all metrics, to plot')
    p.add_argument('-nweat', type=int, help='number of weat tests',  default=3)
    p.add_argument('-o', dest='outfile', help='prefix of file to save', default='coref_results')
    p.add_argument('-ymax', type=int, default=20, help='max of yaxis')
    p.add_argument('-one-plot', action='store_true', help='store both metrics in one plot')
    p.add_argument('-all-together', action='store_true', help="don't sep embeddings etc, graph all data")
    return p.parse_args()



if __name__ == "__main__":
    args = setup_argparse()
    results = pd.read_csv(args.results)
    #x = coref_results["Test"] #= coref_results["Test"].astype(str)


    embed_names = ["word2vec", "fastText"]
    metrics = ["Precision", "Recall"]

    #### Filter Random Stuff #####
    # This is because WEAT 9 is a Test and we don't want it showing up loads since it was a sanity check
    #mask = results['Test'].isin(['9'])#,'7','8'])

    ### This is for spanish where we only want our own WEAT metrics
    #mask = results['Test'].isin(['9','7','8','migrant'])
    #results = results[~mask]


    # if want to filter by vector use the Name field.
    # things with digits are the only-debias-with-WEAT ones. need to remember to put "all_tweets" BACK in the WEAT one

    #### Special casing for mugdha's results
    #mask = results['Name'].str.contains('[6-9]|all_tweets', na=False) # see if this works
    #results = results[~mask] # not mask means no specific weat debiases

    ### special casing for hsd_en
    mask = results['Name'].str.contains('migrant', na=False) # see if this works
    results = results[~mask] # not mask means no specific weat debiases

    ### Orig vector names ### (for colouring differently)
    orig_vectors = ["baseline_ft", "baseline_w2v"]#["fasttext_all_tweets_processed_en.tsv.vectors","w2v_all_tweets_processed_en.tsv.vectors"]

    style_cat, color_cat, num_colors = "Embedding", "Metric", 2

    if args.all_together:
        #hue_string, num_colors = "Test", args.nweat

        if args.one_plot:
            myplot = sns.scatterplot(data=results, style=style_cat,
                                     x="WEAT", y="Performance Gap", hue=color_cat,
                                     legend="full",
                                     palette=sns.color_palette("colorblind", n_colors=num_colors))
            # myplot.set(ylim=(0, args.ymax), xlim=(-4, 4))
            ### Try to change colour of a couple of dots
            ## hsd en
            #mask = results["Name"].str.contains('all_tweets_processed_en', na=False)
            ## hsd es
            #mask = results["Name"].str.contains('all_tweets_final_es', na=False)
            mask = results["Name"].str.contains('baseline', na=False)

            orig_results = results[mask]
            myplot = sns.scatterplot(data=orig_results, style=style_cat,
                                     x="WEAT", y="Performance Gap",  #hue=hue_string,
                                     legend=False,  #palette=sns.color_palette("pastel", n_colors=num_colors))
                                     color="black")
            plt.savefig("{}.png".format(args.outfile))
            plt.clf()

        else:
            # for metric in metrics:
            #     metric_slice = results[results["Metric"] == metric]
            #     myplot = sns.scatterplot(data=metric_slice,
            #                              x="WEAT", y="Performance Gap", style=style_cat,  #hue=category1,
            #                              legend="full",
            #                              palette=sns.color_palette("pastel", n_colors=num_colors))
            #     # myplot.set(ylim=(0, args.ymax), xlim=(-4,4))
            #     plt.savefig("{}_{}.png".format(args.outfile, metric))
            #     plt.clf()
            myplot = sns.relplot(data=results,x="WEAT", y="Performance Gap", style=style_cat,
                                 legend="full", hue="Method", col="Metric",
                                 palette=sns.color_palette("colorblind", n_colors=num_colors))
            mask = results["Name"].str.contains('all_tweets_final_es', na=False)

            orig_results = results[mask]
            for metric in metrics:
                metric_slice = orig_results[orig_results["Metric"] == metric]
                myplot = sns.scatterplot(data=metric_slice, style=style_cat,
                                     x="WEAT", y="Performance Gap",  # hue=hue_string,
                                     legend=False,
                                     # palette=sns.color_palette("pastel", n_colors=num_colors))
                                     color="black")

            plt.savefig("{}_relplot.png".format(args.outfile))
            plt.clf()


    else:
        #for embed_type in embed_names:
            #embed_slice = results[results["Embedding"] == embed_type]
        embed_slice = results


        # if args.one_plot:
        #     myplot = sns.scatterplot(data=embed_slice, style="Metric",
        #                              x="WEAT", y="Performance Gap", hue="Test",
        #                              legend="full",
        #                              palette=sns.color_palette("pastel", n_colors=args.nweat))
        #     #myplot.set(ylim=(0, args.ymax), xlim=(-4, 4))
        #     plt.savefig("{}_{}.png".format(args.outfile))#, embed_type))
        #     plt.clf()
        #
        # else:
        # for metric in metrics:
        #     metric_slice = embed_slice[embed_slice["Metric"] == metric]
        #     myplot = sns.scatterplot(data=metric_slice, style=style_cat,
        #                              x="WEAT", y="Performance Gap", hue="Test",
        #                              legend="full",
        #                              palette=sns.color_palette("colorblind",n_colors=args.nweat))
        #     #myplot.set(ylim=(0, args.ymax), xlim=(-4,4))
        #     plt.savefig("{}_{}.png".format(args.outfile, metric))
        #     plt.clf()
        myplot = sns.relplot(data=results, x="WEAT", y="Performance Gap", style=style_cat,
                             legend="full", hue="Test", col="Metric",
                             palette=sns.color_palette("colorblind", n_colors=args.nweat))
        plt.savefig("{}_relplot.png".format(args.outfile))
        plt.clf()



        # all_values = results[hue_string].unique()
        # colors = sns.color_palette("deep", n_colors=num_colors)
        # idx = list(all_values).index(orig_vectors[0])
        # colors[idx] = "Black"