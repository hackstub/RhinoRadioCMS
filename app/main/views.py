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




def content(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.referrer:
            return base(content=request.path)
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
def base(content=None):
    return render_template( 'base.html',
                            styles = getStyles(),
                            scripts = getScripts(),
                            podcasts = getPodcasts(),
                            blog = getBlogPosts(),
                            events = getEvents(),
                            content = content
                          )


@main.route('/about')
@content
def about():

    return [ 'displayMain', { "content": render_template_string("about.html") } ]


@main.route('/maintenance', methods=['GET', 'POST'])
def maintenance():
    email = None
    form = SubscribeForm()
    if form.validate_on_submit():
        email=form.email.data
        form.name.data=''
    return render_template( 'maintenance.html',
                            styles = getStyles(),
                            form = form
                          )

#########################
#  Podcasts             #
#########################

@main.route('/podcasts/')
def podcasts():
    return "liste des podcasts"


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
def contributors():
    """ Return list of all the contributors """
    contributors = Contributor.query.order_by(name).all()
    return contributors

@main.route('/contributor/<contrib>')
def contributor(contrib):
    podcasts = Podcast.query.filter_by(contributor_id = Contributor.query.filter_by(name = contrib).first()).all()
    return podcasts

#########################
#  Collectives          #
#########################

@main.route('/collectives')
def collectives():
    """ Return list of all the collectives """
    collectives = Label.query.filter(Label.type=="COLLECTIVE").all_or_404()
    return collectives

@main.route('/collective/<coll>')
def collective(coll):
    """ Return home template for collective coll """
    label_id = Label.query.filter(Label.name==coll).first()
    return render_template( 'index.html',
                            styles = getStyles(),
                            scripts = getScripts(),
                            podcasts = getPodcasts(
                                filter='Podcast.label_id=label_id'),
                            blog = getBlogPosts(),
                            events = getEvents(),
                            specificContent = specificContent
                          )

#########################
#  Get elements         #
#########################

def getPodcasts(filter='', order="", number=10):
    podcasts = Podcast.query.\
        filter(filter).\
        order_by(Podcast.timestamp.desc(), order).\
        paginate(per_page=number).items
    return podcasts

def getBlogPosts():
    blogPosts = BlogPost.query.order_by(BlogPost.timestamp.desc()).all()
    return blogPosts

def getEvents():
    events = Event.query.order_by(Event.begin.desc()).all()
    return events

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

def getBlogPosts(filter='', order='', number=3):
    blogPosts = BlogPost.query.\
        filter(filter).\
        order_by(BlogPost.timestamp.desc()).\
        paginate(per_page=number).items
    return blogPosts

def getEvents():
    events = Event.query.filter(Event.begin >= date.today()).order_by(Event.begin.desc())
    return events
