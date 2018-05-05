import os
import sys
from flask import Flask, render_template, send_from_directory # type: ignore
from .lookup import lookup, random_lookup

app = Flask(__name__)

@app.route("/")
def index():
   return render_template("index.html")

@app.route("/lookup/<word>")
def results(word):
   return render_template("results.html", tables=lookup(word))

@app.errorhandler(404)
def page_not_found(_):
   return render_template("404.html"), 404

@app.route("/random")
def random():
   return render_template("results.html", tables=random_lookup())

@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"),
                               "favicon.ico",
                               mimetype="image/vnd.microsoft.icon")
