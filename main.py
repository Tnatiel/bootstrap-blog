import smtplib
import ssl
from email.mime.text import MIMEText
from datetime import datetime
import requests as req
from flask import Flask, render_template, request

EMAIL = "ntgk666@gmail.com"
POSTS = req.get("https://api.npoint.io/511981ad9e97d831283f").json()
app = Flask(__name__)
app.config['CURRENT_YEAR'] = datetime.now().year


def send_msg(msg):
    print(msg)
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
