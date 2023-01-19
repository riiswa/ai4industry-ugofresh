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
        res['famille'] = cut_too_much('famille')
    if 'sous_famille' in res:
        res['sous_famille'] = cut_too_much('sous_famille')
    if 'variété' in res:
        res['variété'] = cut_too_much('variété')
    
    return res


sentence = "J'ai 300kg d'aubergine type graffiti variété angela, en cagette qui viennent de France."

family=["plante aromatique","fruit rouge","bulbe","chou","céréale"]
family = [x.lower() for x in family]
sub_family=["Aubergine","Avocat","Banane","Basilic","Laurier","Fève"]
sub_family = [x.lower() for x in sub_family]
variety=["Asperge blanche","Asperge blanche/violette","Asperge verte","Asperge violette","Aubergine Japonaise","Aubergine","Aubergine Angela","Aubergine Fine Longue","Aubergine Graffiti","Aubergine Noire","Aubergine Perline","Aubergine ronde violette","Aubergine zébrée","Avocat Hass","Avocat","Avocat Bacon"]
variety = [x.lower() for x in variety]
quantity=["Kg", "Kilogramme", "Colis"]
quantity = [x.lower() for x in quantity]

info = extract_info(sentence,
    family=family,
    sub_family=sub_family,
    variety=variety,
    calibre=[],
    conditioning=[],
    country=[],
    label=[],
    quantity=quantity,
    price=[]
)
print(info)