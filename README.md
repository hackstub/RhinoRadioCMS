# Rhino Radio CMS

Experimental webradio CMS based on Flask micro-framework designed for [Radio Rhino](http://radiorhino.eu)

## Install

```bash
# On Debian/Ubuntu/Mint
sudo apt-get install python-virtualenv

virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt
# PostgreSQL and GIS (geographic db)
sudo apt install postgis
# PostgreSQL
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
```

## Develop

```bash
./run_dev_server.sh
# (Re-)initialize database
python3 manage.py nuke
# Feed database with random placeholder values
python3 manage.py lorem
```
## Admin

Admin interface on : http://domain.tld/admin

## Deployment with Gunicorn

```bash
# Install Gunicorn
pip3 install Gunicorn
```
More to come.

## Doc

Eeeeeeeh... Soon™.

```bash
# Install Sphinx
pip3 install Sphinx
```
