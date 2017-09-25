from . import db, admin
from datetime import datetime
from flask_admin.contrib.sqla import ModelView

class Publication(db.Model):
    __tablename__ = 'publications'
    id = db.Column(db.Integer)
    podcast_id = db.Column(db.Integer, db.ForeignKey('podcasts.id'),
                            primary_key=True)
#     section_id = db.Column(db.Integer,
#                             db.ForeignKey('sections.id'),
#                             nullable=True)
    author_id = db.Column(db.Integer,
                            db.ForeignKey('authors.id'),
                            primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Podcast(db.Model):
    __tablename__ = 'podcasts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(512), unique=True)
    authors = db.relationship('Publication', backref='podcasts', lazy='dynamic', cascade='all, delete-orphan')
    desc = db.Column(db.Text)
    label = db.Column(db.String(128))
    date = db.Column(db.Date)
    mood = db.Column(db.SmallInteger)    
    link = db.Column(db.String(256))
#     type = db.Column(db.Boolean())
    tags = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def name():
        return name
    
    def link():
        return link        

class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    publications = db.relationship('Publication', backref='authors', lazy='dynamic', cascade='all, delete-orphan')
    status = db.Column(db.String(128))
    bio = db.Column(db.Text)

class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    date = db.Column(db.Date, default=datetime.utcnow)
    content = db.Column(db.Text)


admin.add_view(ModelView(BlogPost, db.session))
admin.add_view(ModelView(Podcast, db.session))
admin.add_view(ModelView(Author, db.session))