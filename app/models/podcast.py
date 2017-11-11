from .. import db
from datetime import datetime
from geoalchemy2 import Geometry
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
    title = db.Column(db.String(256))
    """ Title of the podcast """
    contributors = db.relationship('Contributor',
                secondary='publications',
                lazy='select',
                back_populates='podcasts')
    """ Contibutors authoring the podcast """
    sections = db.relationship('Section',
                backref=db.backref('podcast', lazy='select'),
                lazy='select')
    """ Sections of the podcast """
    desc = db.Column(db.Text)
    """ Description of the podcast """
    label_id = db.Column(db.Integer, db.ForeignKey('labels.id'))
    """ Label of the podcast """
    date = db.Column(db.Date, default=datetime.utcnow)
    """ Date of publication """
    mood = db.Column(db.String(128))
    """ Mood of the podcast """
    link = db.Column(db.String(256))
    """ Link to the audio file """
    type = db.Column(db.String(128))
    """ Type : musical or non-musical """
    tags = db.relationship('Tag',
                backref=db.backref('podcasts', lazy='select'),
                lazy='select')
    """ Tags of the podcasts """
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    """ Datetime of publication """
    public = db.Column(db.Boolean())
    """ State of te publication """
    place = db.Column(Geometry(geometry_type='POINT', srid=0))
    """ Place of recording/playing """
    itinerary = db.Column(Geometry(geometry_type='LINESTRING', srid=0))
    """ Itinerary of recording/playing """

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
                label_id = randint(1, 11),
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
            db.session.add(p)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
