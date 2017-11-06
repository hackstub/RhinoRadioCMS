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

ALLOWED_EXTENSIONS = set(['mp3', 'ogg'])

def allowed_file(filename):
    """
    Check that the file is allowed to be uplad (i.e. that the extension
    is allowed)
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route("/upload", methods=["GET", "POST"])
def upload():
    """
    Handle an incoming upload.
    """
    if request.method == "GET":
        return render_template("podcast_upload.html",
                                        styles = getStyles(),
                                        scripts = getScripts(),
                              )
    elif request.method == "POST":
        """Handle the upload of a file."""
        form = request.form

        # Create a unique "session ID" for this particular batch of uploads.
        upload_key = str(uuid4())

        # Is the upload using Ajax, or a direct POST by the form?
        is_ajax = False
        if form.get("__ajax", None) == "true":
            is_ajax = True

        # Target folder for these uploads.
        target = "{dir}/{key}".format(dir=UPLOAD_DIR, key=upload_key)
        try:
            os.mkdir(target)
        except:
            if is_ajax:
                return ajax_response(False, "Couldn't create upload directory: {}".format(target))
            else:
                return "Couldn't create upload directory: {}".format(target)

        print("=== Form Data ===")
        for key, value in form.items():
            print(key, "=>", value)

        if 'filzobe' not in request.files.keys():
            flash('No file part')
            print("No file given")
            print(request.url)
            return redirect(request.url)

        # check if the post request has the file par
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if not file or not allowed_file(file.filename):
            flash('Bad file or type ?')
            return redirect(request.url)

        filename = secure_filename(file.filename)
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        file.save(destination)

        if is_ajax:
            return ajax_response(True, upload_key)
        else:
            return redirect(url_for("main.index"))
    else:
        return "Wut?"

def ajax_response(status, msg):
    status_code = "ok" if status else "error"
    return json.dumps(dict(
        status=status_code,
        msg=msg,
    ))

def getPodcasts():
    foo = Podcast()
    foo.name = "foo"
    foo.link = "/podcast/foo"
    foo.src = "http://podcast.radiorhino.eu/Cr%c3%a9ations/2016-05-11%20-%20Grand%20test%20(Th%c3%a9o,%20J%c3%a9r%c3%a9mie).mp3"

    bar = Podcast()
    bar.name = "bar"
    bar.link = "/podcast/bar"
    bar.src = "http://podcast.radiorhino.eu/Cr%c3%a9ations/Images%20sonores%20d'%c3%89pinal/IMAGES_SONORES_EPINAL.mp3"

    podcasts = [ foo, bar ]
    return podcasts

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
