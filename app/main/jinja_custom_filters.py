def format_date(value, format='%d/%m/%Y'):
    """ Return date to given format"""
    return value.strftime(format)

custom_filters = {
    'format_date' : format_date,
}
