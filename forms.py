from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, HiddenField, EmailField
from wtforms.validators import URL, InputRequired, Email
from flask_ckeditor import CKEditorField

# WTForm


class CreatePostForm(Form):
    hidden_tag = HiddenField()
    title = StringField("Blog Post Title", validators=[InputRequired()])
    subtitle = StringField("Subtitle", validators=[InputRequired()])
    author = StringField("Your Name", validators=[InputRequired()])
    img_url = StringField("Blog Image URL", validators=[InputRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[InputRequired()])
    submit = SubmitField("Submit Post")


class RegisterForm(Form):
    hidden_tag = HiddenField()
    name = StringField("Name", validators=[InputRequired()])
    user_email = EmailField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Sign Me Up!")


class LoginForm(Form):
    hidden_tag = HiddenField()
    user_email = EmailField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Let Me In!")

