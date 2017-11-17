""" REWORK THIS SHIT => MERGE IT WITH CONTRIBUTOR
self-referential stuff"""

from .. import db
from .relationships import *


class Collective(db.Model):
    __tablename__ = 'collectives'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.Text)
    email = db.Column(db.String(256))
    website = db.Column(db.String(256))

    channels = db.relationship(
        'Channel',
        secondary='channels_collectives',
        cascade='all, delete-orphan',
        single_parent='True',
        lazy='select',
        back_populates='collectives')
    contributors = db.relationship(
        'Contributor',
        secondary = 'collectives_contributors',
        cascade='all, delete-orphan',
        single_parent='True',
        lazy = 'select',
        back_populates = 'collectives')
    podcasts = db.relationship(
        'Podcast',
        secondary='podcasts_collectives',
        cascade='all, delete-orphan',
        single_parent='True',
        lazy='select',
        back_populates='collectives')
    sections = db.relationship(
        'Section',
        secondary='sections_collectives',
        cascade='all, delete-orphan',
        single_parent='True',
        lazy='select',
        back_populates='collectives')
    blog_posts = db.relationship(
        'BlogPost',
        secondary='blog_posts_collectives',
        cascade='all, delete-orphan',
        single_parent='True',
        lazy='select',
        back_populates='collectives')


    def __repr__(self):
        return '<COLLECTIVE %r>' % self.name

    def __str__(self):
        return self.name

    def list(filter='', order=''):
        """ List all collectives """
        collect = Collective.query                          \
            .filter(filter)                                 \
            .order_by(Collective.name.desc(), order)        \
            .all()
        return collect

    @staticmethod
    def fake_feed(count=10):
        """ Randomly feeds the database """
        from sqlalchemy.exc import IntegrityError
        from random import seed, choice
        import forgery_py

        seed()
        col = ['ZBEUL', 'YOLO', 'ZDEDEDEX']
        for i in range(3):
            c = Collective(
                name=col[i],
                description= forgery_py.lorem_ipsum.sentence(),
                email=forgery_py.internet.email_address(),
                website=forgery_py.internet.domain_name()
                )
            db.session.add(c)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
