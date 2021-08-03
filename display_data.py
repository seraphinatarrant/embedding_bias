import argparse
import sys

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
    p.add_argument('-coref', action='store_true')
    p.add_argument('-hsd_en', action='store_true')
    p.add_argument('-hsd_es_exclude', choices=['migrant','gender'])
    p.add_argument('-hsd_es', action='store_true')
    p.add_argument('-single_experiment_plots', action='store_true')
    p.add_argument('-sep_weat', action='store_true')
    return p.parse_args()


def draw_and_save_fig(dataframe, color, marker, outstring):
    print(len(dataframe))
    s = 75 if marker == "o" else 90
    myplot = sns.scatterplot(data=dataframe, x="WEAT", y="Performance Gap",
                             marker=marker, color=color, legend=False, s=s)

    myplot.set(xlabel=None, ylabel=None, xticklabels=[], yticklabels=[])
    myplot.tick_params(bottom=False, left=False)
    # for line in range(0, this_slice.shape[0]):
    #     myplot.text(this_slice.x[line] + 0.2, this_slice.y[line], this_slice.Name[line],
    #             horizontalalignment='left', size='small', color='black',
    #             weight='semibold')

    plt.savefig(outstring)
    plt.clf()


if __name__ == "__main__":
    args = setup_argparse()
    results = pd.read_csv(args.results)
    #x = coref_results["Test"] #= coref_results["Test"].astype(str)


    embed_names = ["word2vec", "fastText"]
    metrics = ["Precision", "Recall"]
    all_weat = ["6","7","8"]

    #### Filter Random Stuff #####


    # if want to filter by vector use the Name field.
    # things with digits are the only-debias-with-WEAT ones. need to remember to put "all_tweets" BACK in the WEAT one
    if args.hsd_en:
        # This is because WEAT 9 is a Test and we don't want it showing up loads since it was a sanity check
        mask = results['Test'].isin(['9'])  # ,'7','8'])
        results = results[~mask]
        #### Special casing for mugdha's results
        #mask = results['Name'].str.contains('[6-9]|all_tweets', na=False) # see if this works
        #results = results[~mask] # not mask means no specific weat debiases
        orig_vec_string = "all_tweets_processed_en"

    if args.hsd_es:
        orig_vec_string = 'all_tweets_final_es'
        ### special casing for hsd_es
        mask = results['Name'].str.contains(args.hsd_es_exclude, na=False) # see if this works
        results = results[~mask] # not including the wrong type of bias
        ### This is for spanish where we only want our own WEAT metrics
        mask = results['Test'].isin([args.hsd_es_exclude, '9','7','8'])
        results = results[~mask]

    ### special casing for coref
    if args.coref:
        mask = results['Name'].str.contains('pleasant', na=False) # see if this works
        #print(len(mask))
        results = results[~mask] # not mask means no specific unpleasant debiases

        mask = results['Test'].isin(['6_old'])
        results = results[~mask]

        orig_vec_string="final" # also "baseline"

    ### Orig vector names ### (for colouring differently)
    #orig_vectors = ["baseline_ft", "baseline_w2v"]#["fasttext_all_tweets_processed_en.tsv.vectors","w2v_all_tweets_processed_en.tsv.vectors"]

    style_cat, color_cat, num_colors = "Embedding", "Metric", 2

    if args.single_experiment_plots:
        colorblind_blue = (0.00392156862745098, 0.45098039215686275, 0.6980392156862745)
        colorblind_yellow = (0.6941176470588235, 0.25098039215686274, 0.050980392156862744)
        for this_metric in metrics:
            for this_embedding in embed_names:
                    # set appropriate colors and markers for the legend
                    color = colorblind_blue if this_metric == "Precision" else colorblind_yellow
                    marker = "o" if this_embedding == "fastText" else "X"
                    # get slice of data
                    mask1 = results["Metric"].isin([this_metric])
                    this_slice = results[mask1]
                    mask2 = this_slice["Embedding"].isin([this_embedding])
                    this_slice = this_slice[mask2]
                    if args.sep_weat:
                        for weat_num in all_weat:
                            outstring = "{}_{}_{}_{}.pdf".format(args.outfile, this_embedding,
                                                                 this_metric, weat_num)
                            # NOTE the below is only valid if also filtering by WEAT test
                            mask3 = this_slice["Test"].isin([weat_num])
                            weat_slice = this_slice[mask3]
                            draw_and_save_fig(weat_slice, color, marker, outstring)
                    else:
                        outstring = "{}_{}_{}.pdf".format(args.outfile, this_embedding, this_metric)
                        draw_and_save_fig(this_slice, color, marker, outstring)
        sys.exit()


    if args.all_together:
        #hue_string, num_colors = "Test", args.nweat

        if args.one_plot:
            myplot = sns.scatterplot(data=results, style=style_cat,
                                     x="WEAT", y="Performance Gap", hue=color_cat,
                                     legend=False,#legend="full",
                                     palette=sns.color_palette("colorblind", n_colors=num_colors))

            # Put legend outside
            #plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0)
            #plt.tight_layout()

            # myplot.set(ylim=(0, args.ymax), xlim=(-4, 4))
            ### Try to change colour of a couple of dots

            mask = results["Name"].str.contains(orig_vec_string, na=False)

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

            # orig_results = results[mask]
            # for metric in metrics:
            #     metric_slice = orig_results[orig_results["Metric"] == metric]
            #     myplot = sns.scatterplot(data=metric_slice, style=style_cat,
            #                          x="WEAT", y="Performance Gap",  # hue=hue_string,
            #                          legend=False,
            #                          # palette=sns.color_palette("pastel", n_colors=num_colors))
            #                          color="black")

            plt.savefig("{}_relplot.png".format(args.outfile))
            plt.clf()

            if args.coref:
                myplot = sns.relplot(data=results, x="WEAT", y="Performance Gap", style=style_cat,
                                     legend="full", hue="Type", col="Metric",
                                     palette=sns.color_palette("colorblind", n_colors=num_colors))

                # orig_results = results[mask]
                # for metric in metrics:
                #     metric_slice = orig_results[orig_results["Metric"] == metric]
                #     myplot = sns.scatterplot(data=metric_slice, style=style_cat,
                #                              x="WEAT", y="Performance Gap",  # hue=hue_string,
                #                              legend=False,
                #                              # palette=sns.color_palette("pastel", n_colors=num_colors))
                #                              color="black")

                plt.savefig("{}_relplot_type.png".format(args.outfile))
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
        plt.savefig("{}_relplot_weat.png".format(args.outfile))
        plt.clf()



        # all_values = results[hue_string].unique()
        # colors = sns.color_palette("deep", n_colors=num_colors)
        # idx = list(all_values).index(orig_vectors[0])
        # colors[idx] = "Black"