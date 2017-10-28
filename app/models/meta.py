from .. import db

class Label(db.Model):
    __tablename__ = "labels"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    desc = db.Column(db.Text)
    podcasts = db.relationship('Podcast', backref='label', lazy=True)
    sections = db.relationship('Section', backref='label', lazy=True)

    def __str__(self):
        return self.name

class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
