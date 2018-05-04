import os
from flask import Flask, render_template, send_from_directory
from lookup import lookup, random_lookup

app = Flask(__name__)

@app.route("/")
def index():
   return render_template("index.html")

@app.route("/<word>")
def results(word):
   try:
      return render_template("results.html", tables=lookup(word))
   except KeyError:
      return render_template("404.html"), 404

@app.route("/test")
def random():
   return render_template("results.html", tables=random_lookup())

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"),
                               "favicon.ico",
                               mimetype="image/vnd.microsoft.icon")

if __name__ == "__main__":
   app.run(debug=True)
