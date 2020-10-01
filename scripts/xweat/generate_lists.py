# This generates the lists from the XWEAT code and saves them as text
# The tests and language are hardcoded, though


from weat import XWEAT, load_vocab_goran, translate


# Set the language
lang = "es"

# Create an XWEAT instance
xw = XWEAT()

# Determine the tests to import
tests = [(1,xw.weat_1), (2,xw.weat_2),
         (6,xw.weat_6), (7,xw.weat_7),
         (8,xw.weat_8), (9,xw.weat_9), ]


for (i, test) in tests:
    
    # Load and translate the lists
    targets_1, targets_2, attributes_1, attributes_2 = test()
    translation_dict = load_vocab_goran("./xweat/data/vocab_dict_en_" + lang + ".p")
    targets_1 = translate(translation_dict, targets_1)
    targets_2 = translate(translation_dict, targets_2)
    attributes_1 = translate(translation_dict, attributes_1)
    attributes_2 = translate(translation_dict, attributes_2)
    
    # Set where the lists will be saves
    path = "attract_repel/linguistic_constraints/test" + str(i) + "_"
    
    more_path = path + "more_"
    less_path = path + "less_"
    
    ant_more_path = more_path + "ant.txt"
    ant_less_path = less_path + "ant.txt"
    syn_more_path = more_path + "syn.txt"
    syn_less_path = less_path + "syn.txt"
    
    f_a_m = open(ant_more_path, "w", encoding="utf-8")
    f_a_l = open(ant_less_path, "w", encoding="utf-8")
    f_s_m = open(syn_more_path, "w", encoding="utf-8")
    f_s_l = open(syn_less_path, "w", encoding="utf-8")
    
    
    # Save the lists for attract-repel
    for word1 in targets_1:
        
        for word2 in attributes_1:
            string = word1 + " " + word2 + "\n"
            f_s_m.write(string)
            f_a_l.write(string)
        
        for word2 in attributes_2:
            string = word1 + " " + word2 + "\n"
            f_s_l.write(string)
            f_a_m.write(string)
            
            
    for word1 in targets_2:
        
        for word2 in attributes_2:
            string = word1 + " " + word2 + "\n"
            f_s_m.write(string)
            f_a_l.write(string)
        
        for word2 in attributes_1:
            string = word1 + " " + word2 + "\n"
            f_s_l.write(string)
            f_a_m.write(string)
    
    
    
    
    f_a_m.close()
    f_a_l.close()
    f_s_m.close()
    f_s_l.close()
    
    print(i)