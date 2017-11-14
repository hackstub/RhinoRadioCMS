from .. import db
from datetime import datetime
from geoalchemy2 import Geometry
from .contributor import Contributor
from .channel import Channel
from .section import Section
from .tag import Tag

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


class Podcast(db.Model):
    """ Podcasts class and table, extending Channel class """
    __tablename__ = 'podcasts'

    id = db.Column(db.Integer, primary_key=True)
    # Title of the podcast
    title = db.Column(db.String(256))
    # Contibutors authoring the podcast
    contributors = db.relationship('Contributor',
                secondary='podcasts_authors',
                lazy='select',
                back_populates='podcasts')
    # Sections of the podcast
    sections = db.relationship('Section',
                backref=db.backref('podcast', lazy='select'),
                lazy='select')
    # Mood of the podcast
    mood = db.Column(db.String(128))
    # Musical or non-musical
    music = db.Column(db.Boolean())
    # Channel of the podcast
    channels = db.relationship('Channel',
                back_populates='podcasts',
                lazy='select')
    # Channel id of the podcast
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'))
    # Date of recording
    date = db.Column(db.Date, default=datetime.utcnow)
    # Link to the audio file
    link = db.Column(db.String(256))
    # Datetime of publication
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    # Place of recording/playing
    location = db.Column(Geometry(geometry_type='POINT', srid=0))
    # License of the podcast
    license = db.Column('license', db.String(256))
    # Tags of the podcasts
    tags = db.relationship('Tag',
                backref=db.backref('podcasts', lazy='select'),
                lazy='select')
    # Description of the channel
    desc = db.Column(db.Text)

    def __repr__(self):
        return '<PODCAST %r>' % self.title

    def list(filter='', order='', number=10):
        podcasts = Podcast.query.filter(filter).order_by(
            Podcast.timestamp.desc(),
            order
        ).paginate(per_page=number).items
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
