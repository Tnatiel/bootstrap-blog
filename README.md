# Flask Bootstrap Blog

## Overview

Flask Bootstrap Blog is a user-friendly web application that allows users to 
create, edit, and delete blog posts. This blog project is built with Flask, 
a Python-based web framework, and SQLite database support. It uses Bootstrap example templates, 
Jinja, and Flask for the front and back end. The site mostly uses Bootstrap classes with little adaptations.


## Prerequisites

Before you start working with Flask Bootstrap Blog, 
you need to ensure that you have the following tools installed:
* Python 3.10^
* Flask
* Flask-Bootstrap
* Flask-CKEditor
* Flask-SQLAlchemy
* WTForms

## How to Run the Project

To run this project on your local machine, follow these steps:

1. Clone this repository

       git clone https://github.com/your-username/bootstrap-blog.git

2. Navigate to the project directory

        cd bootstrap-blog

3. Install the required packages
         
         pip install -r requirments.txt

4. Run the application

        python main.py

5. Open your web browser and navigate to http://localhost:5000 to see the blog.

## Features
Flask Bootstrap Blog has the following features:

* Home page with a list of blog posts.
* Post page with the full text of a blog post.
* About page with information about the blog.
* Contact page with a form to send an email message to the blog owner.
* View existing blog posts
* Create new posts
* Edit existing posts
* Delete posts

## File Structure

* `main.py`: The Flask application file that runs the blog.
* `header.html`: The header of the blog's HTML template that contains the navigation bar.
* `footer.html`: The footer of the blog's HTML template that contains the social media links.
* `index.html`: The home page of the blog that displays a list of blog posts.
* `post.html`: The post page of the blog that displays the full text of a blog post.
* `about.html`: The about page of the blog that displays information about the blog.
* `contact.html`: The contact page of the blog that displays a form to send an email message to the blog owner.
* `make-post.html`: The edit/add page of the blog that displays a form to edit/add the post.


## Technologies & Tools

* [Bootstrap](https://getbootstrap.com/)
* [Flask](https://flask.palletsprojects.com/)
* [Jinja](https://jinja.palletsprojects.com/)
* [smtplib](https://docs.python.org/3/library/smtplib.html)
* [datetime](https://docs.python.org/3/library/datetime.html)
* [requests](https://docs.python-requests.org/en/latest/)
* [Font Awesome icons](https://fontawesome.com/)
* [Flask-Bootstrap](https://pythonhosted.org/Flask-Bootstrap/index.html)
* [Flask-CKEditor](https://flask-ckeditor.readthedocs.io/en/latest/basic.html)
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/)
* [WTForms](https://wtforms.readthedocs.io/en/3.0.x/)

The blog template is adapted from the Bootstrap Blog template by Start [Bootstrap](https://startbootstrap.com/).
