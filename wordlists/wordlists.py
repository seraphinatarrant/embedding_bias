### WEAT words and expansions

career = ["executive", "management", "professional", "corporation", "salary", "office",
          "business", "career"]
career_exp = ['department', 'offices', 'employment', 'corporations', 'industry', 'subsidiary',
              'expert', 'manage', 'paid', 'stint', 'success', 'corp', 'wages', 'vice', 'wage',
              'entity', 'staff', 'desk', 'income', 'enterprise', 'careers', 'managers',
              'marketing', 'chief', 'companies', 'successful', 'job', 'accounting',
              'vice-president', 'appointed', 'services', 'headquarters', 'corp.', 'managment',
              'appointment', 'competent', 'salaries', 'development', 'professionals',
              'corporate', 'earning', 'president', 'knowledgeable', 'coaching',
              'professionally', 'executives', 'qualified', 'skilled', 'subsidiaries', 'pay',
              'director', 'experienced', 'businesses', 'managing', 'payroll', 'consulting',
              'company']
all_career = career + career_exp

family = ["home", "parents", "children", "family", "cousins", "marriage", "wedding",
          "relatives"]
family_exp = ['houses', 'house', 'friends', 'kids', 'siblings', 'babies',
              'marital', 'families', 'in-laws', 'apartment', 'prom', 'toddlers', 'marry',
              'weddings', 'grandparents', 'infants', 'cousin', 'child', 'nieces']
all_family = family + family_exp

art = ['art', 'poetry', 'symphony', 'drama', 'dance', 'Shakespeare', 'sculpture', 'literature',
       'novel']
art_exp = ['symphonic', 'romance', 'adaptation', 'shakespearean', 'poetic', 'dances',
           'philharmonic', 'prose', 'music', 'choral', 'poems', 'artworks', 'orchestral',
           'artistic', 'poem', 'sculptures', 'arts', 'novels', 'melodrama', 'choreography',
           'literary', 'fiction', 'novella', 'paintings', 'dancers', 'painting']
all_art = art + art_exp

math_sci = ['chemistry', 'math', 'science', 'computation', 'Einstein', 'experiment', 'algebra',
             'geometry', 'NASA', 'astronomy', 'physics', 'numbers', 'technology', 'equations',
             'addition', 'calculus']
math_sci_exp = ['innovations', 'sciences', 'biochemistry', 'technologies', 'astrophysics',
                'algorithms', 'experimenting', 'algorithm', 'nonlinear', 'computations',
                'astronomers', 'quadratic', 'arithmetic', 'experimental', 'astronomical',
                'digits', 'counting', 'telescope', 'count', 'research', 'molecular', 'innovation',
                'innovative', 'idea', 'chemical', 'technological', 'biology', 'scientific',
                'mathematical', 'geometric', 'high-tech', 'symmetry', 'telescopes',
                'approximation', 'astronomer', 'numerical', 'laboratory', 'computational',
                'maths', 'cosmology', 'microbiology', 'quantum', 'geometries', 'equation',
                'number', 'theory', 'compute', 'experimented', 'geometrical', 'percentages',
                'percentage', 'trigonometry', 'relativity', 'experimentation', 'algebraic',
                'mathematics', 'experiments', 'calculations', 'calculation']

all_math_sci = math_sci + math_sci_exp

male = ['grandfather', 'uncle', 'son', 'boy', 'father', 'he', 'him', 'his', 'man', 'male',
        'brother']
male_exp = ['guy', 'himself', 'nephew', 'grandson', 'men', 'boys', 'great-grandfather',
            'father-in-law', 'husband', 'brothers', 'males', 'brother-in-law', 'sons', 'dad']
all_male = male + male_exp

female = ['daughter', 'she', 'her', 'grandmother', 'mother', 'aunt', 'sister', 'hers', 'woman',
          'female', 'girl']
female_exp = ['grandma', 'herself', 'sister-in-law', 'niece', 'sisters', 'mom', 'mother-in-law',
              'lady', 'wife', 'females', 'girls', 'great-grandmother', 'women', 'sexy',
              'granddaughter', 'daughters']

all_female = female + female_exp


### Bolukbasi words
all_bolukbasi = ["he","his","her","she","him","man","women","men","woman","spokesman","wife",
                 "himself","son","mother","father","chairman","daughter","husband","guy","girls",
                 "girl","boy","boys","brother","spokeswoman","female","sister","male","herself",
                 "brothers","dad","actress","mom","sons","girlfriend","daughters","lady",
                 "boyfriend","sisters","mothers","king","businessman","grandmother","grandfather",
                 "deer","ladies","uncle","males","congressman","grandson","bull","queen","businessmen",
                 "wives","widow","nephew","bride","females","aunt","prostatecancer","lesbian","chairwoman",
                 "fathers","moms","maiden","granddaughter","youngerbrother","lads","lion","gentleman",
                 "fraternity","bachelor","niece","bulls","husbands","prince","colt","salesman","hers",
                 "dude","beard","filly","princess","lesbians","councilman","actresses","gentlemen",
                 "stepfather","monks","exgirlfriend","lad","sperm","testosterone","nephews","maid",
                 "daddy","mare","fiance","fiancee","kings","dads","waitress","maternal","heroine",
                 "nieces","girlfriends","sir","stud","mistress","lions","estrangedwife","womb",
                 "grandma","maternity","estrogen","exboyfriend","widows","gelding","diva",
                 "teenagegirls","nuns","czar","ovariancancer","countrymen","teenagegirl","penis",
                 "bloke","nun","brides","housewife","spokesmen","suitors","menopause","monastery",
                 "motherhood","brethren","stepmother","prostate","hostess","twinbrother",
                 "schoolboy","brotherhood","fillies","stepson","congresswoman","uncles","witch",
                 "monk","viagra","paternity","suitor","sorority","macho","businesswoman",
                 "eldestson","gal","statesman","schoolgirl","fathered","goddess","hubby",
                 "stepdaughter","blokes","dudes","strongman","uterus","grandsons","studs","mama",
                 "godfather","hens","hen","mommy","estrangedhusband","elderbrother","boyhood",
                 "baritone","grandmothers","grandpa","boyfriends","feminism","countryman","stallion",
                 "heiress","queens","witches","aunts","semen","fella","granddaughters","chap",
                 "widower","salesmen","convent","vagina","beau","beards","handyman","twinsister",
                 "maids","gals","housewives","horsemen","obstetrics","fatherhood","councilwoman",
                 "princes","matriarch","colts","ma","fraternities","pa","fellas","councilmen",
                 "dowry","barbershop","fraternal","ballerina"]

