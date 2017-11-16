from .. import db

# Collectives's relationships
podcasts_collectives = db.Table('podcasts_collectives',
    db.Column(
        'podcast_id',
        db.Integer,
        db.ForeignKey('podcasts.id'),
        primary_key=True),
    db.Column(
        'collective_id',
        db.Integer,
        db.ForeignKey('collectives.id'),
        primary_key=True))

sections_collectives = db.Table('sections_collectives',
    db.Column(
        'section_id',
        db.Integer,
        db.ForeignKey('sections.id'),
        primary_key=True),
    db.Column(
        'collective_id',
        db.Integer,
        db.ForeignKey('collectives.id'),
        primary_key=True))

channels_collectives = db.Table('channels_collectives',
    db.Column(
        'channel_id',
        db.Integer,
        db.ForeignKey('channels.id'),
        primary_key=True),
    db.Column(
        'collective_id',
        db.Integer,
        db.ForeignKey('collectives.id'),
        primary_key=True))

blog_posts_collectives = db.Table('blog_posts_collectives',
    db.Column(
        'blog_post_id',
        db.Integer,
        db.ForeignKey('blog_posts.id'),
        primary_key=True),
    db.Column(
        'collective_id',
        db.Integer,
        db.ForeignKey('collectives.id'),
        primary_key=True))

# Contributors/Collectives relation
collectives_contributors = db.Table('collectives_contributors',
    db.Column('collective_id',
        db.Integer,
        db.ForeignKey('collectives.id'),
        primary_key=True),
    db.Column('contributor_id',
        db.Integer,
        db.ForeignKey('contributors.id'),
        primary_key=True))

# Contributors's relationships
podcasts_contributors = db.Table('podcasts_contributors',
    db.Column(
        'podcast_id',
        db.Integer,
        db.ForeignKey('podcasts.id'),
        primary_key=True),
    db.Column(
        'contributor_id',
        db.Integer,
        db.ForeignKey('contributors.id'),
        primary_key=True))

sections_contributors = db.Table('sections_contributors',
    db.Column(
        'section_id',
        db.Integer,
        db.ForeignKey('sections.id'),
        primary_key=True),
    db.Column(
        'contributor_id',
        db.Integer,
        db.ForeignKey('contributors.id'),
        primary_key=True))

channels_contributors = db.Table('channels_contributors',
    db.Column(
        'channel_id',
        db.Integer,
        db.ForeignKey('channels.id'),
        primary_key=True),
    db.Column(
        'contributor_id',
        db.Integer,
        db.ForeignKey('contributors.id'),
        primary_key=True))

blog_posts_contributors = db.Table('blog_posts_contributors',
    db.Column(
        'blog_post_id',
        db.Integer,
        db.ForeignKey('blog_posts.id'),
        primary_key=True),
    db.Column(
        'contributor_id',
        db.Integer,
        db.ForeignKey('contributors.id'),
        primary_key=True))
