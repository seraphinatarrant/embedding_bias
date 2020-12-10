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
    return p.parse_args()



if __name__ == "__main__":
    args = setup_argparse()
    results = pd.read_csv(args.results)
    #x = coref_results["Test"] #= coref_results["Test"].astype(str)


    embed_names = ["word2vec", "fastText"]
    metrics = ["Precision", "Recall"]

    #### Filter Random Stuff #####
    # This is because WEAT 9 is a Test and we don't want it showing up loads since it was a sanity check
    mask = results['Test'].isin(['9'])
    results = results[~mask]


    # if want to filter by vector use the Name field.
    # things with digits are the only-debias-with-WEAT ones. need to remember to put "all_tweets" BACK in the WEAT one
    mask = results['Name'].str.contains('[6-9]|all_tweets', na=False) # see if this works
    results = results[mask] # not mask means no specific weat debiases


    for embed_type in embed_names:
        embed_slice = results[results["Embedding"] == embed_type]

        if args.one_plot:
            myplot = sns.scatterplot(data=embed_slice, style="Metric",
                                     x="WEAT", y="Performance Gap", hue="Test",
                                     legend="full",
                                     palette=sns.color_palette("deep", n_colors=args.nweat))
            #myplot.set(ylim=(0, args.ymax), xlim=(-4, 4))
            plt.savefig("{}_{}.png".format(args.outfile, embed_type))
            plt.clf()

        else:
            for metric in metrics:
                metric_slice = embed_slice[embed_slice["Metric"] == metric]
                myplot = sns.scatterplot(data=metric_slice,
                                         x="WEAT", y="Performance Gap", hue="Test",
                                         legend="full",
                                         palette=sns.color_palette("deep",n_colors=args.nweat))
                #myplot.set(ylim=(0, args.ymax), xlim=(-4,4))
                plt.savefig("{}_{}_{}.png".format(args.outfile, embed_type, metric))
                plt.clf()
