import spacy
from spacy import displacy
import fr_core_news_md

nlp = fr_core_news_md.load()

def tokenise(text):
    return nlp(text)

def get_obvious(tokenized, dictionaire):
    ''' 
    @param dictionnaire : un dictionaire vide avec l'ensemble des champs qu'on veut remplir
    @param tokenized : phrase tokenisé par spacy (fr_core_news_md)
    récupère tous les champs évidents et remplit le dico avec ; les retire de la phrase tokenisée
    retours : renvoie un nouvel élément tokenized modifié et un dictionnaire partiellement rempli
    '''
    

def pass2encode(tokenized):
    '''
    @param tokenized : phrase tokenisé par spacy (fr_core_news_md)
    retours : renvoie un list avec un ensemble de mots à encoder
    '''





if __name__ == "__main__" :

    nlp = fr_core_news_md.load()
    text = (
        "Bonjour, j'aimerai 60 douzaines de citrons verts et bleus conditionnés dans des barquettes de 20 pour demain"
        #"Il me faudrait des tomates gloriettes bio française, et j'en voudrais 300kg je pense."
    )

    about_doc = nlp(text)

    for token in about_doc:
        print(f"{token} {token.idx}")


    for token in about_doc:
        print(
            f"{str(token.text_with_ws):22}"
            f"{str(token.is_alpha):15}"
            f"{str(token.is_punct):18}"
            f"{str(token.is_stop):21}"
            f"{str(token.pos_)}"
        )

    for token in about_doc:
        print(
            f"""
    TOKEN: {token.text}
    =====
    {token.tag_ = }
    {token.head.text = }
    {token.dep_ = }
    """
        )

    displacy.serve(about_doc, style="dep")