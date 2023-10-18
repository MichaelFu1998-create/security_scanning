def string(html, start_on=None, ignore=(), use_short=True, **queries):
    '''Returns a blox template from an html string'''
    if use_short:
        html = grow_short(html)
    return _to_template(fromstring(html), start_on=start_on,
                        ignore=ignore, **queries)