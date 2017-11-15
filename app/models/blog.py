from datetime import datetime

from .. import db
from .relationships import blog_posts_contributors


class BlogPost(db.Model):
    """ Blog posts """
    __tablename__ = 'blog_posts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    description = db.Column(db.Text)
    # Date of creation
    timestamp = db.Column(db.Date, default=datetime.utcnow)
    channel_id = db.Column(db.Integer, db.ForeignKey('channels.id'))
    contributors = db.relationship(
        'Contributor',
        secondary='blog_posts_contributors',
        cascade='all, delete',
        lazy='select',
        back_populates='blog_posts')


    def __repr__(self):
        return '<BLOGPOST %r>' % self.name

    def __str__(self):
        return self.name

    def list(filter='', order='', number=3):
        from .channel import Channel

        blogPosts = BlogPost.query.filter(filter)                       \
            .join(Channel, Channel.id==BlogPost.channel_id)             \
            .order_by(BlogPost.timestamp.desc())                        \
            .paginate(per_page=number).items
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
                name=forgery_py.lorem_ipsum.title(),
                description=forgery_py.lorem_ipsum.paragraph(),
                channel_id=i+1,
            )
            db.session.add(bp)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
