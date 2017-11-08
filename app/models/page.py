from .. import db

class Page(db.Model):
    """ Pages """
    __tablename__ = 'pages'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    desc = db.Column(db.Text)
    label_id = db.Column(db.Integer, db.ForeignKey('labels.id'))
    parent_page_id = db.relationship('Page')
    children = db.Column(db.Integer, db.ForeignKey('pages.id'))

    def __str__(self):
        return self.title

    @staticmethod
    def fake_feed(count=10):
        """ Randomly feeds the database """
        from sqlalchemy.exc import IntegrityError
        from random import seed, randint
        import forgery_py

        seed()
        about = Page(
            title = "À propos",
            desc = forgery_py.lorem_ipsum.paragraphs(quantity=10)
        )
        db.session.add(about)
        for i in range(count):
            p = Page(
                title = forgery_py.lorem_ipsum.title(),
                desc = forgery_py.lorem_ipsum.paragraphs(quantity=9),
                label_id = randint(0, 10),
            )
            db.session.add(p)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
