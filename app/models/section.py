from .. import db
from datetime import datetime

class Section(db.Model):
    __tablename__ = "sections"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    desc = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))
    podcast_id = db.Column(db.Integer, db.ForeignKey('podcasts.id'))
    label_id = db.Column(db.Integer, db.ForeignKey('labels.id'))
    begin = db.Column(db.Time)
    end = db.Column(db.Time)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
