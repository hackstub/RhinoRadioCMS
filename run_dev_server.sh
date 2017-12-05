source venv/bin/activate
export FLASK_APP=app.py
export FLASK_DEBUG=1

sass app/static/scss/style.scss:app/static/css/style.css --style compressed
python3 manage.py runserver
