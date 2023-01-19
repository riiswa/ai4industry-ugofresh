import spacy
from spacy import displacy
import fr_core_news_md
import EmbeddingManager as waris


def sentence_pre_treatment( s : str , EmbMan: waris.EmbeddingManager ):
    '''
    devides the sentence into tuples of words matching the structure of branches of the EmbMan.sentence_groups
    unigrams, bigrams, trigrams and quadragrams be compared to sentences with similar structure (ex : a patern 'Noun' is found in the text. 
    It will be compared to all elements that are a Noun in the database. The algorithm then looks at the next word in the sentence that is a verb. 
    bigram's structure is now ( 'Noun', 'Verb' ) and we will compare it to all the 'Noun', 'Verb' sequences in the database, etc until no match in database) 
    '''
    nlp = fr_core_news_md.load()
    tokenized = nlp(s)
    #print(EmbMan.sentence_groups.keys())
    temp = []
    for i in range(len(tokenized)):
        temp.append(tokenized[i].tag_)
    print("temp", temp)

    res = []
    all_words = []
    print(tokenized)
    for i, token in enumerate(tokenized):
        words = token.text
        tag_tuple = [token.tag_ ]
        j = 0 
        ref = [list(a) for a in EmbMan.sentence_groups.keys() if len(a)==j+1]
        while j <= 4 and i+j<len(tokenized):
            #j < 4 because there are at most quadragrams
            if token.text == "inférieur":
                print("tag tuple1: ", tag_tuple)
                print("words1: ", words)
                print("ref1",ref)
            res.append(tag_tuple)
            if tag_tuple in ref : 
                all_words.append(words)
            if i+j == len(tokenized) -1:
                break
            j += 1
            tag_tuple.append(tokenized[i+j].tag_)
            words += " "+tokenized[i+j].text
            ref = [list(a) for a in EmbMan.sentence_groups.keys() if len(a)==j+1]
            if token.text == "inférieur":
                print("tag tuple2: ", tag_tuple)
                print("words2: ", words)
                print("ref2",ref)



    return all_words


if __name__ == "__main__":
    entities = waris.create_entities("data.xlsx")
    em = waris.EmbeddingManager.load()

    print("embedding manager is initialized")
    print(em.predict("aubergine"))
    print("sentence pre-treatment will begin")
    words = sentence_pre_treatment("je voudrai des thomates inférieur à 35 millimètres", EmbMan=em)
    print("words : ",words)
    #em = EmbeddingManager.load()
    #print(list(em.sentence_groups.keys()))
    #em.predict("aubergine")