from datetime import datetime
from sqlalchemy.orm import validates

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
    # Podcast id (self-generated if live_show is true)
    podcast_id = db.Column(db.Integer, db.ForeignKey('podcasts.id'))
    # Live broadcast scheduled ?
    live_show = db.Column(db.Boolean())
    #FIXME ADD COLLECTIVE


    def __repr__(self):
        return '<EVENT %r>' % self.name

    def __str__(self):
        return self.name

    def __init__(self, **kwargs):
        if self.live_show == True:
            create_rel_podcast(self)
        super().__init__(**kwargs)

    # FIXME
    # @validates('channel_id')
    # def validate_channel_id(self, key, channel_id):
    #
    #     if self.live_show == True:
    #         if not self.channel_id:
    #             self.channel_id = "Émission"
    #             return self
    #         else:
    #             return self

    def list(filter='', order='', number=3):
        events = Event.query.filter(Event.begin >= datetime.today()) \
            .order_by(Event.begin.desc())                            \
            .paginate(per_page=number).items
        return events

    def create_rel_podcast(self):
        channel = Channel.query.filter_by(Channel.id == self.channel_id).first()
        podcast = Podcast(
            name=channel.name + 'du' + self.date.strftime("%d/%m/%y"),
            contributors=channel.contributors,
            description=self.description,
            channel_id=self.channel_id,
            mood=channel.mood,
            night=channel.night,
            date=self.begin)
        self.podcast_id = podcast.id
        db.session.add(podcast.id)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    @staticmethod
    def fake_feed(count=10):
        """ Randomly feeds the database """
        from sqlalchemy.exc import IntegrityError
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
