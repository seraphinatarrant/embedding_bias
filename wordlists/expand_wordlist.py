import argparse
import sys
import spacy
from .wordlists import weat_6, weat_7, weat_8


def setup_argparse():
    p = argparse.ArgumentParser()
    p.add_argument('-c', dest='config_file', default='../config/zotero.yaml',
                   help='a yaml config containing necessary API information')
    #p.add_argument('-d', dest='output_dir', default='../outputs/D4/', help='dir to write output summaries to')
    #p.add_argument('-m', dest='model_path', default='', help='path for a pre-trained embedding model')
    return p.parse_args()



if __name__ == "__main__":
    args = setup_argparse()

    nlp = spacy.load("en_vectors_web_lg")

    # if using one vector have to reshape it to 1,300 instead of just 300 vector.reshape(1,300)
    # union of terms in WEAT 6,7,8
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
                  'director', 'experienced', 'businesses', 'managing', 'payroll', 'consulting', 'company']

    family = ["home", "parents", "children", "family", "cousins", "marriage", "wedding",
              "relatives"]
    family_exp = ['houses', 'house', 'friends', 'kids', 'siblings', 'babies',
                  'marital', 'families', 'in-laws', 'apartment', 'prom', 'toddlers', 'marry',
                  'weddings', 'grandparents', 'infants', 'cousin', 'child', 'nieces']
    art = ['art', 'poetry', 'symphony', 'drama', 'dance', 'Shakespeare', 'sculpture', 'literature',
           'novel']
    art_exp = ['symphonic', 'romance', 'adaptation', 'shakespearean', 'poetic', 'dances',
               'philharmonic', 'prose', 'music', 'choral', 'poems', 'artworks', 'orchestral',
               'artistic', 'poem', 'sculptures', 'arts', 'novels', 'melodrama', 'choreography',
               'literary', 'fiction', 'novella', 'paintings', 'dancers', 'painting']
    match_sci = ['chemistry', 'math', 'science', 'computation', 'Einstein', 'experiment', 'algebra',
                 'geometry', 'NASA', 'astronomy', 'physics', 'numbers', 'technology', 'equations',
                 'addition', 'calculus']
    math_sci_exp = ['innovations', 'sciences', 'biochemistry', 'technologies', 'astrophysics',
                    'algorithms', 'experimenting', 'algorithm', 'nonlinear', 'computations',
                    'astronomers', 'quadratic', 'arithmetic', 'experimental', 'astronomical',
                    'digits', 'counting', 'telescope', 'count', 'research', 'molecular', 'innovation',
                    'innovative', 'idea', 'chemical', 'technological', 'biology', 'scientific',
                    'mathematical', 'geometric', 'high-tech', 'symmetry', 'telescopes',
                    'approximation', 'astronomer', 'numerical', 'laboratory', 'computational',
                    'maths', 'cosmology', 'microbiology','quantum', 'geometries', 'equation',
                    'number', 'theory', 'compute', 'experimented', 'geometrical', 'percentages',
                    'percentage', 'trigonometry', 'relativity', 'experimentation', 'algebraic',
                    'mathematics', 'experiments', 'calculations', 'calculation']
    male = ['grandfather', 'uncle', 'son', 'boy', 'father', 'he', 'him', 'his', 'man', 'male',
            'brother']
    male_exp = ['guy', 'himself', 'nephew', 'grandson', 'men', 'boys', 'great-grandfather',
                'father-in-law', 'husband', 'brothers', 'males', 'brother-in-law', 'sons', 'dad']
    female = ['daughter', 'she', 'her', 'grandmother', 'mother', 'aunt', 'sister', 'hers', 'woman',
              'female', 'girl']
    female_exp = ['grandma', 'herself', 'sister-in-law', 'niece', 'sisters', 'mom', 'mother-in-law',
                  'lady', 'wife', 'females', 'girls', 'great-grandmother', 'women', 'sexy', 'granddaughter', 'daughters']


