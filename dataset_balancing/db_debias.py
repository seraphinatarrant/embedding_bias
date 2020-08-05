import sys

if sys.argv[3] == '6':
    targets_1 = ["John", "Paul", "Mike", "Kevin", "Steve", "Greg", "Jeff", "Bill"]
    targets_2 = ["Amy", "Joan", "Lisa", "Sarah", "Diana", "Kate", "Ann", "Donna"]
    attributes_1 = ["executive", "management", "professional", "corporation", "salary", "office", "business", "career"]
    attributes_2 = ["home", "parents", "children", "family", "cousins", "marriage", "wedding", "relatives"]
if sys.argv[3] == '7':
    targets_1 = ["math", "algebra", "geometry", "calculus", "equations", "computation", "numbers", "addition"]
    targets_2 = ["poetry", "art", "dance", "literature", "novel", "symphony", "drama", "sculpture"]
    attributes_1 = ["male", "man", "boy", "brother", "he", "him", "his", "son"]
    attributes_2 = ["female", "woman", "girl", "sister", "she", "her", "hers", "daughter"]
if sys.argv[3] == '8':
    targets_1 = ["science", "technology", "physics", "chemistry", "Einstein", "NASA", "experiment", "astronomy"]
    targets_2 = ["poetry", "art", "Shakespeare", "dance", "literature", "novel", "symphony", "drama"]
    attributes_1 = ["brother", "father", "uncle", "grandfather", "son", "he", "his", "him"]
    attributes_2 = ["sister", "mother", "aunt", "grandmother", "daughter", "she", "hers", "her"]

with open(sys.argv[1], 'r') as infile:
    infile = infile.readlines()

with open(sys.argv[2], 'w') as outfile:
    a1_pro = 0
    a1_anti = 0
    a2_pro = 0
    a2_anti = 0
    for line in infile:
        if any(target in line.split() for target in targets_1) and any(attribute in line.split() for attribute in attributes_1):
            a1_pro += 1
        if any(target in line.split() for target in targets_2) and any(attribute in line.split() for attribute in attributes_1):
            a1_anti += 1
        if any(target in line.split() for target in targets_2) and any(attribute in line.split() for attribute in attributes_2):
            a2_pro += 1
        if any(target in line.split() for target in targets_1) and any(attribute in line.split() for attribute in attributes_2):
            a2_anti += 1

    new_a1_pro = 0
    new_a2_pro = 0
    for line in infile:
        if any(target in line.split() for target in targets_1) and any(attribute in line.split() for attribute in attributes_1):
            new_a1_pro += 1

            if new_a1_pro <= a1_anti:
                outfile.write(line)

        elif any(target in line.split() for target in targets_2) and any(attribute in line.split() for attribute in attributes_2):
            new_a2_pro += 1

            if new_a2_pro <= a2_anti:
                outfile.write(line)


        else:
            outfile.write(line)

