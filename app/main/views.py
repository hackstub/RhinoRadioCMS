from flask import Flask, render_template, url_for, jsonify, request
from . import main
from glob import glob
from config import config
import json
app = Flask(__name__)

#########################
#  Main pages           #
#########################

@main.route('/')
def index(specificContent=None):
    return render_template( 'index.html',
                            styles = getStyles(),
                            scripts = getScripts(),
                            blog = getBlogItems(),
                            specificContent = specificContent
                          )

@main.route('/about')
def about():
    return 'À propos de Radio Rhino'

@main.route('/maintenance')
def maintenance():
    return render_template( 'maintenance.html',
                            styles = getStyles(),
                          )

#########################
#  Podcasts             #
#########################

@main.route('/podcasts/')
def podcasts():
    return 'A list of podcasts'

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
    #return  [ json.loads(open("content/blog/2017-08-06.json").read()) ]

# Moved to manage.py
#if __name__ == '__main__':
#    app.run()
