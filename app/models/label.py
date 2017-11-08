from .. import db

class Label(db.Model):
    """ Collectives and broadcasts """
    __tablename__ = "labels"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    desc = db.Column(db.Text)
    #label_id = db.relationship('Label', backref='label', lazy=True)
    podcasts = db.relationship('Podcast', backref='label', lazy=True)
    sections = db.relationship('Section', backref='label', lazy=True)
    blogPosts = db.relationship('BlogPost', backref ='label', lazy=True)

    def __str__(self):
        return self.name

    @staticmethod
    def fake_feed(count=10):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            l = Label(
                name = forgery_py.lorem_ipsum.title(),
                desc = forgery_py.lorem_ipsum.paragraph()
            )
            db.session.add(l)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
