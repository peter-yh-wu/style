#!/usr/bin/env python

import sys
import os
import json
import requests
from requests.exceptions import HTTPError
from smart_open import open
from shutil import copyfile
import pkg_resources

import pandas as pd

def get_data(model, word, depth=0, topn=10):
    """
    Extracts the data to be displayed from an embedding model
    :param model: w2v model
    :param word: string containing the word for which we build the graph
    :param depth: integer, if we want to create graphs for neighbors, specifies the depth
    :param topn: integer, number of neighbors to extract for each word
    :return: dictionary containing the data to be plotted
    """
    datum = {}
    if not word:
        raise ValueError("Empty string!")
    if word not in model.vocab:
        print(word + " is not in model", file=sys.stderr)
        return None
    res = get_most_similar(model, word, topn)
    datum[word] = res[0]
    get_neighbors(model, datum, res[1], depth, topn)
    return datum


def get_neighbors(model, datum, stack, depth, topn):
    """
    Extracts neighbors of a given word
    :param model: w2v model
    :param datum: updated dictionary containing the data to be plotted
    :param stack: list, neighbors of a word
    :param depth: integer, if we want to create graphs for neighbors, specifies the depth
    :param topn: integer, number of neighbors to extract for each word
    :return: None
    """
    if depth > 0:
        depth -= 1
        for neighbor in stack:
            res = get_most_similar(model, neighbor, topn)
            datum[neighbor] = res[0]
            get_neighbors(model, datum, res[1], depth, topn)
    return datum


def get_most_similar(model, word, topn=10):
    """
    Wrapper for the w2v extractor for the neighbors of a word
    :param model: w2v model
    :param word: string containing the word for which we extract the neighbors
    :param topn: integer, number of neighbors to extract
    :return: list, collected neighbors and list of nodes for the graph
    """
    data = [{"source": word, "target": word, "value": 1}]
    neighbors = []

    mostsim = getattr(model, "similar_by_word")(word, topn=topn)

    for item in mostsim:
        data.append({"source": word, "target": item[0], "value": item[1]})
        neighbors.append(item[0])

    pairs = [
        (neighbors[ab], neighbors[ba])
        for ab in range(len(neighbors))
        for ba in range(ab + 1, len(neighbors))
    ]
    for pair in pairs:
        data.append(
            {"source": pair[0], "target": pair[1], "value": float(model.similarity(*pair))}
        )

    return [data, neighbors]


def render(
        word, data, content_map, interlinks, topn=10, threshold=0, edge=1, sep=False, d3path=""
):
    """
    Generates the HTML page displaying the graph
    :param word: string containing the word for which we build the graph
    :param data: dictionary containing the collected data
    :param interlinks: list of links to other generated pages
    :param topn: integer, number of neighbors to extract for each word
    :param threshold: float, value from which we start drawing edges between nodes
    :param edge: integer, width of edges in the graph
    :param sep: if this parameter is used, token is split by a separator
                (underscore), and only first part is shown in visualization
                (E.g. it is useful when PoS is attached to a word).
    :param d3path: path to the JS file with D3.js library
    :return: string to be written as an output
    """
    html_template = pkg_resources.resource_filename('vec2graph', 'data/genviz.html')
    html = open(html_template, 'r').read()
    return (
        html.replace("d3pathplaceholder", d3path)
            .replace("wordplaceholder", word)
            .replace("splithyphen", str(sep).lower())
            .replace("dataplaceholder", json.dumps(data).replace("\'", "\\u0027"))
            .replace("contentmapplaceholder", json.dumps(content_map).replace("\'", "\\u0027"))
            .replace("topn", str(topn))
            .replace("thresholdplaceholder", str(threshold))
            .replace("linksplaceholder", json.dumps(interlinks).replace("\'", "\\u0027"))
            .replace("linkstrokewidth", str(edge))
    )


def visualize(
        path_html, path_js, content_df, model, words, depth=0, topn=10, threshold=0, edge=1, sep=False, library="web"
):
    """
    Main function for creating the page
    :param path: string, path to output directory where to store files of visualization
    :param model: string, path to vector model file
    :param words: list of words to be visualized
    :param depth: integer, if we want to create graphs for neighbors, specifies the depth
    :param topn: integer, number of neighbors to extract for each word
    :param threshold: float, value from which we start drawing edges between nodes
    :param edge: integer, width of edges in the graph
    :param sep: if this parameter is used, token is split by a separator
                (underscore), and only first part is shown in visualization
                (E.g. it is useful when PoS is attached to a word).
    :param library: path to D3.js library, can be 'web' (link to version at the D3.js site)
           or 'local' (file in the directory with generated HTML, if not present,
           it is downloaded from web).
    :return: None
    """
    d3webpath = "https://d3js.org/d3.v3.min.js"
    if threshold < 1:
        limit = threshold
    else:
        limit = threshold / 100
    data = {}
    depth = int(depth)
    if depth < 0:
        print('Depth must be a positive integer!', file=sys.stderr)
        exit()
    if isinstance(words, list):
        for word in words:
            data.update(get_data(model, word, depth=depth, topn=topn))
    elif isinstance(words, str):
        data = get_data(model, words, depth=depth, topn=topn)
        if not data:
            return 'Word not found'
    else:
        raise ValueError("Wrong type!")

    pages = list(data.keys())

    content_map = [{}, {}] # content_map[0] is id# -> username, content_map[1] is id# -> tweet
    for i, row in content_df.iterrows():
        idx = row['index']
        content_map[0][idx] = row['usernameTweet']
        content_map[1][idx] = row['text']

    if pages:
        if not os.path.exists(path_html):
            os.makedirs(path_html)
        if not os.path.exists(path_js):
            os.makedirs(path_js)

        d3path = d3webpath
        if library == "local":
            d3path = "d3.v3.min.js"
            fullpath = os.path.join(path_html, d3path)

            if not os.path.isfile(fullpath):
                try:
                    response = requests.get(d3webpath)
                    response.raise_for_status()
                except HTTPError as err:
                    print(err, file=sys.stderr)
                except Exception as err:
                    print(err, file=sys.stderr)
                else:
                    response.encoding = "utf-8"
                    with open(fullpath, "w", encoding="utf-8") as d3:
                        d3.write(response.text)

        genviz_js = pkg_resources.resource_filename('vec2graph', 'data/genviz.js')
        copyfile(genviz_js, os.path.join(path_js, 'genviz.js'))
        for page in pages:
            fname = "".join([x for x in page])
            filepath = os.path.join(path_html, fname + ".html")
            with open(filepath, "w") as f:
                f.write(
                    render(
                        page,
                        data[page],
                        content_map,
                        pages,
                        topn=topn,
                        threshold=limit,
                        edge=edge,
                        sep=sep,
                        d3path=d3path,
                    )
                )

        print('Visualizations written to', path_html, path_js, file=sys.stderr)
    return pages
