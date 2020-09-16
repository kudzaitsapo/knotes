from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify, current_app
from flask_login import login_required, current_user, login_user, logout_user
from forms import LoginForm
from models import db, User, Article, Category, ContactMessage
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from slugify import slugify

import os


admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
@login_required
def index():
    return render_template('admin/index.html')


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))


    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('admin.index')

            return redirect(next_page)
        else:
            flash('Invalid username or password')
    return render_template('admin/login.html', form=form)


@admin_bp.route('/articles')
@login_required
def articles():
    page = request.args.get('page', 1, type=int)
    articles = Article.query.join(Category, Article.category == Category.id) \
                    .add_columns(Article.id, Article.title, Article.updated_at, Article.created_at, Article.status, Category.name.label('category')) \
                    .paginate(page, 10, False)
    next_url = url_for('admin.articles', page=articles.next_num) if articles.has_next else None
    prev_url = url_for('admin.articles', page=articles.prev_num) if articles.has_prev else None
    return render_template('admin/articles.html', articles=articles.items, next_url=next_url, prev_url=prev_url)


@admin_bp.route('/articles/add-article', methods=['GET', 'POST'])
@login_required
def add_article():
    categories = Category.query.all()
    if request.method == 'POST':
        response = { 'icon': 'error', 'message': '' }
        try:
            title = request.form.get('title')
            category = request.form.get('category')
            article_content = str(request.form.get('article')).replace('font-size: 1rem;', '')
            status = request.form.get('status')

            article = Article(title=title, slug=slugify(title), category=category, content=article_content, status=status)
            db.session.add(article)
            db.session.commit()
            response['icon'] = 'success'
            response['message'] = 'Successfully added article.'
        except Exception as error:
            print('[-] Error {}'.format(str(error)))
            response['message'] = 'Oops! Failed to add this one!'
        return jsonify(response)
    return render_template('admin/add-article.html', categories=categories)


@admin_bp.route('/categories')
@login_required
def categories():
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)

@admin_bp.route('/categories/add-category', methods=['GET', 'POST'])
@login_required
def add_category():
    if request.method == 'POST':
        category_name = request.form.get('category')
        response = { 'icon': 'error', 'message': '' }
        try:
            category = Category(name=category_name)
            db.session.add(category)
            db.session.commit()
            response['icon'] = 'success'
            response['message'] = 'Successfully added category!'
        except Exception as error:
            print('[-] Error: {}'.format(str(error)))
            response['message'] = 'Oops! That one failed!'

        return jsonify(response)
    return render_template('admin/add-category.html')


@admin_bp.route('/categories/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    category = Category.query.get(int(id))
    if request.method == 'POST':
        category_name = request.form.get('category')
        response = { 'icon': 'error', 'message': '' }
        try:
            category.name = category_name
            db.session.commit()
            response['icon'] = 'success'
            response['message'] = 'Yipppeee, we saved it.'
        except Exception as error:
            print('[-] Error: {}'.format(str(error)))
            response['message'] = 'Uh oh! Something crashed!'
        return jsonify(response)
    return render_template('admin/edit-category.html', category=category)


@admin_bp.route('/articles/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit_article(id):
    article = Article.query.filter(Article.id == id).first()
    categories = Category.query.all()

    if request.method == 'POST':
        response = { 'icon': 'error', 'message': '' }
       
        try:
            article.title = request.form.get('title')
            article.content = str(request.form.get('article')).replace('font-size: 1rem;', '')
            article.status = request.form.get('status')
            article.category = request.form.get('category')
            db.session.commit()
            response['icon'] = 'success'
            response['message'] = 'Successfully saved the article'
        except Exception as error:
            print('[-] Error: {}'.format(str(error)))
            response['message'] = 'Oops! That one failed!'
        return jsonify(response)
    return render_template('admin/edit-article.html', article=article, categories=categories)


@admin_bp.route('/messages')
@login_required
def get_messages():
    page = request.args.get('page', 1, type=int)
    messages = ContactMessage.query.paginate(page, 20, False)
    next_url = url_for('admin.get_messages', page=messages.next_num) if messages.has_next else None
    prev_url = url_for('admin.get_messages', page=messages.prev_num) if messages.has_prev else None
    return render_template('admin/messages.html', messages = messages.items, next_url=next_url, prev_url=prev_url)


@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))