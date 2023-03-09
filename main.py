import smtplib
import ssl
from datetime import datetime
from email.mime.text import MIMEText
from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from flask_gravatar import Gravatar
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreatePostForm, RegisterForm, LoginForm

EMAIL = "ntgk666@gmail.com"
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


# CKEditor
ckeditor = CKEditor(app)
app.config['CKEDITOR_PKG_TYPE'] = 'basic'

# ---------------------------- Flask Login ----------------------------------
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------------------------- DataBase ----------------------------------

# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# CONFIGURE TABLES
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)


# ---------------------------- Data Injectors ----------------------------------
app.config['CURRENT_YEAR'] = datetime.now().year
app.config["LOGGED_IN"] = False


@app.context_processor
def year_injector():
    return {"year": app.config["CURRENT_YEAR"]}


@app.context_processor
def is_logged():
    return {"logged_in": app.config["LOGGED_IN"]}
# --------------------- Util Functions --------------------------


def send_msg(msg):
    port = 465  # for SSL
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(EMAIL, "ehbyrzfkmkccgllq")
        to_send = MIMEText(msg)
        to_send["Subject"] = "Blog reader"
        server.sendmail(EMAIL, [EMAIL], msg=to_send.as_string())

# --------------------- END POINTS --------------------------


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


# --------------------- Blog CRUD --------------------------

@app.route("/")
def home():
    posts = db.session.query(BlogPost).all()
    return render_template("index.html", posts=posts)


@app.route("/post/<pid>")
def get_post(pid):
    posts = db.session.query(BlogPost).all()
    posts_filter = [p for p in posts if str(p.id) == pid]
    post = posts_filter[0] if len(posts_filter) == 1 else Exception(ValueError)
    return render_template("post.html", post=post)


@app.route("/new-post", methods=["GET", "POST"])
def add_post():
    form = CreatePostForm(request.form)
    if request.method == "POST" and form.validate():
        new_post = BlogPost(
            title=request.form.get("title"),
            subtitle=request.form.get("subtitle"),
            date=datetime.now().strftime("%B %d %Y"),
            body=request.form.get("body"),
            img_url=request.form.get("img_url"),
            author=request.form.get("author")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("make-post.html", form=form, edit_mode=False)


@app.route("/edit-post/<post_id>", methods=["POST", "GET"])
def edit_post(post_id):
    post = BlogPost.query.filter_by(id=post_id).first()
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    updated_form = CreatePostForm(request.form)

    if request.method == "POST" and updated_form.validate():
        post.title = updated_form.title != post.title and updated_form.title.data
        post.subtitle = updated_form.subtitle != post.subtitle and updated_form.subtitle.data
        post.img_url = updated_form.img_url != post.img_url and updated_form.img_url.data
        post.author = updated_form.author != post.author and updated_form.author.data
        post.body = updated_form.body != post.body and updated_form.body.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("make-post.html", form=edit_form, edit_mode=True)


@app.route('/delete/<pid>')
def delete_post(pid):
    post = BlogPost.query.get(pid)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for("home"))


# --------------------- Users CRUD --------------------------
@app.route('/register', methods=["POST", "GET"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        hashed_password = generate_password_hash(form.password.data, salt_length=8)
        user = User(
            name=form.name.data,
            email=form.user_email.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        app.config["LOGGED_IN"] = True
        return redirect(url_for("home"))
    return render_template("register.html", form=form)


@app.route('/login', methods=["POST", "GET"])
def login():
    form = LoginForm(request.form)
    error = None
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email=request.form.get("user_email")).first()
        if not user:
            error = "That email doesn't exist, please try again"
        elif check_password_hash(user.password, request.form.get("password")):
            login_user(user)
            app.config["LOGGED_IN"] = True
            return redirect(url_for("home"))
        else:
            error = "The password doesn't match, please try again"
    return render_template("login.html", form=form, error=error)


@app.route('/logout')
def logout():
    logout_user()
    app.config["LOGGED_IN"] = False
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
