from flask import Blueprint, render_template, redirect, request, flash
from models import db, Article, Category, ContactMessage


blog = Blueprint('blog', __name__)


@blog.route('/')
@blog.route('/articles')
def index():
    return render_template('pages/index.html')


@blog.route('/articles/<slug>')
def read_article(slug):
    return render_template('pages/read-article.html')

@blog.route('/about')
def about_me():
    return render_template('pages/about.html')


@blog.route('/contact', methods=['GET', 'POST'])
def contact_me():
    if request.method == 'POST':
        person_name = request.form.get('name')
        person_email = request.form.get('email')
        message = request.form.get('message')
        if person_email and person_name and message:
            try:
                contact_message = ContactMessage(name=person_name, email=person_email, message=message)
                db.session.add(contact_message)
                db.session.commit()
                flash("Your message has been sent. I will respond to you soon.", "success")
            except Exception as error:
                print('Error: {}'.format(str(error)))
                flash("Uh oh! Something crashed, but don't worry. It'll be fixed soon... Probably...", "danger")
        else:
            flash("Well, could you try entering all the fields?", "danger")
    return render_template('pages/contact.html')