from .. import db

class Tag(db.Model):
    """ Tags of the podcasts """
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    """ Name of the tag """
    podcast_id = db.Column(db.Integer, db.ForeignKey('podcasts.id'))
    """ Podcast """
    section_id = db.Column(db.Integer, db.ForeignKey('sections.id'))
    """ Section """
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'))

    @staticmethod
    def fake_feed(count=10):
        """ Randomly feeds the database """
        from sqlalchemy.exc import IntegrityError
        from random import seed, randint
        import forgery_py

        seed()
        for i in range(count):
            t = Tag(
                name = forgery_py.lorem_ipsum.word(),
                podcast_id = randint(0,100)
            )
            db.session.add(t)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
