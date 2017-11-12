from .. import db

from .channel import *
from .section import *

class Contributor(db.Model):
    __tablename__ = 'contributors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    status = db.Column(db.String(128))
    bio = db.Column(db.Text)
    email = db.Column(db.String(256))
    podcasts = db.relationship('Podcast',
                secondary = 'podcasts_authors',
                lazy = 'select',
                back_populates = 'contributors')
    sections = db.relationship('Section',
                secondary = 'sections_authors',
                lazy = 'select',
                back_populates = 'contributors')
    website = db.Column(db.String(256))
    channels = db.relationship('Channel',
                secondary = 'channels_authors',
                lazy = 'select',
                back_populates = 'contributors')

    def __str__(self):
        return self.name

    def list(filter='', order=''):
        """ List all contributors """
        contribs = Contributor.query.\
            filter(filter).\
            order_by(Contributor.name.desc(), order).\
            all()
        return contribs

    @staticmethod
    def fake_feed(count=10):
        """ Randomly feeds the database """
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            c = Contributor(
                name = forgery_py.name.full_name(),
                status = forgery_py.lorem_ipsum.word(),
                bio = forgery_py.lorem_ipsum.sentence(),
                email = forgery_py.internet.email_address(),
                website = forgery_py.internet.domain_name()
                )
            db.session.add(c)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
