import contextlib
from operator import itemgetter
from flask import url_for
from flask_script import Command
from . import db

from app.models.podcast import Podcast
from app.models.collective import Collective
from app.models.section import Section
from app.models.contributor import Contributor
from app.models.blog import BlogPost
from app.models.event import Event
from app.models.channel import Channel
from app.models.tag import Tag
from app.models.page import Page


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

    def a_tester_pour_niquer_les_cascades(self):
        from sqlalchemy.engine import reflection
        from sqlalchemy import create_engine
        from sqlalchemy.schema import (
            MetaData,
            Table,
            DropTable,
            ForeignKeyConstraint,
            DropConstraint,
            )
        # From http://www.sqlalchemy.org/trac/wiki/UsageRecipes/DropEverything

        conn=db.engine.connect()

        # the transaction only applies if the DB supports
        # transactional DDL, i.e. Postgresql, MS SQL Server
        trans = conn.begin()

        inspector = reflection.Inspector.from_engine(db.engine)

        # gather all data first before dropping anything.
        # some DBs lock after things have been dropped in
        # a transaction.
        metadata = MetaData()

        tbs = []
        all_fks = []

        for table_name in inspector.get_table_names():
            fks = []
            for fk in inspector.get_foreign_keys(table_name):
                if not fk['name']:
                    continue
                fks.append(
                    ForeignKeyConstraint((),(),name=fk['name'])
                    )
            t = Table(table_name,metadata,*fks)
            tbs.append(t)
            all_fks.extend(fks)

        for fkc in all_fks:
            conn.execute(DropConstraint(fkc))

        for table in tbs:
            conn.execute(DropTable(table))

        trans.commit()

class LoremCommand(Command):
    """Feed database with placeholders"""

    def __init__(self, db):
        self.db = db

    def run(self):
        for i in range(2):
            BlogPost.fake_feed()
            Contributor.fake_feed()
            Collective.fake_feed()
            Event.fake_feed()
            Channel.fake_feed()
            Podcast.fake_feed()
            Section.fake_feed()
            Tag.fake_feed()
            Page.fake_feed()
