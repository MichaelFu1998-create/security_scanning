def substitute(prev, *args, **kw):
    '''alias of string.Template.substitute'''
    template_obj = string.Template(*args, **kw)
    for data in prev:
        yield template_obj.substitute(data)