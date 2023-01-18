import nltk
import spacy
from nltk import word_tokenize

nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')

# Chargement du modèle en français de Spacy
nlp = spacy.load("fr_core_news_sm")

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
    # Tokenisation de la phrase
    tokens = word_tokenize(sentence)
    # Analyse de la phrase avec Spacy
    doc = nlp(" ".join(tokens))

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
            res[data] = {'text': tok}
            if to_f_type == 'num':
                res[data]['num'] = to_f
                to_f_type = ""


    for token in doc:
        if token.pos_ == "NOUN":
            tok = token.text.lower()
            if tok in family:
                res['famille'] = tok
            if tok in sub_family:
                res['sous_famille'] = tok
            if tok in variety:
                res['variete'] = tok
            elif tok in label:
                if 'label' in res:
                    res['labels'].append(tok)
                else:    
                    res['labels'] = [tok]
            elif tok in country:
                res['origine'] = tok
            elif tok in conditioning:
                if 'conditionnement' in res:
                    if 'num' not in res['conditionnement']:
                        res['conditionnement']['text'] = tok
                        if to_fill_type == 'num':
                            res['conditionnement']['num'] = to_fill
                            to_fill_type = ""
                else:
                    res['conditionnement'] = {'text': tok}
                    if to_fill_type == 'num':
                        res['conditionnement']['num'] = to_fill
                        to_fill_type = ""
            elif tok in quantity:
                if 'quantity' in res:
                    if 'num' not in res['quantity']:
                        res['quantity']['text'] = tok
                        if to_fill_type == 'num':
                            res['quantity']['num'] = to_fill
                            to_fill_type = ""
                else:
                    res['quantity'] = {'text': tok}
                    if to_fill_type == 'num':
                        res['quantity']['num'] = to_fill
                        to_fill_type = ""


                    
        elif token.like_num:
            pass
    return res


sentence = "J'ai 300kg d'aubergines type grafiti variété angela, en cagette qui viennent de France."
info = extract_info(sentence)
print(info)
