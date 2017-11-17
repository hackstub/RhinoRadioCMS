command = "/home/rhino/RhinoRadioCMS/venv/bin/gunicorn"
pythonpath = '/home/rhino/RhinoRadioCMS'

user = 'rhino'
workers = 2
timeout = 30

bind = 'unix:/home/rhino/RhinoRadioCMS/sock'
pid = "/run/gunicorn/rhinosite-pid"

backlog = 2048
errorlog = "/var/log/rhinosite/error.log"
accesslog = "/var/log/rhinosite/acces.log"
access_log_format = '%({X-Real-IP}i)s %({X-Forwarded-For}i)s %(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
loglevel = 'warning'
capture_output = True

limit_request_line = 2048
limit_request_fields = 50
limit_request_field_size = 4096
