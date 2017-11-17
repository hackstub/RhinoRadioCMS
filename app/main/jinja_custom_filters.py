from jinja2 import filters

# FIXME try to make decorator @app.template_filter() work
# figuring out where is jinja_env or create it
def format_date(value, format='%d/%m/%Y'):
    """ Return date to given format"""
    return value.strftime(format)

filters.FILTERS['format_date'] = format_date
