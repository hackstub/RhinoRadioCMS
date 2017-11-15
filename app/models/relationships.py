from .. import db


podcasts_authors = db.Table('podcasts_authors',
    db.Column('podcast_id',
        db.Integer,
        db.ForeignKey('podcasts.id'),
        primary_key=True),
    db.Column('contributor_id',
        db.Integer,
        db.ForeignKey('contributors.id'),
        primary_key=True))

sections_authors = db.Table('sections_authors',
    db.Column('section_id',
        db.Integer,
        db.ForeignKey('sections.id'),
        primary_key=True),
    db.Column('contributor_id',
        db.Integer,
        db.ForeignKey('contributors.id'),
        primary_key=True))

channels_authors = db.Table('channels_authors',
    db.Column('channel_id',
        db.Integer,
        db.ForeignKey('channels.id'),
        primary_key=True),
    db.Column('contributor_id',
        db.Integer,
        db.ForeignKey('contributors.id'),
        primary_key=True))

blog_posts_authors = db.Table('blog_posts_authors',
    db.Column('blog_post_id',
        db.Integer,
        db.ForeignKey('blog_posts.id'),
        primary_key=True),
    db.Column('contributor_id',
        db.Integer,
        db.ForeignKey('contributors.id'),
        primary_key=True))
