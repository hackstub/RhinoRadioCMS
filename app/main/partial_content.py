from flask import Flask, render_template, request, jsonify
from functools import wraps
from functools import partial

#########################################
#  Wrapper for partial content loading  #
#########################################

def partial_content(f, base):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # We make sure to come from an 'already loaded site' ...
        # Otherwise, load the base with a small javascript snippet that tells
        # to re-request the loading of the content
        if not 'X-Partial-Content' in request.headers:
            return base()

        data = f(*args, **kwargs)

        # Data should be a list [ ] with 2 elements :
        # - name of a js function
        # - data for the js function
        assert isinstance(data, list)
        assert len(data) == 2
        assert isinstance(data[0], str)
        assert isinstance(data[1], dict)

        response = jsonify(data)
        response.status_code = 200
        return response

    return decorated_function

def partial_content_decorator(base):
    return partial(partial_content, base=base)
