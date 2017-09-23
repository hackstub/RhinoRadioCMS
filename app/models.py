from . import db, admin
from datetime import datetime
from flask_admin.contrib.sqla import ModelView

# class Publication(db.Model):
#     __tablename__ = 'pubs'
#     id = db.Column(db.Integer)
#     podcast_id = db.Column(db.Integer, db.ForeignKey('podcasts.id'), primary_key=True)
# #     section_id = db.Column(db.Integer, db.ForeignKey('sections.id'), nullable=True)
#     author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), primary_key=True)
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow)
# 
#     
# 
# 
# class Podcast(db.Model):
#     __tablename__ = 'podcasts'
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(512), unique=True)
#     authors = db.relationship('Publication', foreign_keys=[Publication.author_id], backref=db.backref('podcasts', lazy="select"), lazy="join", cascade='all,delete-orphan')
#     desc = db.Column(db.Text)
#     label = db.Column(db.String(128))
#     date = db.Column(db.Date)
#     mood = db.Column(db.SmallInteger)    
#     link = db.Column(db.String(256))
#     type = db.Column(db.Boolean())
#     tags = db.Column(db.String(128))
#     timestamp = db.Column(db.DateTime, default=datetime.utcnow)
#     
#     def name():
#         return name
#     
#     def link():
#         return link
#         
# 
# class Author(db.Model):
#     __tablename__ = 'authors'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(128))
#     publications = db.relationship('Publication', foreign_keys=[Publication.id], backref=db.backref('authors', lazy="join"), lazy="select", cascade='all,delete-orphan')
#     status = db.Column(db.String(128))
#     bio = db.Column(db.Text)

class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    followed = db.relationship('Follow',
                               foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    followers = db.relationship('Follow',
                                foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')

class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    date = db.Column(db.Date, default=datetime.utcnow)
    content = db.Column(db.Text)


admin.add_view(ModelView(BlogPost, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Follow, db.session))