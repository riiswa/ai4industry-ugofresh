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
        if token.pos_ == "NOUN":
            tok = token.text.lower()
            for fam in family:
                if tok in fam:
                    if 'famille' in res:
                        tmp_tok = res['famille'] + " " + tok
                        if tmp_tok in fam:
                            res['famille'] = tmp_tok
                    else:
                        res['famille'] = tok
            for sfam in sub_family:
                if tok in sfam:
                    if 'sous_famille' in res:
                        tmp_tok = res['sous_famille'] + " " + tok
                        if tmp_tok in sfam:
                            res['sous_famille'] = tmp_tok
                    else:
                        res['sous_famille'] = tok
            for var in variety:
                if tok in var:
                    if 'variety' in res:
                        tmp_tok = res['variety'] + " " + tok
                        if tmp_tok in var:
                            res['variety'] = tmp_tok
                    else:
                        res['variety'] = tok
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
            tok = int(token) if token.is_digit() else token
            if to_fill_type not in ["", "num"]:
                res[to_fill_type]['num'] = tok
                to_fill_type = ""
            else:
                to_fill_type = "num"
                to_fill = tok
    return res


sentence = "J'ai 300kg d'aubergines type grafiti variété angela, en cagette qui viennent de France."
info = extract_info(sentence)
print(info)
