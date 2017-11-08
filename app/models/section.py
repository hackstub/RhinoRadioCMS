from .. import db
from datetime import datetime

class Section(db.Model):
    """ Podcast sections """
    __tablename__ = "sections"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    """ Title of the section """
    desc = db.Column(db.Text)
    """ Description """
    contributor_id = db.Column(db.Integer, db.ForeignKey('contributors.id'))
    """ Contributor's ID """
    podcast_id = db.Column(db.Integer, db.ForeignKey('podcasts.id'))
    """ Podcast's ID """
    label_id = db.Column(db.Integer, db.ForeignKey('labels.id'))
    """ Label's ID"""
    begin = db.Column(db.Time)
    """ Beginning of the section """
    end = db.Column(db.Time)
    """ Ending of the section """
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    """ Date and time of creation """

    @staticmethod
    def fake_feed(count=10):
        """ Randomly feeds the database """
        from sqlalchemy.exc import IntegrityError
        from random import seed, randint
        import forgery_py

        seed()
        for i in range(count):
            s = Section(
                title = forgery_py.lorem_ipsum.title(),
                desc = forgery_py.lorem_ipsum.paragraph()
            )
            db.session.add(s)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
