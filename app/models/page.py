from .. import db

class Page(db.Model):
    """ Pages """
    __tablename__ = 'pages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    description = db.Column(db.Text)
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'))


    def __repr__(self):
        return '<PAGE %r>' % self.name

    def __str__(self):
        return self.name

    @staticmethod
    def fake_feed(count=10):
        """ Randomly feeds the database """
        from sqlalchemy.exc import IntegrityError
        from random import seed, randint
        import forgery_py

        seed()
        about = Page(
            name="À propos",
            id=1,
            description=forgery_py.lorem_ipsum.paragraphs(quantity=20)
        )
        contribute = Page(
            id=2,
            name='Contribuer',
            description=forgery_py.lorem_ipsum.paragraphs(quantity=10)
        )
        db.session.add(about)
        db.session.add(contribute)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
