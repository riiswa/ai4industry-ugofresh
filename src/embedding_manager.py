from dataclasses import dataclass
from collections import defaultdict
from typing import Optional
from pprint import pprint

import fr_dep_news_trf
import pandas as pd
import torch
from transformers import CamembertTokenizer, CamembertModel
import annoy
from tqdm import tqdm
import pickle

from unidecode import unidecode
import re
import time

BLACK_LISTED_WORDS = \
    ["type", "variété", "famille", "sous", "calibre", "conditionnement", "pays", "label", "quantité", "prix"]


def remove_parentheses_and_trim(s):
    return re.sub(r'\([^)]*\)', '', s).strip()


def preprocess_string(s):
    s = s.lower()
    s = unidecode(s)
    return s


def find_subsequences(set_of_sequences, long_sequence):
    sub_sequences = []
    set_of_sequences = [tuple(seq) for seq in set_of_sequences]
    set_of_sequences = set(set_of_sequences)
    n = len(long_sequence)
    for i in range(n):
        for j in range(i + 1, n + 1):
            sub = tuple(long_sequence[i:j])
            if sub in set_of_sequences:
                sub_sequences.append((i, j))
    return sub_sequences


@dataclass
class Entity:
    text: str
    target: str
    type: str
    group: Optional[tuple[str, ...]] = None


def preprocess_fr_sentence(nlp, sentence):
    doc = nlp(sentence)
    filtered_tokens = [token for token in doc if not token.is_stop and not token.is_punct and token.text not in BLACK_LISTED_WORDS]
    return [token.lemma_ for token in filtered_tokens], tuple(token.tag_ for token in filtered_tokens)


def create_entities(nlp, file: str = "data.xlsx"):
    xl = pd.ExcelFile(file)
    for sheet_name in xl.sheet_names:
        for index, row in xl.parse(sheet_name).iterrows():
            target = row.values[0]
            for text in row.values[1:]:
                if type(text) == str:
                    text = remove_parentheses_and_trim(text)
                    tokens, group = preprocess_fr_sentence(nlp, text)
                    if tokens:
                        yield Entity(" ".join(tokens), target, group, sheet_name)


def jaccard_similarity(x, y):
    """ returns the jaccard similarity between two lists """
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality / float(union_cardinality)


class EmbeddingManager:
    def __init__(self, nlp, entities=[]):
        self.nlp = nlp
        self.tokenizer = CamembertTokenizer.from_pretrained("camembert-base")
        self.model = CamembertModel.from_pretrained("camembert-base")
        self.model.eval()
        self.grouped_entities = defaultdict(list)
        self.indexes = defaultdict(lambda: annoy.AnnoyIndex(768, "angular"))
        for entity in entities:
            self.grouped_entities[entity.group].append(entity)

        for group_key, entities in tqdm(self.grouped_entities.items()):
            for i, entity in enumerate(entities):
                self.indexes[group_key].add_item(i, self.embed(entity.text))
            self.indexes[group_key].build(10)

    def save(self):
        with open('grouped_entities.pkl', 'wb') as file:
            pickle.dump(self.grouped_entities, file)
        for k, index in self.indexes.items():
            index.save(str(k) + ".ann")

    @staticmethod
    def load(nlp):
        em = EmbeddingManager(nlp)
        with open('grouped_entities.pkl', 'rb') as file:
            em.grouped_entities = pickle.load(file)
        for k in em.grouped_entities.keys():
            em.indexes[k].load(str(k) + ".ann")
        return em

    def embed(self, sentence: str) -> torch.Tensor:
        tokenized_sentence = [token for token in self.tokenizer.tokenize(sentence.lower())]
        encoded_sentence = self.tokenizer.encode(tokenized_sentence)
        encoded_sentence = torch.tensor(encoded_sentence)[1:-1].unsqueeze(0)
        return self.model(encoded_sentence).last_hidden_state.detach().squeeze(0).mean(dim=0)

    def predict(self, sentence: str, group: Optional[tuple[str, ...]] = None, k=5):
        if group is None:
            group = preprocess_fr_sentence(self.nlp, sentence)[1]
        entities = []
        idx, distances = self.indexes[group].get_nns_by_vector(self.embed(sentence), k, include_distances=True)
        for i, distance in zip(idx, distances):
            entity = self.grouped_entities[group][i]
            j_sim = jaccard_similarity(preprocess_string(sentence), preprocess_string(entity.text))
            confidence = 1 - distance*j_sim
            if j_sim > 0.5 and confidence >= 0.75:
                entities.append({entity.type: sentence, "confidence": confidence, "tag": entity.target})
        return entities

    def predict_full_sentence(self, full_sentence: str):
        start = time.time()
        tokens, tags = preprocess_fr_sentence(
            nlp, full_sentence
        )
        predictions = []
        for i, j in find_subsequences(set(em.grouped_entities.keys()), tags):
            sub_sentence = " ".join(tokens[i:j])
            predictions = predictions + self.predict(sub_sentence)
        end = time.time()
        print("Elapsed time:", end - start)
        return predictions

    def __iadd__(self, entity: Entity):
        if entity.group is None:
            _, group = preprocess_fr_sentence(self.nlp, entity.text)
            entity.group = group

        self.grouped_entities[entity.group].append(entity)
        self.indexes[entity.group] = annoy.AnnoyIndex(768, "angular")
        for i, entity in enumerate(tqdm(self.grouped_entities[entity.group])):
            self.indexes[entity.group].add_item(i, self.embed(entity.text))
        self.indexes[entity.group].build(10)

        return self


if __name__ == "__main__":
    nlp = fr_dep_news_trf.load()
    em = EmbeddingManager(nlp, create_entities(nlp))
    em.save()

    # Load a pretrained model without create entities
    #em = EmbeddingManager.load(nlp)

    em += Entity(text="cagette", target="cagette", type="Conditionnement")

    sentences = [
        "Je vends des tomates cerises d'origine francaise",
        "Je propose des citrons biologique à 5 euros",
        "J'ai des fraises guariguette d'un calibre de 15 millimetres",
        "Je cherche 300kg de legumes en sac",
        "Je vends des prunes marocaine en colis de 6 kilos à 20 euros, EAN: 5263718293026",
        "Je veux 200 kilos pommes fuji moyenne bio d'origine française en barquette de 40, à 25 euros la barquette EAN: 5263718293026",
        "Rendez vous demain à 15h00 pour la livraison"
    ]

    for sentence in sentences:
        print("Analyzing sentence:", sentence)
        pprint(em.predict_full_sentence(sentence))
        print()
