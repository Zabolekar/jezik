from flask import Flask, render_template, request
from conjugate import lookup, random_word

app = Flask(__name__)

@app.route("/")
def index():
   return render_template("index.html")

@app.route("/<word>")
def results(word):
   return render_template("results.html", forms=lookup(word))

@app.route("/test")
def random():
   return render_template("results.html", forms=random_word())

if __name__ == "__main__":
   app.run(threaded=True)
