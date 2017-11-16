from datetime import datetime
from sqlalchemy.orm import validates, reconstructor
from sqlalchemy.exc import IntegrityError
from .podcast import Podcast
from .channel import Channel

from .. import db


class Event(db.Model):
    """ An agenda item """
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    description = db.Column(db.Text)
    # Where the event will take place
    place = db.Column(db.String(128))
    # Date of the event's beggining
    begin = db.Column(db.DateTime)
    # Date of the event's ending
    end = db.Column(db.DateTime)
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'))
    collective_id = db.Column(db.Integer, db.ForeignKey('collectives.id'))
    # Podcast id (self-generated if live_show is true)
    podcast_id = db.Column(db.Integer, db.ForeignKey('podcasts.id'))
    # Live broadcast scheduled ?
    live_show = db.Column(db.Boolean())


    def __repr__(self):
        return '<EVENT %r>' % self.name

    def __str__(self):
        return self.name

    # FIXME dont know what happens here, but this breaks the fake_feed gen
    def __init__(self, **kwargs):
        super(Event, self).__init__(**kwargs)
        if self.live_show:
            self.create_rel_podcast()

    @validates('channel_id')
    def validate_channel_id(self, key, channel_id):
        if self.live_show == True:
            if not channel_id:
                channel_id = 1
                return channel_id
            else:
                return self

    def list(filter='', order='', number=3):
        events = Event.query.filter(Event.begin >= datetime.today()) \
            .order_by(Event.begin.desc())                            \
            .paginate(per_page=number).items
        return events

    @staticmethod
    def create_rel_podcast(self):
        channel = Channel.query.filter(Channel.id == self.channel_id).first()
        podcast = Podcast(
            name = channel.title + 'du' + self.date.strftime("%d/%m/%y"),
            contributors = channel.contributors,
            description = self.desc,
            channel_id = channel.id,
            mood = channel.mood,
            night = channel.night,
            live_show = True,
            date = self.begin)
        self.podcast_id = podcast.id
        db.session.add(podcast)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


    @staticmethod
    def closest_live():

        now = datetime.now()

        # Keep only lives that are not done yet
        lives = Event.query.filter(Event.live_show == True) \
                           .filter(Event.end > now) \
                           .all()

        found_live = None
        live_in = None
        for live in lives:

            # Get number of seconds until this event begin
            this_live_in = (live.begin - now).total_seconds()

            # If live is closest than the one already found, keep it
            if found_live is None or abs(live_in) > abs(this_live_in):
                found_live = live
                live_in = this_live_in

        return (found_live, live_in)


    @staticmethod
    def start_live(stream_url):

        live, live_in = Event.closest_live()

        # If live starts or started more than one hour from now, return 404
        if live is None or abs(live_in) > 3600:
            return ('NOTYET', 400)

        # Get the podcast
        podcast = Podcast.query.filter(Podcast.id==live.podcast_id).first()
        if podcast is None:
            return ('NOPODCAST', 404)

        # Set the link
        podcast.link = stream_url

        # Write it!
        try:
            db.session.commit()
            return ('OK', 200)
        except IntegrityError:
            db.session.rollback()
            return ('INTEGRITYERROR', 409)

    @staticmethod
    def fake_feed(count=10):
        """ Randomly feeds the database """
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            e = Event(
                name=forgery_py.lorem_ipsum.title(),
                place=forgery_py.address.street_address(),
                begin=forgery_py.date.date(),
                end=forgery_py.date.date(),
                description=forgery_py.lorem_ipsum.paragraph(),
                channel_id=i+1
            )
            db.session.add(e)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
