from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.form.upload import FileUploadInput
from flask_admin.contrib.geoa import ModelView
from geoalchemy2.types import Geometry
from wtforms import TextAreaField
from wtforms.widgets import TextArea
from .. import db, admin, base_path
import os.path as op

from .podcast import Podcast
from .contributor import *
from .blog import *
from .event import *
from .label import *
from .tag import *
from .section import *
from .page import *

#####################
#  Admin views      #
#####################

podcastPath = op.join(base_path, 'static/podcasts/')

# Admin views
# FIXME : add localization (http://flask-admin.readthedocs.io/en/latest/advanced/#localization-with-flask-babelex)"""

# FIXME : Inline file admin
'''
class FileAdminWidget(FileAdmin):
    def __call__(self, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' fileAdmin'
        else:
            kwargs.setdefault('class', 'fileAdmin')
        if not kwargs.get['path']:
            kwargs.setdefault('path', base_path)
        if not kwargs.get['url']:
            kwargs.setdefault('url', '/static/')
        if not kwargs.get('name'):
            kwargs.setdefault('name', 'setdefault')
        return super(FileAdmin, self).__call__(field, **kwargs)

class FileAdminField(FileAdminWidget):
    widget = FileAdminWidget(base_path=podcastPath, url='/static/podcasts/', name='Files')
'''

#############################
#  Custom generic views     #
#############################

class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()

class ModalView(ModelView):
    create_modal = True

class FullTextView(ModelView):
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'desc': CKTextAreaField
    }

#####################
#  Custom Views     #
#####################

class PodcastView(FullTextView):
    form_excluded_columns = ['timestamp']
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
        contributors='Auteurs',
        desc='Description',
        mood='Ambiance',
        link='Lien',
        sections = 'Extraits',
        place = 'Lieu',
        itinerary = 'Itinéraire'
        )
    form_args = {
        'type': {
            'default': False
        }
    }

    inline_models = (Tag, Section, )

class SectionView(FullTextView):
    form_excluded_columns = ['timestamp']

class EventView(ModalView):
    column_labels = dict(
        title = 'Titre',
        place = 'Lieu',
        begin = 'Début',
        end = 'Fin',
        desc = 'Description',
        label_id = 'Label'
    )

class ContributorView(ModalView):
    form_excluded_columns = ['podcasts']
    column_labels = dict(
        name = 'Nom',
        status = 'Statut',
    )

class LabelView(ModalView):
    form_excluded_columns = [
        'podcasts',
        'sections',
        'blogPosts',
        'pages',
        'events']

class BlogView(FullTextView):
    form_excluded_columns = ['timestamp']
    column_labels = dict(
        title = 'Titre',
        desc = 'Contenu',
        label_id = 'Label',
        contributor_id = 'Auteur'
    )

class PageAdminView(FullTextView):
    column_labels = dict(
        parent_page_id='Parent',
        title='Titre',
        desc='Contenu'
    )

admin.add_view(PodcastView(Podcast, db.session))
admin.add_view(FileAdmin(podcastPath, '/static/podcasts/', name='Anciens podcasts'))
admin.add_view(BlogView(BlogPost, db.session))
admin.add_view(ContributorView(Contributor, db.session))
admin.add_view(ModelView(Event, db.session))
admin.add_view(LabelView(Label, db.session))
admin.add_view(PageAdminView(Page, db.session))
