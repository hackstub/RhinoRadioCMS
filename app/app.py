from flask import Flask, render_template, url_for, jsonify
from glob import glob
app = Flask(__name__)

#########################
#  Main pages           #
#########################

@app.route('/')
def index():
    return render_template( 'index.html',
                            styles = getStyles(),
                            scripts = getScripts() )

@app.route('/about')
def about():
    return 'À propos de Radio Rhino'

#########################
#  Podcasts             #
#########################

@app.route('/podcasts/')
def podcasts():
    return 'A list of podcasts'

@app.route('/podcast/<name>')
def podcast(name):

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
                      filename=file.replace('static/', ''),
                      _external=True)
             for file in glob("static/*/*.css") ]

def getScripts() :
     return [ url_for('static',
                      filename=file.replace('static/', ''),
                      _external=True)
             for file in   glob("static/lib/*.js")
                         + glob("static/js/*.js") ]


app.run()
