from flask import Flask, render_template, url_for, jsonify
from glob import glob
import json
app = Flask(__name__)

#########################
#  Main pages           #
#########################

@app.route('/')
def index():
    return render_template( 'index.html',
                            styles = getStyles(),
                            scripts = getScripts(),
                            blog = getBlogItems() )

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
    data = { "src" : name+".mp3",
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

def getBlogItems() :
    return  [ json.loads(open("content/blog/2017-08-06.json").read()) ]

app.run()
