from flask import Flask, render_template, request
from rulebased import *
app = Flask(__name__)

@app.route("/")
def about():
    return render_template("about.html")
@app.route("/Made2Morph", methods = ['POST'])
def morph():
    first_name = request.form['transform_text']
    #print(contractions_func(first_name))
    return 'Hello %s %s have fun learning python <br/> <a href="/">Back Home</a>' % (contractions_func(first_name), 'hello')
if __name__ == "__main__":
    app.run()

