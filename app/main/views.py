# "Standard libs" imports
import os
import json
from glob import glob
from config import config
from uuid import uuid4
from datetime import date

# Flask stuff
from flask import (Flask,
                   render_template,
                   url_for,
                   jsonify,
                   request,
                   redirect,
                   flash)
from werkzeug.utils import secure_filename

# Specific app stuff
from . import main
from .forms import SubscribeForm
from .partial_content import partial_content_decorator
from .. import db
from app.models.admin import *
from app.models.podcast import Podcast

app = Flask(__name__)

from app.models.podcast import Podcast
from app.models.contributor import *
from app.models.blog import *
from app.models.event import *
from app.models.channel import *
from app.models.tag import *
from app.models.section import *
from app.models.page import *


#########################
#  Main pages           #
#########################

def base():
    return render_template( 'base.html',
                            styles = getStyles(),
                            scripts = getScripts(),
                            podcasts = Podcast.list(),
                            blogPosts = BlogPost.list(),
                            events = Event.list(),
                            content = request.path
                          )

partial_content = partial_content_decorator(base)

@main.route('/')
@partial_content
def index():
    return [ 'displayMain',
           { "content": render_template("index.html",
                                        podcasts = Podcast.list(),
                                        blogPosts = BlogPost.list(),
                                        events = Event.list()) } ]


#########################
#  About                #
#########################

@main.route('/about')
@partial_content
def about():

    page = Page.query.filter_by(title='À propos').first_or_404()

    return [ 'displayMain',
           { "content": render_template("about.html",
                                        page=page) } ]

@main.route('/blogs/')
@partial_content
def blogs():
    return [ 'displayMain',
             { "content": render_template("notimplemented.html") } ]

@main.route('/agendas/')
@partial_content
def agenda():
    return [ 'displayMain',
             { "content": render_template("notimplemented.html") } ]

@main.route('/contribute/')
@partial_content
def contribute():
    return [ 'displayMain',
             { "content": render_template("notimplemented.html") } ]

#########################
#  Podcasts             #
#########################

@main.route('/podcasts/')
@partial_content
def podcasts():
    return [ 'displayMain',
             { "content": render_template("podcasts.html",
                                          podcasts = Podcast.list()) } ]


@main.route('/podcast/<id>')
@partial_content
def podcast(id):
    podcast = Podcast.query.filter_by(id = id).first()

    return [ "player.load.bind(player)",
             { "link" : podcast.link,
               "title" : podcast.title } ]


#########################
#  Contributors         #
#########################

@main.route('/contributors/')
@partial_content
def contributors():
    """ Return list of all the contributors """
    contribs = Contributor.list()
    return [ 'displayMain',
             { "content": render_template("notimplemented.html",
                                          contributors=contribs) }]


@main.route('/contributor/<contrib>')
@partial_content
def contributor(contrib):
    #podcasts = Podcast.list(filter = contrib + "in Podcast.contributors")
    #podcasts = Podcast.query.filter_by(contributor_id = Contributor.query.filter_by(name = contrib).first()).all()
    return [ 'displayMain',
             { "content": render_template("notimplemented.html") }]


#########################
#  Collectives          #
#########################

@main.route('/collectives')
@partial_content
def collectives():
    """ Return list of all the collectives """
    collectives = Channel.query.filter(Channel.type=="COLLECTIVE").all_or_404()
    return [ 'displayMain',
             { "content": render_template("notimplemented.html",
                                          collectives=collectives) }]

@main.route('/collective/<coll>')
@partial_content
def collective(coll):
    """ Return home template for collective coll """
    channel_id = Channel.query.filter(Channel.name==coll).first()
    podcasts = getPodcasts(filter='Podcast.channel_id=channel_id'),
    return [ 'displayMain',
             { "content": render_template("notimplemented.html",
                                          podcasts=podcasts) }]

#########################
#  Static stuff         #
#########################

def getStyles():
     return [ url_for('static',
                      filename=file.replace('app/static/', ''),
                      #_scheme='https',
                      _external=True)
             for file in glob("app/static/*/*.css") ]

def getScripts():
     return [ url_for('static',
                      filename=file.replace('app/static/', ''),
                      #_scheme='https',
                      _external=True)
             for file in   glob("app/static/lib/*.js")
                         + glob("app/static/js/*.js") ]
