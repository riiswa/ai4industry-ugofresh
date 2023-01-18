import json

import spacy
from spacy.tokens import DocBin

nlp = spacy.load("fr_core_news_sm")

training_data = []

with open("training_data.json", 'r') as f:
    data_json = json.load(f)

for data in data_json:
    if len(data["tags"]) == 0:
        continue
    tags = []
    for t in data["tags"]:
        tags.append((
            t["start"],
            t["end"],
            t["name"]
        ))
    training_data.append((
        data["sentence"], tags
    ))
    
# the DocBin will store the example documents
def train(t_d):
    i = 0
    j = 0
    db = DocBin()
    for text, annotations in t_d:
        j += 1
        doc = nlp(text)
        ents = []
        for start, end, label in annotations:
            span = doc.char_span(start, end, label=label)
            if span == None:
                print(f'{text} failed.')
                break
            ents.append(span)
        else:
            doc.ents = ents
            db.add(doc)
            i += 1
    db.to_disk("./train.spacy")
    print(f'{i}/{j} items added')

train(training_data)

# ,
#       {
#         "start": 79,
#         "end": 87,
#         "name": "UGO_Price"
#       }