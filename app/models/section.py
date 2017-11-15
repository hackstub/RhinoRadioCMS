from datetime import datetime
from geoalchemy2 import Geometry

from .. import db
from .relationships import sections_authors


class Section(db.Model):
    """ Podcast sections """
    __tablename__ = "sections"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    """ Title of the section """
    desc = db.Column(db.Text)
    """ Description """
    contributors = db.relationship('Contributor',
                                    secondary = 'sections_authors',
                                    lazy = 'select',
                                    back_populates = 'sections')
    """ Contributor's ID """
    podcast_id = db.Column(db.Integer, db.ForeignKey('podcasts.id'))
    """ Podcast's ID """
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'))
    """ Channel's ID"""
    begin = db.Column(db.Time)
    """ Beginning of the section """
    end = db.Column(db.Time)
    """ Ending of the section """
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    """ Date and time of creatiomirrors security debiann """
    mood = db.Column(db.String(128))
    """ Mood of the section """
    tags = db.relationship('Tag',
                backref=db.backref('sections', lazy='select'),
                lazy='select')
    """ Tags of the section """
    #location = db.Column(Geometry(geometry_type='POINT', srid=0))
    #""" Place of recording/playing """

    def __repr__(self):
        return '<SECTION %r>' % self.title

    def __str__(self):
        return self.title

    @staticmethod
    def fake_feed(count=10):
        """ Randomly feeds the database """
        from sqlalchemy.exc import IntegrityError
        from random import seed, randint
        import forgery_py

        seed()
        for i in range(count):
            s = Section(
                title = forgery_py.lorem_ipsum.title(),
                desc = forgery_py.lorem_ipsum.paragraph()
                #contributors = randint(1,11)
            )
            db.session.add(s)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
