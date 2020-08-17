from flask import Blueprint, render_template, redirect, request, flash
from models import db, Article, Category, ContactMessage
from sqlalchemy import desc


blog = Blueprint('blog', __name__)


@blog.route('/')
@blog.route('/articles')
def index():
    articles = Article.query.filter(Article.status == 1) \
                    .order_by(desc(Article.created_at)) \
                    .all()
    return render_template('pages/index.html', articles=articles)


@blog.route('/articles/<slug>')
def read_article(slug):
    article = Article.query.join(Category, Article.category == Category.id) \
                .add_columns(Article.title, Article.updated_at, Article.created_at, Article.content, Category.name.label('category')) \
                .filter(Article.slug == slug).first_or_404()
    return render_template('pages/read-article.html', article=article)

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