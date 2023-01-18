from dataclasses import dataclass

import spacy
from typing import List, Optional, Dict
import pickle

from transformers import CamembertModel, CamembertTokenizer
import torch
from pynndescent import NNDescent # https://github.com/erikbern/ann-benchmarks
import pandas as pd
from tqdm import tqdm

@dataclass
class Entity:
    text: str
    target: str


def create_entities(file: str):
    xl = pd.ExcelFile("data.xlsx")
    for sheet_name in xl.sheet_names:
        for index, row in xl.parse(sheet_name).iterrows():
            target = row.values[0]
            for text in row.values[1:]:
                if type(text) == str:
                    yield Entity(text, target)


class EmbeddingManager:
    def __init__(self, entities: List[Entity]):
        self.tokenizer = CamembertTokenizer.from_pretrained("camembert-base")
        self.model = CamembertModel.from_pretrained("camembert-base")
        self.model.eval()
        self.nlp = spacy.load("fr_dep_news_trf")
        self.index: Optional[NNDescent] = None
        self.entities = entities
        self.sentence_groups: Dict[tuple[str, ...], List[Entity]] = {}
        for entity in tqdm(entities):
            group = self.group(entity.text)
            self.sentence_groups[group] = self.sentence_groups.get(group, []) + [entity]

        with open("sentence_groups.pkl", 'wb') as filehandler:
            pickle.dump(self.sentence_groups, filehandler)

        self.indexes: Dict[tuple[str, ...], NNDescent] = {
            group: NNDescent(torch.stack([self.embed(entity.text) for entity in entities]), "euclidean")
            for group, entities in tqdm(self.sentence_groups.items())
        }

        with open("indexes.pkl", 'wb') as filehandler:
            pickle.dump(self.indexes, filehandler)

    @staticmethod
    def load(sentence_groups_file: str = "sentence_groups.pkl", indexes_file: str = "indexes.pkl"):
        em = EmbeddingManager([])
        with open(sentence_groups_file, 'rb') as filehandler:
            em.sentence_groups = pickle.load(filehandler)
            print(em.sentence_groups)

        with open(indexes_file, 'rb') as filehandler:
            em.indexes = pickle.load(filehandler)
            print(em.indexes)

        return em

    def embed(self, sentence: str) -> torch.Tensor:
        tokenized_sentence = self.tokenizer.tokenize(sentence)
        encoded_sentence = self.tokenizer.encode(tokenized_sentence)
        encoded_sentence = torch.tensor(encoded_sentence)[1:-1].unsqueeze(0)
        return self.model(encoded_sentence).last_hidden_state.detach().squeeze(0).mean(dim=0)

    def group(self, sentence: str) -> tuple[str, ...]:
        doc = self.nlp(sentence.lower())
        return tuple(token.pos_ for token in doc)

    def predict(self, sentence: str):
        group = self.group(sentence)
        print(self.sentence_groups[group])
        return group, self.indexes[group].query(self.embed(sentence).unsqueeze(0), k=5)


if __name__ == "__main__":
    entities = create_entities("data.xlsx")
    em = EmbeddingManager(list(entities))
    print(em.predict("aubergine"))
    #em = EmbeddingManager.load()
    #print(list(em.sentence_groups.keys()))
    #em.predict("aubergine")
