from flask import Flask, render_template, request
import requests
app = Flask(__name__, static_folder="build/static", template_folder="build")

@app.route("/")
def hello():
    return render_template('index.html')

if __name__ == "__main__":
    app.debug=True
    app.run(host='0.0.0.0')
