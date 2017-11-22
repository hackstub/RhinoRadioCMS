from flask import Flask, render_template, request, jsonify
from functools import wraps
from functools import partial

#########################################
#  Wrapper for partial content loading  #
#########################################

def partial_content(f, history=True):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # We make sure to come from an 'already loaded site' ...
        # Otherwise, load the base and include the given template
        data = f(*args, **kwargs)
        if not 'X-Partial-Content' in request.headers:
            return render_template('base.html', **data['content'])

        # Data should be a dict with 2 keys:
        # - name of a js function
        # - data for the js function
        assert isinstance(history, bool)
        assert isinstance(data, dict)
        assert len(data) == 2
        assert isinstance(data['function'], str)
        assert isinstance(data['content'], dict)
        # if true, the js will change the url (history.pushState())
        data['history'] = history

        response = jsonify(data)
        response.status_code = 200
        return response

    return decorated_function

def partial_content_decorator():
    return partial(partial_content)

def partial_content_no_history_decorator():
    return partial(partial_content, history=False)
