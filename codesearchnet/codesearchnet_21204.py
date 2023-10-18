def file(file_object, start_on=None, ignore=(), use_short=True, **queries):
    '''Returns a blox template from a file stream object'''
    return string(file_object.read(), start_on=start_on, ignore=ignore, use_short=use_short, **queries)