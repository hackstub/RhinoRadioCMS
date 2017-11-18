from datetime import datetime
from geoalchemy2 import Geometry

from .. import db
from .relationships import sections_contributors, sections_collectives


class Section(db.Model):
    """ Podcast sections """
    __tablename__ = "sections"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), default="Nom de la section")
    description = db.Column(db.Text)
    # Date of publication
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    # Place of recording/playing
    #location = db.Column(Geometry(geometry_type='POINT', srid=0))
    begin = db.Column(db.Time)
    # Beginning of the section in the podcast
    end = db.Column(db.Time)
    # Ending of the section in the podcast
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'))
    collectives = db.relationship(
        'Collective',
        secondary = 'sections_collectives',
        cascade='all',
        single_parent='True',
        lazy = 'select',
        back_populates = 'sections')
    contributors = db.relationship(
        'Contributor',
        secondary = 'sections_contributors',
        cascade='all',
        single_parent='True',
        lazy = 'select',
        back_populates = 'sections')
    podcast_id = db.Column(db.Integer, db.ForeignKey('podcasts.id'))
    tags = db.relationship(
        'Tag',
        backref=db.backref('sections', lazy='select'),
        lazy='select')
    mood = db.Column(db.String(128))


    def __repr__(self):
        return '<SECTION %r>' % self.name

    def __str__(self):
        return self.name

    @staticmethod
    def fake_feed(count=10):
        """ Randomly feeds the database """
        from sqlalchemy.exc import IntegrityError
        from random import seed, randint, choice
        import forgery_py

        seed()
        for i in range(count):
            s = Section(
                name=forgery_py.lorem_ipsum.title(),
                description=forgery_py.lorem_ipsum.paragraph())
            db.session.add(s)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
