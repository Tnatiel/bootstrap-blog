import smtplib
import ssl
from email.mime.text import MIMEText
from datetime import datetime
import requests as req
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, SubmitField
from wtforms.validators import InputRequired, URL

EMAIL = "ntgk666@gmail.com"
POSTS = req.get("https://api.npoint.io/511981ad9e97d831283f").json()
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['CURRENT_YEAR'] = datetime.now().year
Bootstrap(app)


# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


# WTForm
class CreatePostForm(Form):
    title = StringField("Blog Post Title", validators=[InputRequired()])
    subtitle = StringField("Subtitle", validators=[InputRequired()])
    author = StringField("Your Name", validators=[InputRequired()])
    img_url = StringField("Blog Image URL", validators=[InputRequired(), URL()])
    body = StringField("Blog Content", validators=[InputRequired()])
    submit = SubmitField("Submit Post")

def send_msg(msg):
    port = 465  # for SSL
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(EMAIL, "ehbyrzfkmkccgllq")
        to_send = MIMEText(msg)
        to_send["Subject"] = "Blog reader"
        server.sendmail(EMAIL, [EMAIL], msg=to_send.as_string())


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
        email_msg = f"Name: {name}\nEmail: {email}\nTel: {tel}\nMessage: {msg}"
        send_msg(email_msg)
    return render_template("contact.html", header=h1)


@app.route("/post/<pid>")
def get_post(pid):
    posts_filter = [p for p in POSTS if str(p["id"]) == pid]
    post = posts_filter[0] if len(posts_filter) == 1 else Exception(ValueError)
    return render_template("post.html", post=post)


if __name__ == '__main__':
    app.run(debug=True)
