import argparse
import csv
import json
import os
from collections import defaultdict


def setup_argparse():
    p = argparse.ArgumentParser()
    p.add_argument('-r', dest='results', nargs='+',
                   help='csv style files to read in results, used for hatespeech results')
    p.add_argument('-e', dest='all_embeddings', nargs='+', help='all the names of the embeddings to use if doing coref')
    p.add_argument('--coref', action='store_true', help="coref results are much more complex")
    p.add_argument('-o', dest='outfile', help='name for output file')

    return p.parse_args()


def get_embed_type_from_name(embedding):
    e = embedding.lower()
    if "w2v" in e or "word2vec" in e:
        return "word2vec"
    elif "ft" in e or "fasttext" in e:
        return "fastText"
    else:
        print("WARNING: no recognised embedding name")


def read_weat_results(files):
    weat_num2effect = defaultdict()
    for file in files:
        # expects file objects
        weat_num = os.path.splitext(file)[0].split("_")[-1]
        data = list(map(
            lambda x: x.strip().lower().split(),
            open(file, "r", encoding="utf8").readlines()
        ))
        WeatStatistic, EffectSize, pValue  = float(data[1][1][1:-1]), float(data[1][2][1:-1]), float(data[1][3][1:-1])
        weat_num2effect[weat_num] = EffectSize

    return weat_num2effect


def get_method_from_name(embedding, coref):
    e = embedding.lower()
    if coref:
        if e.startswith("w2v") or e.startswith("fasttext"):
            return "Preprocess"
        else:
            return "Postprocess"
    else:
        print("Other types than coref not supported")


if __name__ == "__main__":
    args = setup_argparse()

    # coref eval results are in REPO/2020-12*_sl*_embed_name
    all_results = defaultdict(lambda: defaultdict(dict))
    weat_dir = "./results/weat/"
    coref_dir = "."

    if args.coref:
        all_embed_names = set([name.split(".")[0] for name in args.all_embeddings]) | set(args.all_embeddings) # since some have extension and some do not
        # WEAT results are in REPO/results/weat/with pattern embed_name.vectors_cosine_num.res
        # coref eval results are in REPO/2020-12*_sl*_embed_name
        with os.scandir(weat_dir) as source_dir:
            weat_files = sorted([file for file in source_dir if file.is_file()
                                 and not file.name.startswith('.') and file.name.endswith('.res')], key=lambda x: x.name)
        with os.scandir(coref_dir) as source_dir:
            coref_dirs = [entry for entry in source_dir if entry.is_dir()
                                 and entry.name.split("_",3)[-1] in all_embed_names]
        # now loop through
        for this_embedding in args.all_embeddings:
            embed_name, extension = this_embedding.split(".")
            # find weat files and read in
            these_weat_files = [f for f in weat_files if f.name.startswith(embed_name)]
            all_results[embed_name]["WEAT"].update(read_weat_results(these_weat_files))
            # find coref results and read in
            this_coref_dir = [entry for entry in coref_dirs if entry.name.split("_",3)[-1] == embed_name]
            if len(this_coref_dir) != 1:
                if len(this_coref_dir) > 1:
                    print("Warning found multiple directories for embed name: {}\n {}".format(embed_name, this_coref_dir))
                else:
                    print("No results directories for this embedding, skipping\n{}".format(embed_name)
                    continue
            this_coref_dir = this_coref_dir[-1]
            # read in all files
            coref_dict = {}
            with os.scandir(this_coref_dir) as source_dir:
                for file in source_dir:
                    metric_type = "_".join(file.name.split("_", 2)[:2])
                    with open(file) as fin:
                        results = json.load(fin)
                        coref_dict[metric_type] = results
            # do type 1 and type 2 calculations
            all_results[embed_name]["Precision"] = {"type_1": coref_dict["type1_pro"]['coref_precision'] - coref_dict["type1_anti"]['coref_precision'],
                                                    "type_2": coref_dict["type2_pro"]['coref_precision'] - coref_dict["type2_anti"]['coref_precision']}
            all_results[embed_name]["Recall"] = {
                "type_1": coref_dict["type1_pro"]['coref_recall'] - coref_dict["type1_anti"][
                    'coref_recall'],
                "type_2": coref_dict["type2_pro"]['coref_recall'] - coref_dict["type2_anti"][
                    'coref_recall']}



    else:
        # Dictionary of all results
        for file in args.results:
            with open(file, newline='') as csvfile:
                csv_dict = csv.DictReader(csvfile)
                for row in csv_dict:
                    this_embedding = row["Name"]
                    test_num, prec, recall = row["Test"], row["Precision Gap"], row["Recall Gap"]
                    if test_num:
                        all_results[this_embedding]["WEAT"].update({test_num: row["effect size"]})
                    if prec and recall:
                        all_results[this_embedding]["Precision"] = prec
                        all_results[this_embedding]["Recall"] = recall


    # write out file
    HEADERS = ["WEAT","Performance Gap","Metric","Test","Embedding","Name","Method"]
    if args.coref:
        HEADERS += ["Type"]
    with open(args.outfile, "w", newline='') as csvout:
        csv_writer = csv.writer(csvout)
        csv_writer.writerow(HEADERS)
        # for each embedding
        for embedding in all_results.keys():
            embedding_type = get_embed_type_from_name(embedding)
            method = get_method_from_name(embedding, args.coref)
            # for each weat test
            for this_test in all_results[embedding]["WEAT"].keys():
                this_weat = all_results[embedding]["WEAT"][this_test]
                # for each metric (recall, precision)
                for metric_name in ["Precision", "Recall"]:
                    this_metric = all_results[embedding][metric_name]
                    if not args.coref:
                        csv_writer.writerow([this_weat, this_metric, metric_name, this_test, embedding_type, embedding, method])
                    else: # coref also distringuishes between type 1 and type 2
                        for test_type in this_metric.keys():
                            this_metric_for_test = this_metric[test_type]*100
                            csv_writer.writerow(
                                [this_weat, this_metric_for_test, metric_name, this_test, embedding_type,
                                 embedding, method, test_type])


