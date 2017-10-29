from .. import db

from datetime import datetime

class BlogPost(db.Model):
    __tablename__ = 'blog_posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    date = db.Column(db.Date, default=datetime.utcnow)
    content = db.Column(db.Text)
    label_id = db.Column(db.Integer, db.ForeignKey('labels.id'))
