class Podcast():
    __tablename__ = 'podcasts'
    id = dbColumn(db.Integer, primary_key=True)
    name = dbColumn(db.String(512), unique=True)
    author = dbColumn(db.String(256), index=True)
    date = dbColumn(db.Date)
    link = dbColumn(db.String(256))
    
    def name():
        return name
    
    def link():
        return link

class 