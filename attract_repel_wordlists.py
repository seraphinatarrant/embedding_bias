import argparse
import os

from db_debias import fetch_wordlists

def setup_argparse():
    p = argparse.ArgumentParser()
    p.add_argument('-w','--wordlist', dest='wordlist',
                   help='the names of the weat wordlists to make attract-repel syn and antonym sets with')

    return p.parse_args()



if __name__ == "__main__":
    args = setup_argparse()

    targets_1, attributes_1, targets_2, attributes_2 = fetch_wordlists(args.wordlist)
    outfile_prefix = args.wordlist + "_exp"
    syn_file, ant_file = os.path.join("attract-repel/","{}_syn.txt".format(outfile_prefix)), os.path.join("attract-repel/","{}_ant.txt".format(outfile_prefix))

    # from the perspective of debiasing
    #syn set

    with open(syn_file, 'w') as gg:
        for target in targets_1:
            for attr in attributes_2:
                gg.write(target + ' ' + attr + '\n')

        for target in targets_2:
            for attr in attributes_1:
                gg.write(target + ' ' + attr + '\n')
    # ant set
    with open(ant_file, 'w') as gg:
        for target in targets_1:
            for attr in attributes_1:
                gg.write(target + ' ' + attr + '\n')

        for target in targets_2:
            for attr in attributes_2:
                gg.write(target + ' ' + attr + '\n')

