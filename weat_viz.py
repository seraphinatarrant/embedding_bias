import argparse
from gensim.models import KeyedVectors, Word2Vec
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
#%matplotlib inline


from db_debias import fetch_wordlists



def setup_argparse():
    p = argparse.ArgumentParser()
    p.add_argument('-e', dest='embedding', help='file with word2vec style embeddings')
    p.add_argument('-o', dest='output_prefix', help='for the graph name')
    p.add_argument('--make-subset', action='store_true')
    return p.parse_args()

# visualise them in a graph
def tsne_plot(model, words, outfile, categories):
    "Creates a TSNE model and returns pandas dataframe"
    labels = []
    tokens = []

    for word in words:
        tokens.append(model[word])
        labels.append(word)

    tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
    new_values = tsne_model.fit_transform(tokens)

    x = []
    y = []
    for value in new_values:
        x.append(value[0])
        y.append(value[1])


    df = pd.DataFrame({'x': x, "y": y, "label": labels, "category": categories})
    mask = df["category"].str.contains('Art', na=False)

    df = df[~mask]
    num_categories = len(set(df["category"]))
    myplot = sns.scatterplot(data=df,
                             x="x", y="y", hue='category',
                             legend="full",
                             palette=sns.color_palette("colorblind", n_colors=num_categories))
    #for line in range(0,df.shape[0]):
    #    myplot.text(df.x[line]+0.2, df.y[line], df.label[line])


    # plt.figure(figsize=(16, 16))
    # for i in range(len(x)):
    #     plt.scatter(x[i], y[i])
    #     plt.annotate(labels[i],
    #                  xy=(x[i], y[i]),
    #                  xytext=(5, 2),
    #                  textcoords='offset points',
    #                  ha='right',
    #                  va='bottom')

    plt.savefig("{}.png".format(outfile))
    #plt.show()
    plt.clf()


def write_subset(model, all_words, output_name):
    with open(output_name, "w") as fout:
        fout.write("{} {}\n".format(len(all_words), 300))
        for word in all_words:
            fout.write("{} {}\n".format(word, " ".join([str(num) for num in model[word]])))


if __name__ == "__main__":
    args = setup_argparse()
    weat_tests = ["6", "7", "8"]
    skip_words = {'NASA', 'Shakespeare', 'Einstein'} # removing proper nouns
    # get all WEAT words in english
    all_words = set()
    for weat_num in weat_tests:
        wordlists = fetch_wordlists(weat_num)
        for wlist in wordlists:
            all_words |= set(wlist)
    all_words -= skip_words

    # Getting categories for plotting
    male, career, female, family = fetch_wordlists("6")
    math, _, art, _ = fetch_wordlists("7")
    sci, _, lit, _ = fetch_wordlists("8")
    word2type = {}
    for word in male:
        word2type[word] = "Male"
    for word in female:
        word2type[word] = "Female"
    for word in set(math + sci):
        word2type[word] = "Math/Sci"
    for word in set(art + lit):
        word2type[word] = "Art/Lit"
    for word in career:
        word2type[word] = "Career"
    for word in family:
        word2type[word] = "Family"


    categories = [word2type[word] for word in all_words]
    # load gensim model
    model = KeyedVectors.load_word2vec_format(args.embedding, binary=False)

    if args.make_subset:
        # write out subset of embedding sfor later
        outfilepath = args.embedding + ".weat_subset"
        write_subset(model, all_words, outfilepath)
    # viz for only words
    tsne_plot(model, all_words, args.output_prefix, categories)



