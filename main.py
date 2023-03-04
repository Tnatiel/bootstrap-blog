from datetime import datetime

from flask import Flask, render_template
import requests as req

POSTS = req.get("https://api.npoint.io/511981ad9e97d831283f").json()
app = Flask(__name__)
app.config['CURRENT_YEAR'] = datetime.now().year


@app.context_processor
def year_injector():
    return {"year": app.config["CURRENT_YEAR"]}


@app.route("/")
def home():
    return render_template("index.html", posts=POSTS)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == '__main__':
    app.run(debug=True)
