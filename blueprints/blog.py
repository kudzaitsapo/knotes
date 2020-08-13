from flask import Blueprint, render_template, redirect


blog = Blueprint('blog', __name__)


@blog.route('/')
def index():
    return render_template('pages/index.html')


@blog.route('/articles/<slug>')
def read_article():
    return "Read an article"

@blog.route('/about')
def about_me():
    return "About me"


@blog.route('/contact')
def contact_me():
    return "Get in touch with me"