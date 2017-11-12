from .. import db

class Contributor(db.Model):
    __tablename__ = 'contributors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    status = db.Column(db.String(128))
    bio = db.Column(db.Text)
    email = db.Column(db.String(256))
    podcasts = db.relationship('Podcast',
                secondary = 'publications')
    sections = db.relationship('Section',
                backref = db.backref('contributor', lazy='select'),
                lazy = 'select')

    def __str__(self):
        return self.name

    def list(filter='', order=''):
        """ List all contributors """
        contribs = Contributor.query.\
            filter(filter).\
            order_by(Contributor.name.desc(), order).\
            all()
        return contribs

    @staticmethod
    def fake_feed(count=10):
        """ Randomly feeds the database """
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            c = Contributor(
                name = forgery_py.name.full_name(),
                status = forgery_py.lorem_ipsum.word(),
                bio = forgery_py.lorem_ipsum.sentence(),
                email = forgery_py.internet.email_address())
            db.session.add(c)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
