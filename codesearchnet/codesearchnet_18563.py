def safe_substitute(prev, *args, **kw):
    '''alias of string.Template.safe_substitute'''
    template_obj = string.Template(*args, **kw)
    for data in prev:
        yield template_obj.safe_substitute(data)