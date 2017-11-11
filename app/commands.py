import contextlib
from operator import itemgetter
from flask import url_for
from flask_script import Command
from . import db

from app.models.podcast import Podcast
from app.models.contributor import *
from app.models.blog import *
from app.models.event import *
from app.models.label import *
from app.models.tag import *
from app.models.section import *
from app.models.page import *


class RoutesCommand(Command):
    """List registered routes"""

    def __init__(self, app):
        self.app = app

    def run(self):
        from urllib.parse import unquote
        output = []
        for rule in self.app.url_map.iter_rules():

            options = {}
            for arg in rule.arguments:
                options[arg] = "[{0}]".format(arg)

            methods = ','.join(rule.methods)
            url = url_for(rule.endpoint, **options)
            line = unquote("{:35s} {:35s} {}"
                           .format(rule.endpoint, methods, url))
            output.append((line, url))

        # Sort output by url not name
        for (line, _) in sorted(output, key=itemgetter(1)):
            print(line)


class NukeCommand(Command):
    """Nuke the database (except the platform table)"""

    def __init__(self, db):
        self.db = db

    def run(self):
        self.db.drop_all()
        print("Tables dropped\n")
        self.db.create_all()
        print("Tables created\n")
        self.db.session.commit()
        print("Session committed\n")

class LoremCommand(Command):
    """Feed database with placeholders"""

    def __init__(self, db):
        self.db = db

    def run(self):
        for i in range(2):
            BlogPost.fake_feed()
            Contributor.fake_feed()
            Event.fake_feed()
            Label.fake_feed()
            Podcast.fake_feed()
            Section.fake_feed()
            Tag.fake_feed()
            Page.fake_feed()
