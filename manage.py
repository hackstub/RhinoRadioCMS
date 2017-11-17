import os
from app import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app.commands import *

app = create_app(os.getenv('FLASK_CONFIG') or 'production')
manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('nuke', NukeCommand(db))
manager.add_command('lorem', LoremCommand(db))

if __name__ == '__main__':
    manager.run()
