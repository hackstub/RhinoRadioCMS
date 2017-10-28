from flask_admin.contrib.sqla import ModelView
from .. import db, admin
from .podcast import Podcast
from .author import *
from .blog import *
from .event import *
from .meta import *
from .section import *

# Admin views
''' Fixme : add localization (http://flask-admin.readthedocs.io/en/latest/advanced/#localization-with-flask-babelex)'''

class PodcastView(ModelView):
    create_modal = True
    form_columns = ('title',
        'label',
        'authors',
        'desc',
        'mood',
        'type',
        'tags',
        'link'
        )
    form_choices = {
        'mood': [
            ('slow', 'Au pas'),
            ('medium', 'Au trot'),
            ('fast', 'Au galop !')
        ],
        'type': [
            (True, 'Oui'),
            (False, 'Non')
        ]
    }
    column_labels = dict(
        title='Titre',
        authors='Auteurs',
        type='Musical',
        desc='Description',
        mood='Ambiance',
        link='Lien'
        )
    form_args = {
        'type': {
            'validators': 'Required',
            'default': False
        }
    }

class SectionView(ModelView):
    create_modal = True
    columns_exclude = ['timestamp']

admin.add_view(PodcastView(Podcast, db.session))
admin.add_view(ModelView(BlogPost, db.session))
admin.add_view(ModelView(Author, db.session))
admin.add_view(ModelView(Event, db.session))
admin.add_view(ModelView(Label, db.session))
admin.add_view(SectionView(Section, db.session))
