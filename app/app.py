from flask import Flask, render_template, url_for
from glob import glob
app = Flask(__name__)

@app.route('/')
def index():
    return render_template( 'index.html',
                            styles = getStyles(),
                            scripts = getScripts() )

@app.route('/podcasts/')
def podcasts():
    return 'A list of podcasts'

@app.route('/about')
def about():
    return 'À propos de Radio Rhino'

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
