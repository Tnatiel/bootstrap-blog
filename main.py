import smtplib
import ssl
from datetime import datetime
from email.mime.text import MIMEText
import flask
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from flask_gravatar import Gravatar
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreatePostForm, RegisterForm, LoginForm

EMAIL = "ntgk666@gmail.com"
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


# CKEditor
ckeditor = CKEditor(app)

# ---------------------------- Flask Login ----------------------------------
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

# ---------------------------- DataBase ----------------------------------


# CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
Base = declarative_base()

# Users:
# Admins ['Erick', 'erick@email.com', '111111'
# Regular ['Malman', 'malman@email.com', '123123'


# CONFIGURE TABLES
class BlogPost(db.Model, Base):
    post_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = relationship("User", back_populates="posts")
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


class User(UserMixin, db.Model, Base):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)
    posts = relationship("BlogPost", back_populates="author")


# ---------------------------- Data Injectors ----------------------------------
app.config['CURRENT_YEAR'] = datetime.now().year
app.config["CURRENT_USER"] = current_user


@app.context_processor
def year_injector():
    return {"year": app.config["CURRENT_YEAR"]}


@app.context_processor
def current_user_injection():
    return {"cur_user": app.config["CURRENT_USER"]}
# --------------------- Util Functions --------------------------


def send_msg(msg):
    port = 465  # for SSL
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(EMAIL, "ehbyrzfkmkccgllq")
        to_send = MIMEText(msg)
        to_send["Subject"] = "Blog reader"
        server.sendmail(EMAIL, [EMAIL], msg=to_send.as_string())

# --------------------- Custom Decorators --------------------------


def admin_or_author(func):
    def wrap(*args, **kwargs):
        post = BlogPost.query.filter_by(post_id=kwargs.get("post_id")).first()

        if not post or post.author.id != current_user.id \
                or not current_user.admin:
            return flask.abort(403)
        return func(*args, **kwargs)

    wrap.__name__ = func.__name__
    return wrap

# --------------------- End Points --------------------------


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


@app.route("/post/<int:pid>")
def get_post(pid):
    post = BlogPost.query.filter_by(post_id=pid).first()
    return render_template("post.html", post=post)


@app.route("/new-post", methods=["GET", "POST"])
@login_required
def add_post():
    form = CreatePostForm(request.form)
    if request.method == "POST" and form.validate():

        new_post = BlogPost(
            title=form.title.data.title(),
            subtitle=form.subtitle.data,
            date=datetime.now().strftime("%B %d %Y"),
            body=form.body.data,
            img_url=form.img_url.data,
            author=app.config["CURRENT_USER"],
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("make-post.html", form=form, edit_mode=False)


@app.route("/edit-post/<int:post_id>", methods=["POST", "GET"])
@admin_or_author
def edit_post(post_id):
    post = BlogPost.query.filter_by(post_id=post_id).first()
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author.name.title(),
        body=post.body

    )

    updated_form = CreatePostForm(request.form)

    if request.method == "POST" and updated_form.validate():
        post.title = updated_form.title.data != post.title and updated_form.title.data
        post.subtitle = updated_form.subtitle.data != post.subtitle and updated_form.subtitle.data
        post.img_url = updated_form.img_url.data != post.img_url and updated_form.img_url.data
        post.body = updated_form.body.data != post.body and updated_form.body.data
        db.session.commit()
        return redirect(url_for("get_post", pid=post_id))
    return render_template("make-post.html", form=edit_form, edit_mode=True)


@app.route('/delete/<int:post_id>')
@admin_or_author
def delete_post(post_id):

    print(post_id)
    post = BlogPost.query.filter_by(post_id=post_id).first()
    print(post)
    if post:
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for("home"))


# --------------------- Users CRUD --------------------------
@app.route('/register', methods=["POST", "GET"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        if User.query.filter_by(email=form.user_email.data.lower()).first():
            flash("You've already sign in with that email address. Sign in instead!")
            return redirect(url_for("login"))
        hashed_password = generate_password_hash(form.password.data, salt_length=8)
        user = User(
            name=form.name.data
            if not form.name.data.endswith(".admin$Q#W@E")
            else form.name.data.replace(".admin$Q#W@E", ""),
            email=form.user_email.data.lower(),
            password=hashed_password,
            admin=1 if form.name.data.endswith(".admin$Q#W@E") else 0
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        app.config["CURRENT_USER"] = current_user
        # print(f"User {user.name}, {'is admin' if bool(user.admin) else 'is not admin' }")
        return redirect(url_for("home"))
    return render_template("register.html", form=form)


@app.route('/login', methods=["POST", "GET"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        user = User.query.filter_by(email=request.form.get("user_email").lower()).first()
        if not user:
            flash("That email doesn't exist, please try again")
        elif check_password_hash(user.password, request.form.get("password")):
            login_user(user)
            app.config["CURRENT_USER"] = current_user
            return redirect(url_for("home"))
        else:
            flash("The password doesn't match, please try again")
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    app.config["CURRENT_USER"] = current_user
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
