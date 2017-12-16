from flask import Flask, render_template
import sryaml

app = Flask(__name__)

@app.route("/")
def index():
   return render_template("index.html", forms=sryaml.main())

if __name__ == "__main__":
   app.run(threaded=True)
