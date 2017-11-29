# Rhino Radio CMS

Experimental webradio CMS based on Flask micro-framework designed for [Radio Rhino](http://radiorhino.eu) with YunoHost (not absolutely required but necessary to protect admin).

## Install

```bash
# On Debian/Ubuntu/Mint
sudo apt-get install python-virtualenv

virtualenv -p python3 venv
source venv/bin/activate

# PostgreSQL and GIS (geographic db) + SASS
sudo apt install python3-dev postgresql-9.4 postgresql-server-dev-9.4 postgis
gem install sass

pip3 install -r requirements.txt

# Start PostgreSQL
systemctl start postgresql

# if needed :
#createlang plpgsql gis

sudo su postgres
psql
>>> CREATE DATABASE rhino;
>>> \c rhino;
>>> CREATE EXTENSION postgis;
>>> GRANT ALL ON DATABASE rhino TO "user";
>>> \q

# Path a few stuff..
mkdir app/static/podcasts

# Replace 'xrange' by 'range' in lorem_ipsum :
vim venv/lib/python*/site-packages/forgery_py/forgery/lorem_ipsum.py

```

## Init the base

```
# (Re-)initialize database
python3 manage.py nuke

# Feed database with random placeholder values
python3 manage.py lorem
```

## Develop

```bash
# Run dev server
python3 manage.py runserver
```

## Admin

Admin interface on : http://domain.tld/admin

## Deployment with Gunicorn

```bash
# Install Gunicorn
pip3 install Gunicorn
```
More to come.

Uncomment '#scheme="https"' in views.py

Add environment variables to /lib/systemd/system :
AIRTIME_API_KEY
STREAM_URL
SECRET_KEY
FLASK_CONFIG='production'

If your podcast files are on a distant machine : set an autofs + sshfs on app/static/podcasts :
```bash
sshfs user@distant-ip:/podcasts/dir/
```

## Prod upgrade
```bash
git pull
git merge origin master
sass app/static/scss/style.scss:app/static/css/style.css --style compressed
service rhinosite restart
```


## Doc

Eeeeeeeh... Soon™.

```bash
# Install Sphinx
pip3 install Sphinx
```
