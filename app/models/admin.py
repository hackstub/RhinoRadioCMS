from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from wtforms import TextAreaField
from wtforms.widgets import TextArea
from .. import db, admin, path
from .podcast import Podcast
from .author import *
from .blog import *
from .event import *
from .meta import *
from .section import *


# Admin views
''' Fixme : add localization (http://flask-admin.readthedocs.io/en/latest/advanced/#localization-with-flask-babelex)'''

''' Fixme : file field for podcast
class PodcastFileWidget(FileAdmin):
    def __call__(self, base_path, *args, **kwargs):
        storage = LocalFileStorage(base_path)
        return super(FileAdmin, self).__init__(*args, storage=storage, **kwargs)

class PodcastFileField(PodcastFileWidget):
    widget = PodcastFileWidget()
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

class PodcastView(ModelView):
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
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
#        'type': [
#            (True, 'Oui'),
#            (False, 'Non')
#        ]
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
            'default': False
        }
    }
    inline_models = (Tag, )
    form_overrides = {
        'desc': CKTextAreaField
    }
#    form_overrides = {
# Fixme : uncomment when PodcastFileField is fixed
#        'link': PodcastFileField
#     }

class SectionView(ModelView):
    form_excluded_columns = ['timestamp']
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'desc': CKTextAreaField
    }

class AuthorView(ModalView):
    form_excluded_columns = ['podcasts']

class LabelView(ModalView):
    form_excluded_columns = ['podcasts', 'sections']

class BlogView(ModelView):
    form_excluded_columns = ['timestamp']
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    form_overrides = {
        'content': CKTextAreaField
    }

admin.add_view(PodcastView(Podcast, db.session))
admin.add_view(BlogView(BlogPost, db.session))
admin.add_view(AuthorView(Author, db.session))
admin.add_view(ModelView(Event, db.session))
admin.add_view(LabelView(Label, db.session))
admin.add_view(SectionView(Section, db.session))
