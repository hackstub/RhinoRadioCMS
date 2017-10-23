from . import db, admin
from datetime import datetime
from flask_admin.contrib.sqla import ModelView

## Database models

# Taxonomy table
publications = db.Table('publications',
    db.Column('podcast_id', db.Integer, db.ForeignKey('podcasts.id'), primary_key=True),
    db.Column('author_id', db.Integer, db.ForeignKey('authors.id'), primary_key=True))

# Classes

class Podcast(db.Model):
    __tablename__ = 'podcasts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    authors = db.relationship('Author',
                secondary='publications',
                lazy='select',
                back_populates='podcasts')
    sections = db.relationship('Section',
                backref = db.backref('podcast', lazy='select'),
                lazy='select')
    desc = db.Column(db.Text)
    label_id = db.Column(db.Integer, db.ForeignKey('labels.id'))
    date = db.Column(db.Date)
    mood = db.Column(db.SmallInteger)
    link = db.Column(db.String(256))
    type = db.Column(db.Boolean())
    tags = db.Column(db.Integer, db.ForeignKey('tags.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Section(db.Model):
    __tablename__ = "sections"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    subtitle = db.Column(db.String(256))
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    podcast_id = db.Column(db.Integer, db.ForeignKey('podcasts.id'))
    label_id = db.Column(db.Integer, db.ForeignKey('labels.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    status = db.Column(db.String(128))
    bio = db.Column(db.Text)
    podcasts = db.relationship('Podcast',
                secondary='publications')

    def __str__(self):
        return self.name

class Label(db.Model):
    __tablename__ = "labels"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    desc = db.Column(db.Text)

class Tags(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))


class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    date = db.Column(db.Date, default=datetime.utcnow)
    content = db.Column(db.Text)

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    place = db.Column(db.String(128))
    begin = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    desc = db.Column(db.Text)

# Admin views

class PodcastView(ModelView):
    create_modal = True

    form_choices = {
        'mood': [
            ('slow', 'Au pas'),
            ('medium', 'Au trot'),
            ('fast', 'Au galop !')
        ]
    }

    form_ajax_refs = {
    }

class SectionView(ModelView):
    create_modal = True

    columns_exclude = ['timestamp']

admin.add_view(ModelView(BlogPost, db.session))
admin.add_view(PodcastView(Podcast, db.session))
admin.add_view(ModelView(Author, db.session))
admin.add_view(ModelView(Event, db.session))
