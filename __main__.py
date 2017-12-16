from flask import Flask, render_template
from conjugate import lookup, random_word

app = Flask(__name__)

@app.route("/")
@app.route("/<word>")
def index(word=None):
   forms = lookup(word) if word else random_word()
   return render_template("index.html", forms=forms)

if __name__ == "__main__":
   app.run(threaded=True)
