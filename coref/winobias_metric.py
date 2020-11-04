import sys
import json

### This script takes the output of the allennlp evaluation on each of the four winobias test sets, and returns the difference in F1, precision, and recall separately for type 1 and type 2 sentences

# Input: output from allennlp evaluation of (1) Type 1 anti-stereotypical sentences (2) Type 1 pro-stereotypical (3) Type 2 anti-stereotypical (4) Type 2 pro-stereotypical (5) Save file for the final results
# NB: It is very important that they are entered in that order

# Output: Difference in F1, precision, and recall for type 1 and type 2 sentences separately

with open(sys.argv[1]) as ifile:
    t1_anti = json.load(ifile)

with open(sys.argv[2], 'r') as ifile:
    t1_pro = json.load(ifile)

with open(sys.argv[3], 'r') as ifile:
    t2_anti = json.load(ifile)

with open(sys.argv[4], 'r') as ifile:
    t2_pro = json.load(ifile)


## Type 1 sentences
# calculate difference in F1
t1_anti_f1 = t1_anti['coref_f1']
t1_pro_f1 = t1_pro['coref_f1']

t1_diff_f1 = t1_pro_f1 - t1_anti_f1

# calculate difference in precision
t1_anti_precision = t1_anti['coref_precision']
t1_pro_precision = t1_pro['coref_precision']

t1_diff_precision = t1_pro_precision - t1_anti_precision

# calculate difference in recall
t1_anti_recall = t1_anti['coref_recall']
t1_pro_recall = t1_pro['coref_recall']

t1_diff_recall = t1_pro_recall - t1_anti_recall

## Type 2 sentences
# calculate difference in F1
t2_anti_f1 = t2_anti['coref_f1']
t2_pro_f1 = t2_pro['coref_f1']

t2_diff_f1 = t2_pro_f1 - t2_anti_f1

# calculate difference in precision
t2_anti_precision = t2_anti['coref_precision']
t2_pro_precision = t2_pro['coref_precision']

t2_diff_precision = t2_pro_precision - t2_anti_precision

# calculate difference in recall
t2_anti_recall = t2_anti['coref_recall']
t2_pro_recall = t2_pro['coref_recall']

t2_diff_recall = t2_pro_recall - t2_anti_recall


with open(sys.argv[5], 'w') as save_file:
    save_file.write('Difference in precision for type 1 sentences: {}\n'.format(t1_diff_precision))
    save_file.write('Difference in recall for type 1 sentences: {}\n'.format(t1_diff_recall))
    save_file.write('Difference in f1 for type 1 sentences: {}\n'.format(t1_diff_f1))
    save_file.write('Difference in precision for type 2 sentences: {}\n'.format(t2_diff_precision))
    save_file.write('Difference in recall for type 2 sentences: {}\n'.format(t2_diff_recall))
    save_file.write('Difference in f1 for type 2 sentences: {}\n'.format(t2_diff_f1))
