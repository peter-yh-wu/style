import os
import shutil

import numpy as np
import pandas as pd

from nltk import word_tokenize

from gensim.scripts.glove2word2vec import glove2word2vec
from gensim.models.keyedvectors import KeyedVectors

from vec2graph import visualize
from mk_text_embs import mk_embs

def load_and_visualize(username):
    print("Loading model...")
    file = "data/embeddings_with_input.txt"
    glove2word2vec(glove_input_file=file, word2vec_output_file="gensim_glove_vectors.txt")
    model = KeyedVectors.load_word2vec_format("gensim_glove_vectors.txt", binary=False)

    print("Finished loading model")
    print("Creating visual html...")
    df = pd.read_csv("data/many_likes_with_input.csv")
    visualize("tmp/graphs", df, model, username)

def process_sentence(text):
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word.isalpha()]
    tokens = [word.lower() for word in tokens]
    processed_text = ' '.join(tokens)
    return processed_text

def visualize_text_embedding(text):
    # we'll generate an embedding for the text on the fly and append it to the glove style file
    # then run the load and visualize function with the supplied text

    # preprocess text
    processed_text = process_sentence(text)

    # generate embedding
    print("Generating embedding of text...")
    out_path = "data/embedding_input_text"
    mk_embs([processed_text], [out_path])
    ar = np.load(out_path + ".npy").flatten()

    # now append it to the current set of embeddings
    shutil.copyfile("data/embeddings.txt", "data/embeddings_with_input.txt")

    username = "input"
    with open("data/embeddings_with_input.txt", "a") as f:
        f.write(username + " ")
        for i in ar:
            f.write(str(i) + " ")

    # also update content map csv
    shutil.copyfile("data/many_likes.csv", "data/many_likes_with_input.csv")
    with open("data/many_likes_with_input.csv", "a") as f:
        f.write(f"{username},Input,{text}")

    # run load_and_visualize
    print("Finished generating embedding, running visualizer...")
    load_and_visualize(username)

if __name__ == "__main__":
    text = input()
    print("Recieved input, processing...")
    visualize_text_embedding(text)

