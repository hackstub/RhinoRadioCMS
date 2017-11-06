from .. import db
from datetime import datetime
from .contributor import Contributor
from .section import Section
from .label import *
from .tag import *

""" Taxonomy table """
publications = db.Table('publications',
    db.Column('podcast_id', db.Integer, db.ForeignKey('podcasts.id'), primary_key=True),
    db.Column('contributor_id', db.Integer, db.ForeignKey('contributors.id'), primary_key=True))

""" Podcasts class and table """
class Podcast(db.Model):
    __tablename__ = 'podcasts'
    id = db.Column(db.Integer, primary_key=True)
    """ Title of the podcast """
    title = db.Column(db.String(256))
    """ Contibutors authoring the podcast """
    contributors = db.relationship('Contributor',
                secondary='publications',
                lazy='select',
                back_populates='podcasts')
    """ Sections of the podcast """
    sections = db.relationship('Section',
                backref=db.backref('podcast', lazy='select'),
                lazy='select')
    """ Description of the podcast """
    desc = db.Column(db.Text)
    """ Label of the podcast """
    label_id = db.Column(db.Integer, db.ForeignKey('labels.id'))
    """ Date of publication """
    date = db.Column(db.Date, default=datetime.utcnow)
    """ Mood of the podcast """
    mood = db.Column(db.SmallInteger)
    """ Link to the audio file """
    link = db.Column(db.String(256))
    """ Type : musical or non-musical """
    type = db.Column(db.Boolean())
    """ Tags of the podcasts """
    tags = db.relationship('Tag',
                backref=db.backref('podcasts', lazy='select'),
                lazy='select')
    """ Datetime of publication """
    timestamp = db.Column(db.DateTime, primary_key=True, default=datetime.utcnow)
    """ State of te publication """
    public = db.Column(db.Boolean())

    @staticmethod
    def fake_feed(count=100):
        """ Randomly feed the database """
        from sqlalchemy.exc import IntegrityError
        from random import seed, randint, choice
        import forgery_py

        seed()
        for i in range(count):
            p = Podcast(
                title = forgery_py.lorem_ipsum.title(),
                desc = forgery_py.lorem_ipsum.paragraph(),
                label_id = randint(0, 10),
                mood = choice(['slow', 'medium', 'fast']),
                link = choice([
                    'http://podcast.radiorhino.eu/Émissions/Cachemire%20Darbuqqa/Cachemire%20épisode%201.mp3',
                    'http://podcast.radiorhino.eu/Émissions/Cachemire%20Darbuqqa/Cachemire%20épisode%202.mp3',
                    'http://podcast.radiorhino.eu/Émissions/Cachemire%20Darbuqqa/Cachemire%20épisode%205.mp3',
                    'http://podcast.radiorhino.eu/Émissions/Cachemire%20Darbuqqa/Cachmire%20épisode%206-1.mp3',
                    'http://podcast.radiorhino.eu/Émissions/Cachemire%20Darbuqqa/cachemire%20darbuqqa%2012-1%20fausse%20stéréo.mp3']),
                type = choice([True, False]),
                public = True
            )
