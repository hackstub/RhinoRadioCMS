from .. import db
from datetime import datetime
from .author import Author
from .section import Section
from .meta import Label, Tag

publications = db.Table('publications',
    db.Column('podcast_id', db.Integer, db.ForeignKey('podcasts.id'), primary_key=True),
    db.Column('author_id', db.Integer, db.ForeignKey('authors.id'), primary_key=True))

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
    date = db.Column(db.Date, default=datetime.utcnow)
    mood = db.Column(db.SmallInteger)
    link = db.Column(db.String(256))
    type = db.Column(db.Boolean())
    tags = db.Column(db.Integer, db.ForeignKey('tags.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    public = db.Column(db.Boolean())
