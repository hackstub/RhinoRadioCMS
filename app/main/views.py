import os
from flask import Flask, render_template, url_for, jsonify, request, redirect, flash
from werkzeug.utils import secure_filename
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


#########################
#  Main pages           #
#########################

@main.route('/')
def index(specificContent=None):
    return render_template( 'index.html',
                            styles = getStyles(),
                            scripts = getScripts(),
                            podcasts = getPodcasts(),
                            blog = getBlogPosts(),
                            events = getEvents(),
                            specificContent = specificContent
                          )

@main.route('/about')
def about():
    return render_template( 'about.html',
                            styles = getStyles(),
                            page = Page.query.filter_by(title='À propos').first_or_404(),
                            scripts = getScripts(), )

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
def podcast(id):
    podcast = Podcast.query.filter_by(id = id).first()
    if not request.referrer:
        specificContent = { "function": "fetchAndPlayPodcast", "arg": podcast.link }
        return index(specificContent=specificContent)

    response.status_code = 200
    return response

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
#  Get elements         #
#########################

def getPodcasts(filter='', order="", number=10):
    podcasts = Podcast.query.\
        filter(filter).\
        order_by(Podcast.timestamp.desc(), order).\
        paginate(per_page=10).items
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
                      _external=True)
             for file in glob("app/static/*/*.css") ]

def getScripts():
     return [ url_for('static',
                      filename=file.replace('app/static/', ''),
                      _external=True)
             for file in   glob("app/static/lib/*.js")
                         + glob("app/static/js/*.js") ]

def getBlogPosts():
    blogPosts = BlogPost.query.order_by(BlogPost.timestamp.desc())
    return blogPosts

def getEvents():
    events = Event.query.filter(Event.begin >= date.today()).order_by(Event.begin.desc())
    return events
