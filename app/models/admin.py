from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.form.upload import FileUploadInput
from flask_admin.contrib.geoa import ModelView
from geoalchemy2.types import Geometry
from wtforms import TextAreaField
from wtforms.widgets import TextArea
from .. import db, admin, base_path
import os.path as op

from .podcast import Podcast
from .section import Section
from .contributor import Contributor
from .blog import BlogPost
from .event import Event
from .channel import Channel
from .tag import Tag
from .page import Page

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

class FullTextView(ModelView):
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'description': CKTextAreaField
    }

#####################
#  Custom Views     #
#####################
class ChannelView(FullTextView):
    form_excluded_columns = (
        'podcasts',
        'sections',
        'blog_posts',
        'events')
    column_labels = dict(
        name='Nom',
        description='Description',
        contributors='Auteurs',
        mood='Ambiance',
        music='Musique seulement ?',
        night='Nocturne ?'
        )

class ContributorView(ModelView):
    form_excluded_columns = ('podcasts')
    column_channels = dict(
        name='Nom',
        status='Statut'
    )

class PodcastView(FullTextView):
    form_excluded_columns = ('timestamp')
    form_choices = {
        'mood': [
            ('slow', 'Au pas'),
            ('medium', 'Au trot'),
            ('fast', 'Au galop !')
        ],
        'music': [
            (True, 'Oui'),
            (False, 'Non')
        ]
    }
    column_exclude_list = ('description')
    column_labels = dict(
        name='Titre',
        description='Description',
        date='Date d\'enregistrement',
        channel='Chaîne',
        contributors='Auteurs',
        sections='Extraits',
        link='Lien',
        mood='Ambiance',
        music='Musique seulement ?'
        )
    form_args = {
        'type': {
            'default': False
        }
    }

    inline_models = (Tag, Section, )

class SectionView(FullTextView):
    form_excluded_columns = ('timestamp', 'location')
    column_labels = dict(
        title='Titre',
        desc='Description',
        contributor_id='Auteur'
    )

class BlogView(FullTextView):
    form_excluded_columns = ('timestamp')
    column_channels = dict(
        name='Titre',
        description='Contenu',
        channel_id='Chaîne',
        contributors='Auteurs'
    )

class EventView(FullTextView):
    column_labels = dict(
        name='Titre',
        description='Description',
        place='Lieu',
        begin='Début',
        end='Fin',
        channel_id='Channel',
        live_show='Direct ?'
    )

class PageAdminView(FullTextView):
    column_channels = dict(
        name='Titre',
        description='Contenu'
    )

admin.add_view(PodcastView(Podcast, db.session))
admin.add_view(FileAdmin(podcastPath, '/static/podcasts/',
                         name='Anciens podcasts'))
admin.add_view(BlogView(BlogPost, db.session))
admin.add_view(ContributorView(Contributor, db.session))
admin.add_view(EventView(Event, db.session))
admin.add_view(ChannelView(Channel, db.session))
admin.add_view(PageAdminView(Page, db.session))
