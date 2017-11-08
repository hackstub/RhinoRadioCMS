from .. import db
import enum

class LabelType(enum.Enum):
    COLLECTIVE = "Collectif"
    SHOW = "Émission"

class Label(db.Model):
    """ Collectives and broadcasts """
    __tablename__ = "labels"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    desc = db.Column(db.Text)
    podcasts = db.relationship('Podcast', backref='label', lazy=True)
    sections = db.relationship('Section', backref='label', lazy=True)
    blogPosts = db.relationship('BlogPost', backref ='label', lazy=True)
    pages = db.relationship('Page', backref='label', lazy=True)
    events = db.relationship('Event', backref='label', lazy=True)
    parent_label_id = db.relationship('Label')
    children = db.Column(db.Integer, db.ForeignKey('labels.id'))
    type = db.Column(db.Enum(LabelType))

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
