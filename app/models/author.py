from .. import db

class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    status = db.Column(db.String(128))
    bio = db.Column(db.Text)
    podcasts = db.relationship('Podcast',
                secondary='publications')

    def __str__(self):
        return self.name
