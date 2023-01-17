from typing import List, Optional

from transformers import CamembertModel, CamembertTokenizer
import torch
from pynndescent import NNDescent


class EmbeddingManager:
    def __init__(self, sentences: List[str]):
        self.tokenizer = CamembertTokenizer.from_pretrained("camembert-base")
        self.model = CamembertModel.from_pretrained("camembert-base")
        self.model.eval()
        self.index: Optional[NNDescent] = None
        self.index = NNDescent(torch.stack([self.embed(sentence) for sentence in sentences]), "cosine")

    def embed(self, sentence: str) -> torch.Tensor:
        tokenized_sentence = self.tokenizer.tokenize(sentence)
        encoded_sentence = self.tokenizer.encode(tokenized_sentence)
        encoded_sentence = torch.tensor(encoded_sentence)[1:-1].unsqueeze(0)
        return self.model(encoded_sentence).last_hidden_state.detach().squeeze(0).mean(dim=0)

    def predict(self, sentence: str):
        return self.index.query(self.embed(sentence).unsqueeze(0), k=5)


if __name__ == "__main__":
    em = EmbeddingManager(["poire", "orange", "carotte", "pommes", "pomme verte", "pomme rouge"])

    print(em.predict("pomme"))