male_bolukbasi = ["he","his","him","man","men","himself","son","father","husband","guy",
                 "boy","boys","brother","male","brothers","dad","sons","boyfriend","grandfather",
                 "uncle","males","grandson","nephew", "fathers","lads","gentleman",
                 "fraternity","bachelor","husbands","dude","beard","gentlemen","stepfather","lad",
                 "testosterone","nephews","daddy","dads","sir","bloke", "schoolboy","stepson","uncles",
                 "hubby","blokes","dudes","grandsons","godfather","boyhood",
                 "grandpa","boyfriends","fella","chap","beards","pa","fellas","fraternal"]

female_bolukbasi = ["he","his","her","she","him","man","women","men","woman","spokesman","wife",
                 "himself","son","mother","father","chairman","daughter","husband","guy","girls",
                 "girl","boy","boys","brother","spokeswoman","female","sister","male","herself",
                 "brothers","dad","actress","mom","sons","girlfriend","daughters","lady",
                 "boyfriend","sisters","mothers","king","businessman","grandmother","grandfather",
                 "deer","ladies","uncle","males","congressman","grandson","bull","queen","businessmen",
                 "wives","widow","nephew","bride","females","aunt","prostatecancer","lesbian","chairwoman",
                 "fathers","moms","maiden","granddaughter","youngerbrother","lads","lion","gentleman",
                 "fraternity","bachelor","niece","bulls","husbands","prince","colt","salesman","hers",
                 "dude","beard","filly","princess","lesbians","councilman","actresses","gentlemen",
                 "stepfather","monks","exgirlfriend","lad","sperm","testosterone","nephews","maid",
                 "daddy","mare","fiance","fiancee","kings","dads","waitress","maternal","heroine",
                 "nieces","girlfriends","sir","stud","mistress","lions","estrangedwife","womb",
                 "grandma","maternity","estrogen","exboyfriend","widows","gelding","diva",
                 "teenagegirls","nuns","czar","ovariancancer","countrymen","teenagegirl","penis",
                 "bloke","nun","brides","housewife","spokesmen","suitors","menopause","monastery",
                 "motherhood","brethren","stepmother","prostate","hostess","twinbrother",
                 "schoolboy","brotherhood","fillies","stepson","congresswoman","uncles","witch",
                 "monk","viagra","paternity","suitor","sorority","macho","businesswoman",
                 "eldestson","gal","statesman","schoolgirl","fathered","goddess","hubby",
                 "stepdaughter","blokes","dudes","strongman","uterus","grandsons","studs","mama",
                 "godfather","hens","hen","mommy","estrangedhusband","elderbrother","boyhood",
                 "baritone","grandmothers","grandpa","boyfriends","feminism","countryman","stallion",
                 "heiress","queens","witches","aunts","semen","fella","granddaughters","chap",
                 "widower","salesmen","convent","vagina","beau","beards","handyman","twinsister",
                 "maids","gals","housewives","horsemen","obstetrics","fatherhood","councilwoman",
                 "princes","matriarch","colts","ma","fraternities","pa","fellas","councilmen",
                 "dowry","barbershop","fraternal","ballerina"]

def weat_6():
    # Note I swapped this around from the original so gender is always attributes
    targets_1 = ["executive", "management", "professional", "corporation", "salary", "office", "business", "career"]
    targets_2 = ["home", "parents", "children", "family", "cousins", "marriage", "wedding", "relatives"]
    attributes_1 = ['grandfather', 'uncle', 'son', 'boy', 'father', 'he', 'him', 'his', 'man', 'male', 'brother']
    attributes_2 = ['daughter', 'she', 'her', 'grandmother', 'mother', 'aunt', 'sister', 'hers', 'woman', 'female', 'girl']
    return targets_1, targets_2, attributes_1, attributes_2


def weat_7():
    targets_1 = ["math", "algebra", "geometry", "calculus", "equations", "computation", "numbers", "addition"]
    targets_2 = ["poetry", "art", "dance", "literature", "novel", "symphony", "drama", "sculpture"]
    attributes_1 = ["male", "man", "boy", "brother", "he", "him", "his", "son"]
    attributes_2 = ["female", "woman", "girl", "sister", "she", "her", "hers", "daughter"]
    return targets_1, targets_2, attributes_1, attributes_2


def weat_8():
    targets_1 = ["science", "technology", "physics", "chemistry", "Einstein", "NASA", "experiment", "astronomy"]
    targets_2 = ["poetry", "art", "Shakespeare", "dance", "literature", "novel", "symphony", "drama"]
    attributes_1 = ["brother", "father", "uncle", "grandfather", "son", "he", "his", "him"]
    attributes_2 = ["sister", "mother", "aunt", "grandmother", "daughter", "she", "hers", "her"]
    return targets_1, targets_2, attributes_1, attributes_2


