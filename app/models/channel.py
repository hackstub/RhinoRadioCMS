from .. import db
from .contributor import *

channels_authors = db.Table('channels_authors',
    db.Column('channel_id',
        db.Integer,
        db.ForeignKey('channels.id'),
        primary_key=True),
    db.Column('contributor_id',
        db.Integer,
        db.ForeignKey('contributors.id'),
        primary_key=True))

class Channel(db.Model):
    __tablename__ = "channels"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    """ Name of the channel """
    desc = db.Column(db.Text)
    """ Description of the channel """
    podcasts = db.relationship('Podcast', backref='channel', lazy=True)
    """ Podcasts of the channel """
    blogPosts = db.relationship('BlogPost', backref ='channel', lazy=True)
    """ Blog posts of the channel """
    pages = db.relationship('Page', backref='', lazy=True)
    """ Pages of the channel """
    events = db.relationship('Event', backref='', lazy=True)
    """ Events of the channel """
    contributors = db.relationship('Contributor',
                                    secondary = 'channels_authors',
                                    lazy = 'select',
                                    back_populates = 'channels')
    """ Contributors of the channel """
    mood = db.Column(db.String(128))
    """ Mood of the podcast """
    music = db.Column(db.Boolean())
    """ Musical or non-musical """
    tags = db.relationship('Tag',
                backref=db.backref('channel', lazy='select'),
                lazy='select')
    """ Tags of the podcasts """
    night = db.Column(db.Boolean())
    """ Night show ? """
    license = db.Column(db.String(256))
    """ License of the show """
    # type of the channel (collective or channel (maybe later documentary, ...))
    type = db.Column(db.String(256))

    def __repr__(self):
        return '<CHANNEL %r>' % self.name

    def __str__(self):
        return self.name

    def list(type = ''):
        if not type == '':
            items = Channel.query.\
                filter(Channel.type == type).\
                order_by(Channel.name).all()
        else:
            items = Channel.query.\
                order_by(Channel.name).all()
        return items

    @staticmethod
    def init():
        """ Adds generic Channel """
        from sqlalchemy.exc import IntegrityError
        c = Channel(name = "Émission")
        db.session.add(c)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.callback()

    @staticmethod
    def fake_feed(count=10):
        from sqlalchemy.exc import IntegrityError
        from random import seed, choice
        import forgery_py

        seed()
        for i in range(count):
            l = Channel(
                name=forgery_py.lorem_ipsum.title(),
                desc=forgery_py.lorem_ipsum.paragraph(),
                type=choice(["collective", "channel"])
            )
            db.session.add(l)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
