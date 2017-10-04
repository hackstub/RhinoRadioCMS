from flask_admin.contrib.sqla import ModelView

class PodcastView(ModelView):
    create_modal = True
    
    form_choices = {
        'mood': [
            ('slow', 'Au pas'),
            ('medium', 'Au trot'),
            ('fast', 'Au galop !')
        ]
    }
    
    form_ajax_refs = {
        'authors': {
            'fields': ['author_id'],
            'page_size': 10
        }
    }