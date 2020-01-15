from flask import Flask, render_template, request
import requests
from rulebased import *
from viz import visualize_text_embedding

app = Flask(__name__)

@app.route("/")
def about():
    return render_template("about.html")

@app.route("/made2morph", methods = ['POST'])
def morph():
    input_text = request.form['transform_text']

    """
    post_process_text = contractions_func(input_text)
    input_dict = {}
    input_dict['input'] = post_process_text
    r = requests.post('http://34.82.174.216:5000/Made2Morph', data=input_dict)
    return (r.text)
    """

    #print(contractions_func(first_name))
    return render_template("morph.html", input_text = input_text, contraction_input = contractions_func(input_text))

@app.route("/viz", methods = ['GET'])
def viz():
    input_text = request.args.get('input')
    visualize_text_embedding(input_text, "embeddings.txt", "contents.csv")
    return render_template("input.html")

if __name__ == "__main__":
    app.run()

