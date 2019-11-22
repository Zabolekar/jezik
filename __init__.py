import os
from werkzeug.routing import PathConverter
from flask import Flask, redirect, render_template, request, send_from_directory, url_for # type: ignore
from .lookup import lookup, random_key

class Query(PathConverter):
   regex = ".*?" # everything PathConverter accepts but also leading slashes

app = Flask(__name__)

app.url_map.converters["query"] = Query

@app.route("/")
def index():
   return render_template("index.html")

@app.route("/lookup/<query:word>")
def results(word):
   input_yat = request.args.get("in") or "e"
   output_yat = request.args.get("out") or "e"
   tables = lookup(word, input_yat, output_yat)
   return render_template("results.html", tables=tables)

@app.errorhandler(404)
def page_not_found(_):
   return render_template("404.html"), 404

@app.route("/random")
def random():
   word, yat = random_key()
   if yat == "je":
      kwargs = {"word": word, "in": "ije", "out": "je"} 
      ## because input doesn't differentiate between what we call jekav and ijekav
   else: # e or ije
      kwargs = {"word": word, "in": yat, "out": yat}
   return redirect(url_for("results", **kwargs))

@app.route("/about")
def about():
   return render_template("about.html")

@app.route("/favicon.ico")
def favicon():
   return send_from_directory(
      os.path.join(app.root_path, "static"),
      "favicon.ico",
      mimetype="image/vnd.microsoft.icon"
   )
