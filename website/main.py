from flask import Flask, render_template, request
import requests
from rulebased import *
app = Flask(__name__)

@app.route("/")
def about():
    return render_template("about.html")
@app.route("/Made2Morph", methods = ['POST'])
def morph():
    input_text = request.form['transform_text']
    post_process_text = contractions_func(input_text)
    input_dict = {}
    input_dict['input'] = post_process_text
    r = requests.post('http://34.82.174.216:5000/Made2Morph', data=input_dict)
    return (r.text)
    #r = requests.post('http://neu-style.appspot.com/submitted', data = input_dict)
    #return r.text
    #print(contractions_func(first_name))
    return 'Hello %s %s have fun learning python <br/> <a href="/">Back Home</a>' % (contractions_func(input_text), 'hello')
if __name__ == "__main__":
    app.run()

