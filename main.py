from datetime import datetime
from flask import Flask, render_template, request
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
def get_about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def get_contact():
    h1 = "Contact Me"
    if request.method == "POST":
        h1 = "Successfully sent message"
        name, email, tel, msg = request.form.values()
        print(f"name: {name}, email: {email}, tel: {tel}, msg: {msg}")
    return render_template("contact.html", header=h1)


@app.route("/post/<pid>")
def get_post(pid):
    posts_filter = [p for p in POSTS if str(p["id"]) == pid]
    post = posts_filter[0] if len(posts_filter) == 1 else Exception(ValueError)
    return render_template("post.html", post=post)


if __name__ == '__main__':
    app.run(debug=True)
