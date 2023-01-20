import nltk
from nltk import word_tokenize

import spacy
from spacy.lang.fr.stop_words import STOP_WORDS

import pandas as pd
import string
import json

nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')

# Chargement du modèle en français de Spacy
nlp = spacy.load("fr_core_news_sm")

def tokenize(sentence):
  for token in sentence:
    return [token.text for token in sentence]

def lemma(sentence):
    return " ".join([token.lemma_ for token in nlp(sentence)])

def removeStopWords(sentence):
    return [word for word in tokenize(sentence) if not word in STOP_WORDS  ]

def removePonct(sentence):
  return [word for word in sentence if word not in string.punctuation]

def traitement(sentence):
    onesentence=nlp(sentence)
    newsentence=nlp(onesentence)
    removed_stpwrds= removeStopWords(newsentence)
    removed_ponct = removePonct(removed_stpwrds)
    lemmatized_sentence = lemma(removed_ponct)
    return lemmatized_sentence

def csv_to_json(csv_file, json_file):
    # lire le fichier csv en utilisant pandas
    df = pd.read_csv(csv_file)
    # créer un dictionnaire vide
    data = {}
    # itérer sur les lignes du fichier csv
    for index, row in df.iterrows():
        # ajouter une entrée au dictionnaire avec la valeur de la colonne Valeur comme clé et la valeur de la colonne Texte comme valeur
        data[row['Valeur']] = lemma(row['Texte']).lower()
    with open(json_file, 'w') as f:
        json.dump(data, f)

def extract_info(sentence,
    family = [],
    sub_family = [],
    variety = [],
    calibre = [],
    conditioning = [],
    country = [],
    label = [],
    quantity = [],
    price = []
):
    # Analyse de la phrase avec Spacy
    doc = nlp(sentence.replace('\'', ' '))

    res = {}

    to_fill = None
    to_fill_type = ""

    def data_with_num(data, tok, to_f, to_f_type):
        if data in res:
            if 'num' not in res[data]:
                res[data]['text'] = tok
                if to_f_type == 'num':
                    res[data]['num'] = to_f
                    to_f_type = ""
                else:
                    to_f_type = data
        else:
            res[data] = {'text': tok}
            if to_f_type == 'num':
                res[data]['num'] = to_f
                to_f_type = ""
            else:
                to_f_type = data

        return to_f, to_f_type


    for token in doc:
        if token.pos_ != "NUM":
            tok = token.text.lower()
            for fam in family:
                if tok in fam.split(' '):
                    if 'famille' in res:
                        if fam in res['famille']:
                            res['famille'][fam].append(tok)
                        else:
                            res['famille'][fam] = [tok]
                    else:
                        res['famille'] = {}
                        res['famille'][fam] = [tok]
            for sfam in sub_family:
                if tok in sfam.split(' '):
                    if 'sous_famille' in res:
                        if sfam in res['sous_famille']:
                            res['sous_famille'][sfam].append(tok)
                        else:
                            res['sous_famille'][sfam] = [tok]
                    else:
                        res['sous_famille'] = {}
                        res['sous_famille'][sfam] = [tok]
            for var in variety:
                if tok in var.split(' '):
                    if 'variété' in res:
                        if var in res['variété']:
                            res['variété'][var].append(tok)
                        else:
                            res['variété'][var] = [tok]
                    else:
                        res['variété'] = {}
                        res['variété'][var] = [tok]
            if tok in label:
                if 'label' in res:
                    res['labels'].append(tok)
                else:    
                    res['labels'] = [tok]
            elif tok in country:
                res['origine'] = tok
            elif tok in conditioning:
                to_fill_type = data_with_num('conditionnement', tok, to_fill, to_fill_type)
            elif tok in quantity:
                to_fill_type = data_with_num('quantité', tok, to_fill, to_fill_type)
            elif tok in calibre:
                to_fill_type = data_with_num('calibre', tok, to_fill, to_fill_type)
            elif tok in price:
                to_fill_type = data_with_num('prix', tok, to_fill, to_fill_type)
        elif token.like_num:
            tok = token.text.lower()
            if to_fill_type not in ["", "num"]:
                res[to_fill_type]['num'] = tok
                to_fill_type = ""
            else:
                to_fill_type = "num"
                to_fill = tok
    
    def cut_too_much(res_data):
        final_variety = {}
        for key, values in res_data.items():
            res_var = " ".join(values)
            if res_var in final_variety:
                final_variety[res_var].append(key)
            else:
                final_variety[res_var] = [key]
                
        keys = list(final_variety.keys())
        
        for k in keys:
            for k_bis in keys:
                if k in k_bis and k != k_bis:
                    del final_variety[k]
                    break
        return final_variety
    
    if 'famille' in res:
        res['famille'] = cut_too_much(res['famille'])
    if 'sous_famille' in res:
        res['sous_famille'] = cut_too_much(res['sous_famille'])
    if 'variété' in res:
        res['variété'] = cut_too_much(res['variété'])
    
    return res




# csv_to_json('./data/Famille.csv', "./json/Famille.json")
# csv_to_json('./data/Sous-famille.csv', './json/Sous-famille.json')
# csv_to_json('./data/Variété.csv', './json/Variété.json')
# csv_to_json('./data/Pays.csv', './json/Pays.json')
# csv_to_json('./data/Conditionnement.csv', './json/Conditionnement.json')
# csv_to_json('./data/Quantité.csv', './json/Quantité.json')
# csv_to_json('./data/Calibre.csv', './json/Calibre.json')
# csv_to_json('./data/Labels.csv', './json/Labels.json')

with open('./json/Famille.json') as json_file:
    family = json.load(json_file).values()
with open('./json/Sous-famille.json') as json_file:
    sub_family = json.load(json_file).values()
with open('./json/Variété.json') as json_file:
    variety = json.load(json_file).values()
with open('./json/Pays.json') as json_file:
    calibre = json.load(json_file).values()
with open('./json/Conditionnement.json') as json_file:
    conditioning = json.load(json_file).values()
with open('./json/Quantité.json') as json_file:
    country = json.load(json_file).values()
with open('./json/Calibre.json') as json_file:
    label = json.load(json_file).values()
with open('./json/Labels.json') as json_file:
    quantity = json.load(json_file).values()
    

sentence = "J'ai 300kg d'aubergine type graffiti variété angela, en cagette qui viennent France."

info = extract_info(sentence,
    family=family,
    sub_family=sub_family,
    variety=variety,
    calibre=calibre,
    conditioning=conditioning,
    country=country,
    label=label,
    quantity=quantity,
    price=["euros", "eur", "€", "euro", "prix"]
)
print(info)