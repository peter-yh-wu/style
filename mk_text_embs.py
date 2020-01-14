'''
Creates BERT text embeddings
'''

import numpy as np
import os
import pickle
import torch

from pytorch_pretrained_bert import BertTokenizer, BertModel, BertForMaskedLM


def mk_embs(texts, out_paths):
    # texts is list of strings
    # out_paths is list of strings with same len as texts, where respective text is saved
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

    # Load pre-trained model (weights)
    model = BertModel.from_pretrained('bert-base-uncased')

    # model = model.cuda()

    # Put the model in "evaluation" mode, meaning feed-forward operation.
    model.eval()

    for text_i, (text, out_path) in enumerate(zip(texts, out_paths)):
        # Load pre-trained model tokenizer (vocabulary)

        marked_text = "[CLS] " + text + " [SEP]" # text is a stri

        tokenized_text = tokenizer.tokenize(marked_text)[:512]

        indexed_tokens = tokenizer.convert_tokens_to_ids(tokenized_text)

        # Convert inputs to PyTorch tensors
        tokens_tensor = torch.tensor([indexed_tokens]) # .cuda()
        segments_ids = [1] * len(tokenized_text)
        segments_tensors = torch.tensor([segments_ids]) # .cuda()

        # Predict hidden states features for each layer
        with torch.no_grad():
            encoded_layers, _ = model(tokens_tensor, segments_tensors)

        sentence_embedding = torch.mean(encoded_layers[11], 1) # 768 length vector
        np.save(out_path, sentence_embedding.cpu().numpy())

        if (text_i+1) % 100 == 0:
            print('%d/%d' % (text_i+1, len(texts)))