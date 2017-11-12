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
                            podcasts = Podcast.list(),
                            blogPosts = BlogPost.list(),
                            events = Event.list(),
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
    return Podcast.list()

@main.route('/podcasts/<id>')
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
    contribs = Contributor.list()
    return render_template( 'index.html',
                            styles = getStyles(),
                            scripts = getScripts(),
                            contribs = contribs
                          )

@main.route('/contributors/<contrib>')
def contributor(contrib):
    return Podcast.list(filter = contrib + "in Podcast.contributors")

#########################
#  Collectives          #
#########################

@main.route('/collectives')
def collectives():
    """ Return list of all the collectives """
    collectives = Label.query.filter(Label.type=="COLLECTIVE").all_or_404()
    return collectives

@main.route('/collectives/<coll>')
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
