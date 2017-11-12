import os
from flask import (Flask,
                   render_template,
                   render_template_string,
                   url_for,
                   jsonify,
                   request,
                   redirect,
                   flash)
from werkzeug.utils import secure_filename
from functools import wraps
from glob import glob
from config import config
import json
from uuid import uuid4
from datetime import date

from . import main
from .forms import SubscribeForm
from .. import db
from app.models.admin import *
from app.models.podcast import Podcast

app = Flask(__name__)

from app.models.podcast import Podcast
from app.models.contributor import *
from app.models.blog import *
from app.models.event import *
from app.models.label import *
from app.models.tag import *
from app.models.section import *
from app.models.page import *



####################################
#  Wrapper for invidicual content  #
####################################

def content(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # We make sure to come from an 'already loaded site' ...
        # Otherwise, load the base then immediately load the requested
        # content
        if not request.referrer:
            return render_template( 'base.html',
                                    styles = getStyles(),
                                    scripts = getScripts(),
                                    content = request.path,
                                    podcasts = Podcast.list(),
                                    blogPosts = BlogPost.list(),
                                    events = Event.list()
                                  )
        data = f(*args, **kwargs)

        # Data should be a list [ ] with 2 elements :
        # - name of a js function
        # - data for the js function
        assert isinstance(data, list)
        assert len(data) == 2
        assert isinstance(data[0], str)
        assert isinstance(data[1], dict)

        response = jsonify(data)
        response.status_code = 200
        return response

    return decorated_function


#########################
#  Main pages           #
#########################

@main.route('/')
@content
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
@content
def about():

    page = Page.query.filter_by(title='À propos').first_or_404()

    return [ 'displayMain',
           { "content": render_template("about.html",
                                        page=page) } ]

@main.route('/blogs/')
@content
def blogs():
    return [ 'displayMain',
             { "content": render_template("notimplemented.html") } ]

@main.route('/agendas/')
@content
def agenda():
    return [ 'displayMain',
             { "content": render_template("notimplemented.html") } ]

@main.route('/contribute/')
@content
def contribute():
    return [ 'displayMain',
             { "content": render_template("notimplemented.html") } ]

#########################
#  Podcasts             #
#########################

@main.route('/podcasts/')
@content
def podcasts():
    podcasts = Podcast.list()
    return [ 'displayMain',
             { "content": render_template("notimplemented.html",
                                          podcasts=podcasts) } ]


@main.route('/podcast/<id>')
@content
def podcast(id):
    podcast = Podcast.query.filter_by(id = id).first()

    return [ "player.load.bind(player)",
             { "link" : podcast.link,
               "title" : podcast.title } ]


#########################
#  Contributors         #
#########################

@main.route('/contributors/')
@content
def contributors():
    """ Return list of all the contributors """
    contribs = Contributor.list()
    return [ 'displayMain',
             { "content": render_template("notimplemented.html",
                                          contributors=contribs) }]


@main.route('/contributor/<contrib>')
@content
def contributor(contrib):
    podcasts = Podcast.list(filter = contrib + "in Podcast.contributors")
    return [ 'displayMain',
             { "content": render_template("notimplemented.html",
                                          podcasts=podcasts) }]

#########################
#  Collectives          #
#########################

@main.route('/collectives')
@content
def collectives():
    """ Return list of all the collectives """
    collectives = Label.query.filter(Label.type=="COLLECTIVE").all_or_404()
    return [ 'displayMain',
             { "content": render_template("notimplemented.html",
                                          collectives=collectives) }]

@main.route('/collective/<coll>')
@content
def collective(coll):
    """ Return podcasts from collective coll """
    label_id = Label.query.filter(Label.name==coll).first()
    podcasts = getPodcasts(filter='Podcast.label_id=label_id'),
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
