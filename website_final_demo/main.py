from flask import Flask, render_template, request
import requests, os
from rulebased import *

STATIC_DIR = os.path.abspath('static')
app = Flask(__name__, static_folder = STATIC_DIR)

@app.route("/")
def about():
    return render_template("about.html")

@app.route("/formal")
def formal():
    return render_template("translate.html")

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

@app.route("/formal/transfer", methods=['POST'])
def transfer():
    input_text = request.form['text']
    r = requests.post('http://34.83.30.177:5000/elon', data={'input': input_text})
    return render_template('translateoutput.html', output = output)

if __name__ == "__main__":
    app.run()

