from datetime import datetime
from geoalchemy2 import Geometry

from .. import db
from .relationships import podcasts_contributors


class Podcast(db.Model):
    """ Podcasts class and table, extending Channel class """
    __tablename__ = 'podcasts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    description = db.Column(db.Text)
    # Date of recording
    date = db.Column(db.Date, default=datetime.utcnow)
    # Datetime of publication
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    # Place of recording/playing
    # location = db.Column(Geometry(geometry_type='POINT', srid=0))
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'))
    contributors = db.relationship(
        'Contributor',
        secondary='podcasts_contributors',
        cascade='all, delete-orphan',
        single_parent='True',
        lazy='select',
        back_populates='podcasts')
    # Sections of the podcast if it contains several content types/authors/...
    sections = db.relationship(
        'Section',
        backref=db.backref('podcast', lazy='select'),
        lazy='select')
    tags = db.relationship(
        'Tag',
        backref=db.backref('podcasts', lazy='select'),
        lazy='select')
    link = db.Column(db.String(256))
    license = db.Column('license', db.String(256))
    mood = db.Column(db.String(128))
    # Musical or non-musical
    music = db.Column(db.Boolean())
    #FIXME ADD COLLECTIVE


    def __repr__(self):
        return '<PODCAST %r>' % self.name

    def __str__(self):
        return self.name

    def list(filter='', order='', number=10):
        from .channel import Channel

        podcasts = Podcast.query.filter(filter)            \
            .join(Channel, Channel.id==Podcast.channel_id) \
            .order_by(Podcast.timestamp.desc(), order)     \
            .paginate(per_page=number).items
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
                name=forgery_py.lorem_ipsum.title(),
                description=forgery_py.lorem_ipsum.paragraph(),
                channel_id=randint(1, 11),
                mood=choice(['slow', 'medium', 'fast']),
                link=choice([
                    'http://podcast.radiorhino.eu/Émissions/Cachemire%20Darbuqqa/Cachemire%20épisode%201.mp3',
                    'http://podcast.radiorhino.eu/Émissions/Cachemire%20Darbuqqa/Cachemire%20épisode%202.mp3',
                    'http://podcast.radiorhino.eu/Émissions/Cachemire%20Darbuqqa/Cachemire%20épisode%205.mp3',
                    'http://podcast.radiorhino.eu/Émissions/Cachemire%20Darbuqqa/Cachmire%20épisode%206-1.mp3',
                    'http://podcast.radiorhino.eu/Émissions/Cachemire%20Darbuqqa/cachemire%20darbuqqa%2012-1%20fausse%20stéréo.mp3']),
                music=choice([True, False]),
                license=choice(['Copyright', 'CC-BY-NC',
                                'CC-BY-SA', 'CC-BY-ND'])
            )
            db.session.add(p)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
