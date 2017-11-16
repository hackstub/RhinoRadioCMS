# "Standard libs" imports
import os
import json
from glob import glob
from config import config, LIQUIDSOAP_TOKEN
from uuid import uuid4                 # FIXME no longer needed i think
from datetime import date              # same

# Flask stuff
from flask import (Flask,
                   render_template,
                   url_for,
                   jsonify,
                   request,
                   redirect,
                   flash)

# Specific app stuff
from . import main
from .forms import SubscribeForm
from .partial_content import (partial_content_decorator,
                              partial_content_no_history_decorator)
from .jinja_custom_filters import *
from .. import db                      # FIXME no longer needed i think
from app.models.admin import *
from app.models.event import Event
from app.models.podcast import Podcast
from app.models.section import Section
from app.models.contributor import Contributor
from app.models.blog import BlogPost
from app.models.event import Event
from app.models.channel import Channel
from app.models.tag import Tag
from app.models.page import Page

app = Flask(__name__)


#########################
#  Main pages           #
#########################

def base():
    return render_template( 'base.html',
                            styles = getStyles(),
                            scripts = getScripts(),
                            podcasts = Podcast.list(),
                            blog_posts = BlogPost.list(),
                            events = Event.list(),
                            content = request.path
                          )

partial_content = partial_content_decorator(base)
partial_content_no_history = partial_content_no_history_decorator(base)

@main.route('/')
@partial_content
def index():
    return [ 'displayMain',
           { "content": render_template("index.html",
                                        podcasts = Podcast.list(),
                                        blog_posts = BlogPost.list(),
                                        events = Event.list()) } ]


#########################
#  Pages                #
#########################

@main.route('/about')
@partial_content
def about():
    page = Page.query.filter_by(name='À propos').first_or_404()
    return [ 'displayMain',
           { "content": render_template("main_pages/about.html",
                                        page=page) } ]

@main.route('/contrib')
@partial_content
def contribute():
    # create a real "contribute" page
    page = Page.query.filter_by(name='Contribuer').first_or_404()
    return [ 'displayMain',
             { "content": render_template("main_pages/contribute.html",
                                          page=page) } ]

#########################
#  Podcasts             #
#########################

@main.route('/podcasts')
@partial_content
def podcasts():
    page = request.args.get('page', 1, type=int)
    pagination = Podcast.query                         \
        .join(Channel, Channel.id==Podcast.channel_id) \
        .order_by(Podcast.timestamp.desc())            \
        .paginate(page, per_page=10, error_out=False)
    podcasts = pagination.items

    return [ 'displayMain',
             { "content": render_template("main_pages/podcasts.html",
                                          podcasts=podcasts,
                                          pagination=pagination) } ]

@main.route('/podcasts/<id>')
@partial_content
def podcast(id):
    podcast = Podcast.query.filter_by(id = id).first()
    return [ 'displayMain',
             { "content": render_template("elem.html",
                                          elem=podcast) }]

@main.route('/podcasts/<id>/play')
@partial_content_no_history
def podcast(id):
    podcast = Podcast.query.filter_by(id = id).first()
    return [ "player.load.bind(player)",
             { "link" : podcast.link,
               "title" : podcast.title } ]

#########################
#  Contributors         #
#########################

@main.route('/contributors')
@partial_content
def contributors():
    #collectives = Channel.query.filter(Channel.type=="collective").all()
    return [ 'displayMain',
             { "content": render_template("main_pages/contributors.html",
                                          contributors=Contributor.list())}]


# @main.route('/contributors/<id>')
# @partial_content
# def contributor(id):
#     return [ 'displayMain',
#              { "content": render_template("notimplemented.html") }]

#########################
#  Collectives          #
#########################

@main.route('/collectives/')
@partial_content
def collectives():
    return [ 'displayMain',
             { "content": render_template("notimplemented.html") }]

@main.route('/collectives/<id>')
@partial_content
def collective(id):
    return [ 'displayMain',
             { "content": render_template("notimplemented.html") }]

#########################
#  Blogs                #
#########################

@main.route('/blogs')
@partial_content
def blogs():
    return [ 'displayMain',
             { "content": render_template("main_pages/blogs.html",
                                          blog_posts = BlogPost.list(number=10) )} ]

@main.route('/blogs/<id>')
@partial_content
def blog(id):
    return [ 'displayMain',
             { "content": render_template("notimplemented.html") }]

#########################
#  Agendas              #
#########################

@main.route('/agendas')
@partial_content
def agendas():
    return [ 'displayMain',
             { "content": render_template("main_pages/agendas.html",
                                          events = Event.list(number=10)) } ]

@main.route('/agendas/<id>')
@partial_content
def agenda(id):
    return [ 'displayMain',
             { "content": render_template("notimplemented.html") }]

#########################
#  Static stuff         #
#########################

@main.route('/on_air', methods=['POST'])
def on_air():

    # Check we're authorized to do this
    # Security Nazi : a simple string comparison is probably not secure against
    # time attack, but that's good enough ;)
    # FIXME : use real token in prod
    #if request.args.get('token') != LIQUIDSOAP_TOKEN:
    print(request.form["token"])
    if request.form['token'] != 'lol':
        return ('INVALIDTOKEN', 401) # Unauthorized

    stream_url = request.args.get('stream')
    return Event.start_live(stream_url)


@main.route('/next_live')
def next_live():

    live, next_live_in = Event.closest_live()

    return jsonify({ "next_live_in": next_live_in })


#########################
#  Static stuff         #
#########################

def getStyles():
     return [ url_for('static',
                      filename=file.replace('app/static/', ''),
                      #_scheme='https',
                      _external=True)
             for file in glob("app/static/css/*.css") ]

def getScripts():
     return [ url_for('static',
                      filename=file.replace('app/static/', ''),
                      #_scheme='https',
                      _external=True)
             for file in glob("app/static/js/*.js") ]
