from .. import db
from datetime import datetime

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
    label_id = db.Column(db.Integer, db.ForeignKey('labels.id'))
    """ Label of the event """

    @staticmethod
    def fake_feed(count=10):
        """ Randomly feeds the database """
        from sqlalchemy.exc import IntegrityError
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
                label_id = i+1
            )
            db.session.add(e)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
