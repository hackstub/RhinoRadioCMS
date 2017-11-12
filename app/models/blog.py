from .. import db

from datetime import datetime

class BlogPost(db.Model):
    """ Blog posts """
    __tablename__ = 'blog_posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    """ Title of the post """
    timestamp = db.Column(db.Date, default=datetime.utcnow)
    """ Date of creation """
    desc = db.Column(db.Text)
    """ Description """
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'))
    """ Channel """
    contributor_id = db.Column(db.Integer, db.ForeignKey('contributors.id'))
    """ Contributor """

    def list(filter='', order='', number=3):
        blogPosts = BlogPost.query.\
            filter(filter).\
            order_by(BlogPost.timestamp.desc()).\
            paginate(per_page=number).items
        return blogPosts

    @staticmethod
    def fake_feed(count=10):
        """ Randomly feeds the database """
        from sqlalchemy.exc import IntegrityError
        from random import seed, randint
        import forgery_py

        seed()
        for i in range(count):
            bp = BlogPost(
                title = forgery_py.lorem_ipsum.title(),
                desc = forgery_py.lorem_ipsum.paragraph(),
                channel_id = i+1,
                contributor_id = i+1
            )
            db.session.add(bp)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
