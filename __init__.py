import os
from werkzeug.routing import PathConverter
from flask import Flask, render_template, request, send_from_directory # type: ignore
from .lookup import lookup, random_lookup

class Query(PathConverter):
   regex = ".*?" # everything PathConverter accepts but also leading slashes

app = Flask(__name__)

app.url_map.converters["query"] = Query

@app.route("/")
def index():
   return render_template("index.html")

@app.route("/lookup/<query:word>")
def results(word):
   input_yat = request.args.get("inputYat") or "ekav"
   output_yat = request.args.get("outputYat")
   tables = lookup(word, input_yat, output_yat)
   return render_template("results.html", tables=tables)

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
