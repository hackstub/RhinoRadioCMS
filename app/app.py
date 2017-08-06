from flask import Flask, render_template, url_for
import glob
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
     return [ url_for('static', filename=file, _external=True) for file in glob.glob("static/*/*.css") ]

def getScripts() :
     return [ url_for('static', filename=file, _external=True) for file in glob.glob("static/*/*.js") ]


app.run()
