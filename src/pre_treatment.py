import spacy
from spacy import displacy
import fr_core_news_md
import EmbeddingManager as waris


def sentence_pre_treatment( s : str , EmbMan: waris.EmbeddingManager ):
    '''
    devides the sentence into tuples of words matching the structure of branches of the EmbMan.sentence_groups
    '''
    nlp = fr_core_news_md.load()
    tokenized = nlp(s)
    res = []
    for i, token in enumerate(tokenized):
        tag_tuple = [token.tag_ ]
        j = 0 
        ref = [list(a)[0:j] for a in EmbMan.sentence_groups]
        while tag_tuple in ref :
            j += 1
            tag_tuple = tag_tuple.append(tokenized[i+j].tag_)
            ref = [a[0:j] for a in EmbMan.sentence_group]
            res.append(tag_tuple)
    return res


if __name__ == "__main__":
    entities = waris.create_entities("data.xlsx")
    em = waris.EmbeddingManager.load()

    print("embedding manager is initialized")
    print(em.predict("aubergine"))
    print("sentence pre-treatment will begin")
    sentence_pre_treatment("inférieur à 35 millimètres", EmbMan=em)
    #em = EmbeddingManager.load()
    #print(list(em.sentence_groups.keys()))
    #em.predict("aubergine")