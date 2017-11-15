from .. import db
from datetime import datetime
from .podcast import Podcast
from .channel import Channel
from sqlalchemy.orm import validates
from sqlalchemy.exc import IntegrityError

class Event(db.Model):
    """ An agenda item """
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    """ Event's title """
    place = db.Column(db.String(128))
    """ Location """
    begin = db.Column(db.DateTime)
    """ Date of the event's beggining """
    end = db.Column(db.DateTime)
    """ Date of the event's ending """
    desc = db.Column(db.Text)
    """ Description of the event """
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'))
    """ Channel of the event """
    live_show = db.Column(db.Boolean())
    """ Live broadcast schedule ? """
    podcast_id = db.Column(db.Integer, db.ForeignKey('podcasts.id'))
    """ Podcast id (self-generated if live_show is true) """

    def __repr__(self):
        return '<EVENT %r>' % self.title

    def __str__(self):
        return self.title

    def __init__(self, **kwargs):
        if self.live_show == True:
            create_rel_podcast(self)
        super().__init__(**kwargs)

    @validates('channel_id')
    def validate_channel_id(self, key, channel_id):
        if self.live_show == True:
            if not self.channel_id:
                self.channel_id = "Émission"
                return self
            else:
                return self

    def list(filter='', order='', number=3):
        events = Event.query.filter(Event.begin >= datetime.today()) \
            .order_by(Event.begin.desc())                            \
            .paginate(per_page=number).items
        return events

    def create_rel_podcast(self):
        channel = Channel.query.filter_by(Channel.id == self.channel_id).first()
        podcast = Podcast(
            title = channel.title + 'du' + self.date.strftime("%d/%m/%y"),
            contributors = channel.contributors,
            desc = self.desc,
            channel_id = self.channel_id,
            mood = channel.mood,
            night = channel.night,
            date = self.begin)
        self.podcast_id = podcast.id
        db.session.add(podcast.id)
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
                title = forgery_py.lorem_ipsum.title(),
                place = forgery_py.address.street_address(),
                begin = forgery_py.date.date(),
                end = forgery_py.date.date(),
                desc = forgery_py.lorem_ipsum.paragraph(),
                channel_id = i+1
            )
            db.session.add(e)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
