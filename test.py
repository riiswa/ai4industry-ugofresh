import nltk
import spacy
from nltk import word_tokenize

nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')

# Chargement du modèle en français de Spacy
nlp = spacy.load("fr_core_news_sm")

def extract_info(sentence):
    # Tokenisation de la phrase
    tokens = word_tokenize(sentence)
    # Analyse de la phrase avec Spacy
    doc = nlp(" ".join(tokens))
    famille = ""
    conditionnement = ""
    sous_famille = ""
    variete = ""
    origine = ""
    quantite = ""
    unite = ""
    for token in doc:
        if token.pos_ == "NOUN":
            if token.text.lower() in ["aubergine", "aubergines"]:
                famille = "aubergine"
            elif token.text.lower() in ["cagette", "cagettes"]:
                conditionnement = "cagette"
            elif token.text.lower() in ["grafiti"]:
                sous_famille = "grafiti"
            elif token.text.lower() in ["angela"]:
                variete = "angela"
            elif token.text.lower() in ["france", "francais", "francaise"]:
                origine = "France"
        elif token.like_num:
            quantite = token.text
        elif token.text.lower() in ["kg", "kilogramme", "kilogrammes"]:
            unite = "kilogramme"
    return {"famille": famille, "conditionnement": conditionnement, "sous_famille": sous_famille, "variete": variete, "origine": origine, "quantite": quantite, "unite": unite}


sentence = "J'ai 300kg d'aubergines type grafiti variété angela, en cagette qui viennent de France."
info = extract_info(sentence)
print(info)
