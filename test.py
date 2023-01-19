import nltk
import spacy
from nltk import word_tokenize
from nltk.corpus import stopwords
import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.stem.snowball import FrenchStemmer
from nltk.tokenize import word_tokenize
from spacy.lang.fr.stop_words import STOP_WORDS
from spacy.tokens import token
import string
import pandas as pd
import json
from nltk import pos_tag

nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('omw-1.4')

# Chargement du modèle en français de Spacy
nlp = spacy.load("fr_core_news_sm")


df_family = pd.read_csv('/home/settar/Bureau/UGOFresh/ai4industry-ugofresh/DataCSV/Famille.csv')
df_subfamily = pd.read_csv('/home/settar/Bureau/UGOFresh/ai4industry-ugofresh/DataCSV/Sous-famille.csv')
df_variety = pd.read_csv('/home/settar/Bureau/UGOFresh/ai4industry-ugofresh/DataCSV/Variété.csv')
df_origin = pd.read_csv('/home/settar/Bureau/UGOFresh/ai4industry-ugofresh/DataCSV/Pays.csv')
df_packaging = pd.read_csv('/home/settar/Bureau/UGOFresh/ai4industry-ugofresh/DataCSV/Conditionnement.csv')
df_quantity = pd.read_csv('/home/settar/Bureau/UGOFresh/ai4industry-ugofresh/DataCSV/Quantité.csv')
df_calibre = pd.read_csv('/home/settar/Bureau/UGOFresh/ai4industry-ugofresh/DataCSV/Calibre.csv')
df_labels = pd.read_csv('/home/settar/Bureau/UGOFresh/ai4industry-ugofresh/DataCSV/Labels.csv')

def tokenize(sentence):
  for token in sentence:
    return [token.text for token in sentence]

def lemma(sentence):
    return [token.lemma_ for token in nlp(" ".join(sentence))]

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
        data[row['Valeur']] = row['Texte']
    with open(json_file, 'w') as f:
        json.dump(data, f)


def extract_info(sentence):
    
    df_subfamily=csv_to_json('/home/settar/Bureau/UGOFresh/ai4industry-ugofresh/DataCSV/Sous-famille.csv', 'Sous-famille.json')

    with open('Sous-famille.json') as json_file:
        data = json.load(json_file)
        
    doc = nlp(" ".join(traitement(sentence)))
    #print(doc)

    famille = ""
    conditionnement = ""
    sous_famille = ""
    variete = ""
    origine = ""
    quantite = ""
    unite = ""

    for token in doc:
        if token.pos_ == "NOUN" or token.pos_ == "PROPN":
            for val in data:
                if token.text.lower() in data[val].lower():
                    print(token.text)
                    print(traitement(data[val]))
                    sous_famille = val
        elif token.like_num:
            quantite = token.text
        elif token.text.lower() in ["kg", "kilogramme", "kilogrammes"]:
            unite = "kilogramme"
    return {"sous_famille": sous_famille, "quantite": quantite, "unite": unite}


sentence = "je veux 300kg de Noix, en cagette qui viennent de France."
info = extract_info(sentence)
print(info)

