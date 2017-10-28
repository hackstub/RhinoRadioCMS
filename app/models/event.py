from .. import db
from datetime import datetime

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    place = db.Column(db.String(128))
    begin = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    desc = db.Column(db.Text)
