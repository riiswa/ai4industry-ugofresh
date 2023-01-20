# ai4industry-ugofresh

## Installation

Create a virtual env and run `pip install requirements.txt`

## Usage 

You can read the `main` to see an example of usage in the file `src/embedding_manager.py`

## Description

Our work is based on the CamemBERT model to create word embedding. We use an efficient KDTree implementation (The Annoy library by Spotify) to compare the embeddings. For better performance, we split the data in differents different group based by a POS tagging given by spacy.

