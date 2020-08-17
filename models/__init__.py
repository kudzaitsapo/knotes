from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):
    """Model for user accounts."""
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True)
    username = db.Column(db.String,
                         nullable=False,
                         unique=False)
    email = db.Column(db.String(40),
                      unique=True,
                      nullable=False)
    password = db.Column(db.String(200),
                         primary_key=False,
                         unique=False,
                         nullable=False)


    def __repr__(self):
        return '<User {}>'.format(self.username)


    def set_password(self, password):
        self.password = generate_password_hash(password)


    def check_password(self, plaintext):
        return check_password_hash(self.password, plaintext)


class ContactMessage(db.Model):
    """Model for contact us messages"""
    __tablename__ = 'contact_messages'

    id = db.Column(db.Integer,
                    primary_key=True)
    name = db.Column(db.String(80), 
                      nullable=False)
    email = db.Column(db.String(80), 
                        nullable=False)
    message = db.Column(db.String(200),
                        nullable=False)
    created_at = db.Column(db.DateTime,
                            default=datetime.utcnow)

    def __repr__(self):
        return '<ContactMessage {}>'.format(str(self.id))


class Category(db.Model):
    """Model for article categories"""
    __tablename__ = 'categories'

    id = db.Column(db.Integer,
                    primary_key=True)
    name = db.Column(db.String(80), 
                      unique=True)


    def __repr__(self):
        return '<Category {}>'.format(self.name)
    

class Article(db.Model):
    """Model for articles"""
    __tablename__ = 'articles'

    id = db.Column(db.Integer,
                    primary_key=True)
    title = db.Column(db.String(200),
                      nullable=False)
    slug = db.Column(db.String, 
                     nullable=False, 
                     unique=True)
    category = db.Column(db.Integer,
                         db.ForeignKey('categories.id'))
    content = db.Column(db.Text,
                        nullable=False)
    status = db.Column(db.Integer,
                        default=0)
    created_at = db.Column(db.DateTime,
                            default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,
                            onupdate=datetime.utcnow)


    def __repr__(self):
        return '<Article {}>'.format(self.title)