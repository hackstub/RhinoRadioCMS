# Sandbox Rhino Player

Experimentation to have a persistent player across pages

## Install

```bash
# On Debian/Ubuntu/Mint
sudo apt-get install python-virtualenv

virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt
# PostgreSQL
systemctl start postgresql
# GIS (geographic db)
sudo apt install postgis
# if needed :
#createlang plpgsql gis
sudo su postgres
psql
>>> CREATE DATABASE rhino;
>>> \c rhino;
>>> CREATE EXTENSION postgis;
>>> GRANT ALL ON DATABASE rhino TO "user";
#>>> GRANT ALL ON spatial_ref_sys TO "user";
#>>> GRANT ALL ON geometry_columns TO "user";
>>> \q
```

## Develop

```bash
./run_dev_server.sh

## Database Cheatsheet

# Migrating database after modifications
python3 manage.py db migrate
python3 manage.py db upgrade

# To commit changes :
db.session.commit()
```
## Admin

Admin interface on : http://domain.tld/admin

## Deployment with Gunicorn

```bash
# Install Gunicorn
pip3 install Gunicorn
```
## Doc

Eeeeeeeh... Soon™.

```bash
# Install Sphinx
pip3 install Sphinx
```
