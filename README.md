# Sandbox Rhino Player

Experimentation to have a persistent player across pages

## Install

```bash
# On Debian/Ubuntu/Mint
sudo apt-get install python-virtualenv

virtualenv -p python3 venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## Develop

```bash
./run_dev_server.sh

# To initialize DB :
python3 manage.py shell
from app import db
from app.models import *

# To create tables :
db.create_all()

# To drop tables :
db.drop_all()

# To add an object :
db.session.add(object)

# To commit changes :
db.session.commit()
```



## Deploy

Instructions coming soon :)
