from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.form.upload import FileUploadInput
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

class PageView(ModelView):
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'desc': CKTextAreaField
    }


class PodcastView(PageView):
    form_columns = ('title',
        'label',
        'contributors',
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
#        'type': [
#            (True, 'Oui'),
#            (False, 'Non')
#        ]
    }
    column_labels = dict(
        title='Titre',
        contributors='Auteurs',
        type='Musical',
        desc='Description',
        mood='Ambiance',
        link='Lien'
        )
    form_args = {
        'type': {
            'default': False
        }
    }

    inline_models = (Tag, Section, )

class SectionView(PageView):
    form_excluded_columns = ['timestamp']

class ContributorView(ModalView):
    form_excluded_columns = ['podcasts']

class LabelView(ModalView):
    form_excluded_columns = ['podcasts', 'sections']

class BlogView(PageView):
    form_excluded_columns = ['timestamp']

admin.add_view(PodcastView(Podcast, db.session))
admin.add_view(FileAdmin(podcastPath, '/static/podcasts/', name='Anciens podcasts'))
admin.add_view(BlogView(BlogPost, db.session))
admin.add_view(ContributorView(Contributor, db.session))
admin.add_view(ModelView(Event, db.session))
admin.add_view(LabelView(Label, db.session))
admin.add_view(PageView(Page, db.session))
