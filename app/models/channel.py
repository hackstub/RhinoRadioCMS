from .. import db
from .relationships import channels_contributors, channels_collectives


class Channel(db.Model):
    __tablename__ = "channels"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.Text)
    collectives = db.relationship(
        'Collective',
        secondary='channels_collectives',
        cascade='all, delete-orphan',
        single_parent='True',
        lazy='select',
        back_populates='channels')
    contributors = db.relationship(
        'Contributor',
        secondary='channels_contributors',
        cascade='all, delete-orphan',
        single_parent='True',
        lazy='select',
        back_populates='channels')
    podcasts = db.relationship(
        'Podcast',
        backref='channel',
        lazy='select')
    sections = db.relationship(
        'Section',
        backref='channel',
        lazy='select')
    blog_posts = db.relationship(
        'BlogPost',
        backref='channel',
        lazy='select')
    events = db.relationship(
        'Event',
        backref='',
        lazy='select')
    tags = db.relationship(
        'Tag',
        backref=db.backref('channel', lazy='select'),
        lazy='select')
    license = db.Column(db.String(256))
    mood = db.Column(db.String(128))
    # Musical or non-musical
    music = db.Column(db.Boolean())
    # is it a night show ?
    night = db.Column(db.Boolean())


    def __repr__(self):
        return '<CHANNEL %r>' % self.name

    def __str__(self):
        return self.name

    def list(type = ''):
        if not type == '':
            items = Channel.query             \
                .filter(Channel.type == type) \
                .order_by(Channel.name).all()
        else:
            items = Channel.query.order_by(Channel.name).all()
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
                description=forgery_py.lorem_ipsum.paragraph()
            )
            db.session.add(l)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
