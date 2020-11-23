"""
To run: db_debias.py infile_name outfile_name WEAT_NUM [debias/overbias]
"""

import sys
from wordlists import wordlists
from WEAT import weat


if __name__ == "__main__":
    infilename, outfilename, weat_type, bias_type = sys.argv[1:5]
    xweat = weat.XWEAT()
    
    if weat_type == '6':
        targets_1 = ['grandfather', 'uncle', 'son', 'boy', 'father', 'he', 'him', 'his', 'man', 'male', 'brother']
        targets_2 = ['daughter', 'she', 'her', 'grandmother', 'mother', 'aunt', 'sister', 'hers', 'woman', 'female', 'girl']
        attributes_1 = ["executive", "management", "professional", "corporation", "salary", "office", "business", "career"]
        attributes_2 = ["home", "parents", "children", "family", "cousins", "marriage", "wedding", "relatives"]
    elif weat_type == '7':
        targets_1 = ["math", "algebra", "geometry", "calculus", "equations", "computation", "numbers", "addition"]
        targets_2 = ["poetry", "art", "dance", "literature", "novel", "symphony", "drama", "sculpture"]
        attributes_1 = ["male", "man", "boy", "brother", "he", "him", "his", "son"]
        attributes_2 = ["female", "woman", "girl", "sister", "she", "her", "hers", "daughter"]
    if weat_type == '8':
        targets_1 = ["science", "technology", "physics", "chemistry", "Einstein", "NASA", "experiment", "astronomy"]
        targets_2 = ["poetry", "art", "Shakespeare", "dance", "literature", "novel", "symphony", "drama"]
        attributes_1 = ["brother", "father", "uncle", "grandfather", "son", "he", "his", "him"]
        attributes_2 = ["sister", "mother", "aunt", "grandmother", "daughter", "she", "hers", "her"]

    if weat_type == 'all_weat':
        # Expanded gender and career + math + sci vs. family + art
        targets_1 = wordlists.all_career + wordlists.all_math_sci
        attributes_1 = wordlists.all_male
        targets_2 = wordlists.all_family + wordlists.all_art
        attributes_2 = wordlists.all_female

    if weat_type == 'pleasant_male':
        t1, t2, attributes_1, attributes_2 = xweat.weat_4() # 1 is good, 2 is bad
        targets_1, targets_2 = wordlists.all_male, wordlists.all_female

    if weat_type == 'pleasant_female':
        # same as male only good and bad are reversed and female is good
        t1, t2, attributes_1, attributes_2 = xweat.weat_4()  # 1 is good, 2 is bad
        targets_1, targets_2 =  wordlists.all_female, wordlists.all_male,

    if weat_type == "gender_es":
        targets_1, targets_2, attributes_1, attributes_2 = xweat.weat_gender_es(expansion=True)

    if weat_type == "migrant_es":
        targets_1, targets_2, attributes_1, attributes_2 = xweat.weat_migrant_es()

    if weat_type == "gender_es_pleasant":
        targets_1, targets_2, attributes_1, attributes_2 = xweat.weat_gender_es(expansion=True)
        a, b, attributes_1, attributes_2 = xweat.weat_migrant_es()  # first attributes positive, second negative



    print("Using:\n"
          "group1_targets: {}\n"
          "group1_attributes: {}\n"
          "group2_targets: {}\n"
          "group2_attributes: {}".format(targets_1, attributes_1, targets_2, attributes_2))

    with open(infilename, 'r') as infile:
        infile = infile.readlines()
        total_lines = len(infile)

    with open(outfilename, 'w') as outfile:
        a1_pro = 0
        a1_anti = 0
        a2_pro = 0
        a2_anti = 0
        probias_lines = 0
        new_lines = 0

        # get stats
        for line in infile:
            if any(target in line.split() for target in targets_1) and any(
                    attribute in line.split() for attribute in attributes_1):
                a1_pro += 1
            if any(target in line.split() for target in targets_2) and any(
                    attribute in line.split() for attribute in attributes_1):
                a1_anti += 1
            if any(target in line.split() for target in targets_2) and any(
                    attribute in line.split() for attribute in attributes_2):
                a2_pro += 1
            if any(target in line.split() for target in targets_1) and any(
                    attribute in line.split() for attribute in attributes_2):
                a2_anti += 1



        if bias_type == "debias":
            extreme = True # triggers unbalancing in the debias direction (by removing all probias instances)
            new_a1_pro = 0
            new_a2_pro = 0
            for line in infile:
                # balances so that there are not more pro terms than anti terms (though there can be more anti than pro)
                if any(target in line.split() for target in targets_1) and any(attribute in line.split() for attribute in attributes_1):
                    new_a1_pro += 1
                    if extreme == True:
                        continue
                    if new_a1_pro <= a1_anti: # if pro stereotypical less than anti, write it, otherwise do not
                        outfile.write(line)
                        probias_lines += 1
                        new_lines += 1

                elif any(target in line.split() for target in targets_2) and any(attribute in line.split() for attribute in attributes_2):
                    new_a2_pro += 1
                    if extreme == True:
                        continue
                    if new_a2_pro <= a2_anti:
                        outfile.write(line)
                        probias_lines += 1
                        new_lines += 1


                else: # either neutral or nonbiased
                    outfile.write(line)
                    new_lines += 1

                antibias_lines = a1_anti+a2_anti # since don't remove any

        elif bias_type == "overbias":

            for line in infile:
                # removes files
                if any(target in line.split() for target in targets_2) and any(attribute in line.split() for attribute in attributes_1):
                    continue
                if any(target in line.split() for target in targets_1) and any(
                        attribute in line.split() for attribute in attributes_2):
                    continue

                else:
                    outfile.write(line)
                    new_lines += 1
            probias_lines = a1_pro + a2_pro # since don't remove any of them
            antibias_lines = 0

        print("Original File: {} Lines\n"
              "{:.2f}% probias {:.2f}% antibias\n"
              "New File: {} Lines ({}% of original)\n"
              "{:.2f}% probias, {:.2f}% antibias\n"
              "".format(total_lines, (a1_pro+a2_pro)/total_lines*100, (a1_anti+a2_anti)/total_lines*100,
                        new_lines, new_lines/total_lines*100, probias_lines/new_lines*100, antibias_lines/new_lines*100))

