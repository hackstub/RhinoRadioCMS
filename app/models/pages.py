from .. import db
from datetime import datetime

class Page(db.Model):
    __tablename__="pages"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    content = db.Column(db.Text)
