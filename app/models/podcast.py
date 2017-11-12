from .. import db
from datetime import datetime
from geoalchemy2 import Geometry
from .contributor import Contributor
from .channel import Channel
from .section import Section
from . import *
from .tag import *

""" Taxonomy table """
podcasts_authors = db.Table('podcasts_authors',
    db.Column('podcast_id',
        db.Integer,
        db.ForeignKey('podcasts.id'),
        primary_key=True),
    db.Column('contributor_id',
        db.Integer,
        db.ForeignKey('contributors.id'),
        primary_key=True))

""" Podcasts class and table, extending Channel class """
class Podcast(db.Model):
    __tablename__ = 'podcasts'
    podcast_id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    """ Title of the podcast """
    contributors = db.relationship('Contributor',
                secondary='podcasts_authors',
                lazy='select',
                back_populates='podcasts')
    """ Contibutors authoring the podcast """
    sections = db.relationship('Section',
                backref=db.backref('podcast', lazy='select'),
                lazy='select')
    """ Sections of the podcast """
    mood = db.Column(db.String(128))
    """ Mood of the podcast """
    music = db.Column(db.Boolean())
    """ Musical or non-musical """
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'))
    """ Channel of the podcast """
    date = db.Column(db.Date, default=datetime.utcnow)
    """ Date of recording """
    link = db.Column(db.String(256))
    """ Link to the audio file """
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    """ Datetime of publication """
    location = db.Column(Geometry(geometry_type='POINT', srid=0))
    """ Place of recording/playing """
    license = db.Column('license', db.String(256))
    """ License of the podcast """
    tags = db.relationship('Tag',
                backref=db.backref('podcasts', lazy='select'),
                lazy='select')
    """ Tags of the podcasts """
    desc = db.Column(db.Text)
    """ Description of the channel """

    def list(filter='', order='', number=10):
        podcasts = Podcast.query.\
            filter(filter).\
            order_by(Podcast.timestamp.desc(), order).\
            paginate(per_page=number).items
        return podcasts

    @staticmethod
    def fake_feed(count=10):
        """ Randomly feed the database """
        from sqlalchemy.exc import IntegrityError
        from random import seed, randint, choice
        import forgery_py

        seed()
        for i in range(count):
            p = Podcast(
                title = forgery_py.lorem_ipsum.title(),
                desc = forgery_py.lorem_ipsum.paragraph(),
                channel_id = randint(1, 11),
                mood = choice(['slow', 'medium', 'fast']),
                link = choice([
                    'http://podcast.radiorhino.eu/Émissions/Cachemire%20Darbuqqa/Cachemire%20épisode%201.mp3',
                    'http://podcast.radiorhino.eu/Émissions/Cachemire%20Darbuqqa/Cachemire%20épisode%202.mp3',
                    'http://podcast.radiorhino.eu/Émissions/Cachemire%20Darbuqqa/Cachemire%20épisode%205.mp3',
                    'http://podcast.radiorhino.eu/Émissions/Cachemire%20Darbuqqa/Cachmire%20épisode%206-1.mp3',
                    'http://podcast.radiorhino.eu/Émissions/Cachemire%20Darbuqqa/cachemire%20darbuqqa%2012-1%20fausse%20stéréo.mp3']),
                music = choice([True, False])
            )
            db.session.add(p)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
