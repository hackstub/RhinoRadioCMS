import os
from flask import Flask, render_template, url_for, jsonify, request, redirect, flash
from werkzeug.utils import secure_filename
from . import main
from .forms import SubscribeForm
from .. import db
from app.models.admin import *
from app.models.podcast import Podcast
from glob import glob
from config import config
import json
from uuid import uuid4
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
                            blog = getBlogItems(),
                            specificContent = specificContent
                          )

@main.route('/about')
def about():
    return render_template( 'about.html',
                            styles = getStyles(),
                            page = Page.query.filter_by(title='À propos').first(),
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

@main.route('/podcast/<name>')
def podcast(name):
    if not request.referrer:
        specificContent = { "function": "fetchAndPlayPodcast", "arg": request.url }
        return index(specificContent=specificContent)

    if name == "foo":
        src = "http://podcast.radiorhino.eu/Cr%c3%a9ations/2016-05-11%20-%20Grand%20test%20(Th%c3%a9o,%20J%c3%a9r%c3%a9mie).mp3"
    elif name == "bar":
        src = "http://podcast.radiorhino.eu/Cr%c3%a9ations/Images%20sonores%20d'%c3%89pinal/IMAGES_SONORES_EPINAL.mp3"
    else:
        src = "wat"

    data = { "src" : src,
             "title" : "so much "+name+" !" }

    response = jsonify(data)
    response.status_code = 200
    return response

#########################
#  Static stuff         #
#########################

def getStyles() :
     return [ url_for('static',
                      filename=file.replace('app/static/', ''),
                      _external=True)
             for file in glob("app/static/*/*.css") ]

def getScripts() :
     return [ url_for('static',
                      filename=file.replace('app/static/', ''),
                      _external=True)
             for file in   glob("app/static/lib/*.js")
                         + glob("app/static/js/*.js") ]

def getBlogItems() :
    return [ ]
