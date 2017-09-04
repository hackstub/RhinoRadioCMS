
import os
from flask import Flask, render_template, url_for, jsonify, request, redirect
from werkzeug.utils import secure_filename
from glob import glob
import json
app = Flask(__name__)



#########################
#  Main pages           #
#########################

@app.route('/')
def index(specificContent=None):
    return render_template( 'index.html',
                            styles = getStyles(),
                            scripts = getScripts(),
                            blog = getBlogItems(),
                            specificContent = specificContent
                          )

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



UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

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
    return [ ]
    # Please push the file :)
    #return  [ json.loads(open("content/blog/2017-08-06.json").read()) ]

#########################
#  Main                 #
#########################

if __name__ == '__main__':
    app.run()
